#!/usr/bin/env python3
import os
from dataclasses import dataclass
from google.protobuf.descriptor import (
    Descriptor,
    FieldDescriptor,
    FileDescriptor,
    MethodDescriptor,
    ServiceDescriptor,
)
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pool import DescriptorPool
from resemble.cli import terminal
from resemble.options import (
    get_method_options,
    get_service_options,
    is_resemble_service,
)
from resemble.protoc_gen_resemble_generic import (
    BaseFile,
    BaseMethod,
    BaseMethodOptions,
    BaseService,
    BaseServiceOptions,
    PluginSpecificData,
    ProtoType,
    ResembleProtocPlugin,
    UserProtoError,
)
from typing import Optional, Sequence

PythonType = str


@dataclass
class PythonMethodOptions(BaseMethodOptions):
    errors: dict[ProtoType, PythonType]


@dataclass
class PythonMethod(BaseMethod):
    options: PythonMethodOptions
    input_type: PythonType
    output_type: PythonType
    input_type_fields: dict[str, str]


@dataclass
class PythonServiceOptions(BaseServiceOptions):
    state_pb2_name: str


@dataclass
class PythonService(BaseService):
    methods: Sequence[PythonMethod]
    options: PythonServiceOptions


@dataclass
class PythonLegacyGrpcService:
    name: str


@dataclass
class PythonFile(BaseFile):
    # The following is a Sequence, not list, to make it covariant:
    #   https://mypy.readthedocs.io/en/stable/common_issues.html#variance
    services: Sequence[PythonService]
    # List of gRPC services that are not resemble services.
    legacy_grpc_services: list[PythonLegacyGrpcService]
    imports: set[str]
    # The name of the Python protoc generated '*_pb2.py' file.
    pb2_name: str
    # The name of the Python protoc generated '*_pb2_grpc.py' file.
    pb2_grpc_name: str


class PythonResembleProtocPlugin(ResembleProtocPlugin):

    def __init__(self, pool: Optional[DescriptorPool] = None):
        """Initialize the plugin with a descriptor pool. Used only when NodeJS
        plugin generates Python Resemble code."""
        if pool is not None:
            self.pool = pool

    def plugin_template_data(
        self, proto_file: FileDescriptorProto
    ) -> BaseFile:
        file = self.pool.FindFileByName(proto_file.name)
        python_file: BaseFile = PythonFile(
            proto=self._analyze_proto_file(file),
            services=[
                PythonService(
                    proto=self._analyze_proto_service(
                        service,
                        file.services_by_name[service.name],
                    ),
                    methods=[
                        PythonMethod(
                            proto=self._analyze_proto_method(method),
                            options=PythonMethodOptions(
                                proto=self._analyze_proto_method_options(
                                    file.services_by_name[service.name].
                                    methods_by_name[method.name],
                                    method.client_streaming or
                                    method.server_streaming
                                ),
                                errors=self._analyze_errors(
                                    file.services_by_name[service.name].
                                    methods_by_name[method.name]
                                ),
                            ),
                            input_type=self._get_python_type_from_proto_type(
                                file.services_by_name[service.name].
                                methods_by_name[method.name].input_type
                            ),
                            output_type=self._get_python_type_from_proto_type(
                                file.services_by_name[service.name].
                                methods_by_name[method.name].output_type
                            ),
                            input_type_fields=self._analyze_message_fields(
                                file.services_by_name[service.name].
                                methods_by_name[method.name].input_type
                            ),
                        ) for method in service.method
                    ],
                    options=PythonServiceOptions(
                        proto=self._analyze_proto_service_options(
                            file.services_by_name[service.name]
                        ),
                        state_pb2_name=self._get_pb2_name_for_state(
                            file.services_by_name[service.name]
                        )
                    )
                ) for service in proto_file.service if
                is_resemble_service(file.services_by_name[service.name])
            ],
            legacy_grpc_services=[
                PythonLegacyGrpcService(name=service.name)
                for service in proto_file.service
                if
                not is_resemble_service(file.services_by_name[service.name])
            ],
            imports=self._analyze_imports(file),
            pb2_name=self._get_pb2_file_name(file),
            pb2_grpc_name=self._get_pb2_file_name(file) + '_grpc',
        )

        return python_file

    @staticmethod
    def plugin_specific_data() -> PluginSpecificData:
        return PluginSpecificData(
            template_filename="resemble.py.j2",
            output_filename_suffix="_rsm.py",
            supported_features=[
                "reader",
                "writer",
                "transaction",
                "error",
                "streaming",
                "workflow",
            ]
        )

    def _get_pb2_name_for_state(self, service: ServiceDescriptor) -> str:
        """Get gRPC Python module name from service descriptor.
        """
        service_options = get_service_options(service.GetOptions())
        state_name = service_options.state
        file = self.get_file_for_message_name(state_name, service.file)
        return self._get_pb2_file_name(file)

    @classmethod
    def _get_pb2_file_name(cls, file: FileDescriptor) -> str:
        """Get gRPC Python module name from file descriptor name and package.
        """
        file_name = os.path.basename(file.name).removesuffix('.proto')
        return file.package + '.' + file_name + '_pb2'

    @classmethod
    def _py_type_name(cls, message: Descriptor) -> str:
        """Get type name of the given message type, including any enclosing
        types.
        """
        if message.containing_type is None:
            return message.name
        return f"{cls._py_type_name(message.containing_type)}.{message.name}"

    @classmethod
    def _get_python_type_from_proto_type(
        cls,
        message: Descriptor,
    ) -> str:
        """Get full name (package and type) of generated gRPC message from
        message descriptor.
        """
        py_type_name = cls._py_type_name(message)
        py_module_name = cls._get_pb2_file_name(message.file)
        full_py_type_name = f'{py_module_name}.{py_type_name}'
        return full_py_type_name

    @classmethod
    def _get_python_type_from_map_entry_type(
        cls,
        message: Descriptor,
    ) -> str:
        """Gets a fully qualified `dict[K,V]` type definition for the given `repeated ${Field}Entry`
        message.

        Protobuf encodes its `map` type as a repeated message type name `{${Field}Entry}`, which is
        an inner type of the message with the same name as the field.
        """

        field_types = cls._analyze_message_fields(message)
        if set(field_types.keys()) != {'key', 'value'}:
            raise UserProtoError(
                f"Unexpected content for `map` field type message: {field_types}. "
                "Please report this issue to the maintainers!"
            )

        key_name = field_types['key']
        value_name = field_types['value']

        return f'dict[{key_name}, {value_name}]'

    def _analyze_errors(
        self, method: MethodDescriptor
    ) -> dict[ProtoType, PythonType]:
        method_options = get_method_options(method.GetOptions())
        # From error name, e.g., 'product.api.ErrorName' to Python type, e.g., {
        # 'product.api.ErrorName': 'product.api.file_pb2.ErrorName' }.
        errors: dict[ProtoType, PythonType] = {}

        for error in method_options.errors:
            file = self.get_file_for_message_name(
                message_name=error,
                current_file=method.containing_service.file,
            )
            errors[f"{file.package}.{error.split('.')[-1]}"
                  ] = self._get_python_type_from_proto_type(
                      file.message_types_by_name[error.split('.')[-1]],
                  )

        return errors

    @classmethod
    def _analyze_imports(cls, file: FileDescriptor) -> set[str]:
        """Return set of python imports necessary for our generated code
        based on the file descriptor.
        """
        # Firstly, we need the standard gRPC modules, i.e., `_pb2` and
        # `_pb2_grpc`...
        imports = {
            cls._get_pb2_file_name(file),
            cls._get_pb2_file_name(file) + '_grpc'
        }

        # Also include each 'import' in the .proto file.
        for dependency in file.dependencies:
            imports.add(cls._get_pb2_file_name(dependency))

        return imports

    @classmethod
    def _analyze_message_fields(
        cls,
        message: Descriptor,
    ) -> dict[str, str]:
        """Returns a dict from field name, e.g., 'foo' to type
        depending on language, e.g., { 'foo': 'product.api.file_pb2.Foo' }.
        """
        py_types: dict[int, str] = {
            FieldDescriptor.TYPE_DOUBLE: 'float',
            FieldDescriptor.TYPE_FLOAT: 'float',
            FieldDescriptor.TYPE_INT32: 'int',
            FieldDescriptor.TYPE_INT64: 'int',
            FieldDescriptor.TYPE_UINT32: 'int',
            FieldDescriptor.TYPE_UINT64: 'int',
            FieldDescriptor.TYPE_SINT32: 'int',
            FieldDescriptor.TYPE_SINT64: 'int',
            FieldDescriptor.TYPE_FIXED32: 'int',
            FieldDescriptor.TYPE_FIXED64: 'int',
            FieldDescriptor.TYPE_SFIXED32: 'int',
            FieldDescriptor.TYPE_SFIXED64: 'int',
            FieldDescriptor.TYPE_BOOL: 'bool',
            FieldDescriptor.TYPE_STRING: 'str',
            FieldDescriptor.TYPE_BYTES: 'bytes',
            FieldDescriptor.TYPE_ENUM: 'int',
        }

        message_fields: dict[str, str] = {}

        for field in message.fields:
            if cls._is_map_field(message, field):
                message_fields[field.name
                              ] = cls._get_python_type_from_map_entry_type(
                                  field.message_type
                              )
                continue

            if field.type == FieldDescriptor.TYPE_GROUP:
                raise UserProtoError(
                    "Fields of type 'group' are currently not supported"
                )
            elif field.type == FieldDescriptor.TYPE_MESSAGE:
                message_fields[field.name
                              ] = cls._get_python_type_from_proto_type(
                                  field.message_type
                              )
            else:
                assert field.type in py_types
                message_fields[field.name] = py_types[field.type]

            if field.label == FieldDescriptor.LABEL_REPEATED:
                # TODO(benh): can we use 'Iterable' instead of 'list'?
                message_fields[field.name
                              ] = f"list[{message_fields[field.name]}]"

        return message_fields


# This is a separate function (rather than just being in `__main__`) so that we
# can refer to it as a `script` in our `pip_package` BUILD targets.
def main():
    try:
        PythonResembleProtocPlugin.execute()
    except UserProtoError as error:
        terminal.fail(str(error))


if __name__ == '__main__':
    main()
