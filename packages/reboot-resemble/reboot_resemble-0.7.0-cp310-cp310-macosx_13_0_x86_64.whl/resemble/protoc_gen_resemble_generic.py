#!/usr/bin/env python3
import os
from dataclasses import asdict, dataclass
from google.api import annotations_pb2
from google.protobuf.descriptor import (
    Descriptor,
    FieldDescriptor,
    FileDescriptor,
    MethodDescriptor,
    ServiceDescriptor,
)
from google.protobuf.descriptor_pb2 import (
    FileDescriptorProto,
    ServiceDescriptorProto,
)
# TODO: Dependency not recognized in git-submodule for some reason.
from pyprotoc_plugin.helpers import (  # type: ignore[import]
    add_template_path,
    load_template,
)
from pyprotoc_plugin.plugins import ProtocPlugin  # type: ignore[import]
from resemble.cli import terminal
from resemble.options import (
    get_method_options,
    get_service_options,
    is_resemble_service,
)
from resemble.v1alpha1 import options_pb2
from typing import Literal, Optional, Sequence

# NOTE: we need to add the template path so we can test
# `ResembleProtocPlugin` even when we're not '__main__'.
add_template_path(os.path.join(__file__, '../templates/'))

Feature = Literal[
    'reader',
    'writer',
    'transaction',
    'error',
    'streaming',
    'workflow',
]


class UserProtoError(Exception):
    """Exception raised in case of a malformed user-provided proto file."""
    pass


@dataclass(kw_only=True)
class PluginSpecificData:
    template_filename: str
    output_filename_suffix: str
    supported_features: list[Feature]


ProtoType = str


@dataclass
class ProtoMethodOptions:
    kind: str
    constructor: bool
    state_streaming: bool
    has_errors: bool


@dataclass
class BaseMethodOptions:
    proto: ProtoMethodOptions


@dataclass
class ProtoMethod:
    name: str
    client_streaming: bool
    server_streaming: bool


@dataclass
class BaseMethod:
    proto: ProtoMethod
    options: BaseMethodOptions


@dataclass
class ProtoServiceOptions:
    state_name: str


@dataclass
class BaseServiceOptions:
    proto: ProtoServiceOptions


@dataclass
class ProtoService:
    name: str
    has_constructor: bool
    requires_constructor: bool


@dataclass
class BaseService:
    proto: ProtoService
    # The following is a Sequence, not list, to make it covariant:
    #   https://mypy.readthedocs.io/en/stable/common_issues.html#variance
    methods: Sequence[BaseMethod]
    options: BaseServiceOptions


@dataclass
class ProtoFile:
    package_name: str
    file_name: str
    # List of all messages and enums in the proto file.
    messages_and_enums: list[str]


@dataclass
class BaseFile:
    proto: ProtoFile
    # The following is a Sequence, not list, to make it covariant:
    #   https://mypy.readthedocs.io/en/stable/common_issues.html#variance
    services: Sequence[BaseService]


class ResembleProtocPlugin(ProtocPlugin):

    @staticmethod
    def plugin_specific_data() -> PluginSpecificData:
        """Returns the plugin-specific data for the plugin."""
        raise NotImplementedError

    @classmethod
    def _proto_message_and_enum_names(
        self,
        file: FileDescriptor,
    ) -> list[str]:
        """Helper to extract name of all messages and enums from file descriptor.
        """
        # NOTE: `message_types_by_name` is undefined if no messages are present.
        try:
            # Include *only* top-level messages and enums in the file. Accessing
            # nested structures is supported through parent message, which will
            # be included in the list of.
            import_messages_and_enums = list(
                file.message_types_by_name.keys()
            ) + list(file.enum_types_by_name.keys())

            return import_messages_and_enums
        except AttributeError as e:
            assert 'message_types_by_name' in str(e)
            return []

    def template_data(
        self,
        proto_file: FileDescriptorProto,
    ) -> Optional[BaseFile]:
        file = self.pool.FindFileByName(proto_file.name)
        if file.package == '':
            raise UserProtoError(
                f"{file.name} is missing a (currently) required 'package'"
            )

        directory = os.path.dirname(file.name)
        package_directory = file.package.replace('.', os.path.sep)
        if package_directory != directory:
            raise UserProtoError(
                f"Proto file '{file.name}' has package '{file.package}', but "
                "based on the file's path the expected package was "
                f"'{directory.replace(os.path.sep, '.')}'. 'rsm protoc' "
                "expects the package to match the directory structure. Check "
                "that the API base directory is correct, and if so, adjust "
                "either the proto file's location or its package."
            )

        # Validate that only legacy gRPC services are using the
        # `google.api.http` annotations.
        for service in proto_file.service:
            if not is_resemble_service(file.services_by_name[service.name]):
                # Legacy gRPC services are allowed to have `google.api.http`
                # annotations.
                continue
            for method in service.method:
                if method.options.HasExtension(annotations_pb2.http):
                    # The user has specified HTTP annotations on a Resemble
                    # service's methods. We don't support this (yet).
                    #
                    # TODO(rjh): consider what it would take to allow Resemble
                    #            services to have their own `google.api.http`
                    #            annotations; at least singletons.
                    raise UserProtoError(
                        f"Service '{service.name}' method '{method.name}' "
                        "has a 'google.api.http' annotation. This is only "
                        "supported for legacy gRPC services, not for Resemble "
                        "methods. Let the maintainers know about your use case "
                        "if you feel this is a limitation!"
                    )

        template_data = self.plugin_template_data(proto_file)
        # 'template_data.services' only contains Resemble services. If the
        # `proto_file` does not contain resemble services, i.e. dependencies,
        # do not generate Resemble-specific code.
        if len(template_data.services) == 0:
            return None

        self.validate_features(template_data)

        for service in template_data.services:
            for method in service.methods:
                if method.proto.client_streaming and method.options.proto.kind != 'reader':
                    raise UserProtoError(
                        'Client streaming only supported for readers'
                    )
                if method.proto.server_streaming and method.options.proto.kind != 'reader':
                    raise UserProtoError(
                        'Server streaming only supported for readers'
                    )

        return template_data

    def _analyze_proto_file(self, proto_file: FileDescriptor) -> ProtoFile:
        return ProtoFile(
            package_name=proto_file.package,
            file_name=proto_file.name,
            messages_and_enums=self._proto_message_and_enum_names(proto_file),
        )

    def _analyze_proto_service_options(
        self, service: ServiceDescriptor
    ) -> ProtoServiceOptions:
        service_options = get_service_options(service.GetOptions())
        return ProtoServiceOptions(
            state_name=service_options.state.split('.')[-1],
        )

    def _is_default_constructible(self, service: ServiceDescriptor) -> bool:
        service_options = get_service_options(service.GetOptions())
        return service_options.default_constructible

    def _is_method_constructor(self, method: MethodDescriptor) -> bool:
        method_options = get_method_options(method.GetOptions())
        kind: Optional[str] = method_options.WhichOneof('kind')
        if kind is None:
            raise UserProtoError(
                f"'{method.name}' is missing the required Resemble annotation 'kind'"
            )

        return kind in [
            'writer', 'transaction'
        ] and getattr(method_options, kind).HasField('constructor')

    @classmethod
    def _is_map_field(
        cls, message: Descriptor, field: FieldDescriptor
    ) -> bool:
        # Protobuf encodes its `map` type as a repeated message type name
        # `{${Field}Entry}`, which is an inner type of the message with the
        # same name as the field.
        field_camelcase_name = ''.join(
            component.capitalize() for component in field.name.split('_')
        )
        return (
            field.type == FieldDescriptor.TYPE_MESSAGE and
            field.label == FieldDescriptor.LABEL_REPEATED and
            field.message_type.containing_type == message and
            field.message_type.name == f'{field_camelcase_name}Entry'
        )

    def _analyze_proto_service(
        self,
        service_proto: ServiceDescriptorProto,
        service_descriptor: ServiceDescriptor,
    ) -> ProtoService:
        has_constructor = False
        requires_constructor = False

        if not self._is_default_constructible(service_descriptor):
            for method in service_descriptor.methods:
                if self._is_method_constructor(method):
                    has_constructor = True
                    requires_constructor = True
                    break

        return ProtoService(
            name=service_proto.name,
            has_constructor=has_constructor,
            requires_constructor=requires_constructor,
        )

    def _analyze_proto_method(self, method: MethodDescriptor) -> ProtoMethod:
        return ProtoMethod(
            name=method.name,
            client_streaming=method.client_streaming,
            server_streaming=method.server_streaming,
        )

    def _analyze_proto_method_options(
        self,
        method: MethodDescriptor,
        streaming: bool,
    ) -> ProtoMethodOptions:
        method_options = get_method_options(method.GetOptions())
        kind: Optional[str] = method_options.WhichOneof('kind')

        if kind is None:
            raise UserProtoError(
                f"'{method.name}' is missing the required Resemble annotation 'kind'"
            )

        state_streaming = streaming

        if kind == 'reader':
            if (
                method_options.reader.state ==
                options_pb2.ReaderMethodOptions.State.STREAMING
            ):
                state_streaming = True
            elif (
                method_options.reader.state ==
                options_pb2.ReaderMethodOptions.State.UNARY
            ):
                state_streaming = False

        return ProtoMethodOptions(
            kind=kind,
            constructor=self._is_method_constructor(method),
            state_streaming=state_streaming,
            has_errors=len(method_options.errors) > 0,
        )

    def process_file(self, proto_file: FileDescriptorProto) -> None:
        try:
            if (
                proto_file.syntax != "proto3"
                # Special case: the `descriptor.proto` doesn't report a syntax,
                #               but we know we can handle it.
                and proto_file.name != "google/protobuf/descriptor.proto"
            ):
                raise UserProtoError(
                    f"Unsupported: not a proto3 file. "
                    "Resemble only supports proto files that set "
                    "'syntax=\"proto3\";', but got "
                    f"'syntax=\"{proto_file.syntax}\";'"
                )

            template_data = self.template_data(proto_file)

            if template_data is None:
                return None

            for service in template_data.services:
                if len(service.methods) == 0:
                    raise UserProtoError(
                        f"Service '{service.proto.name}' has no rpc methods specified. "
                        "Complete your proto file."
                    )

            content = self.template_render(template_data)
            output_file = self.response.file.add()
            output_file.name = template_data.proto.file_name.replace(
                '.proto',
                self.plugin_specific_data().output_filename_suffix,
            )
            output_file.content = content

        except (UserProtoError, ValueError) as error:
            # NOTE: we catch `ValueError` here because we're using methods from
            # `options.py` that might raise `ValueError` in response to
            # malformed input.
            # We re-raise any error as a `UserProtoError`
            # but with additional information in the error message.
            raise UserProtoError(
                f"Error processing '{proto_file.name}': {error}"
            ) from error

    def plugin_template_data(
        self, proto_file: FileDescriptorProto
    ) -> BaseFile:
        raise NotImplementedError

    def validate_features(self, template_data: BaseFile) -> None:
        """Raises an error if not all user-requested features are implemented.
        """
        feature_set_in_template_data = set()

        for service in template_data.services:
            for method in service.methods:
                feature_set_in_template_data.add(method.options.proto.kind)
                if method.options.proto.has_errors is True:
                    feature_set_in_template_data.add('error')
                if method.options.proto.state_streaming or method.proto.client_streaming or method.proto.server_streaming:
                    feature_set_in_template_data.add('streaming')

        supported_feature_set = set(
            self.plugin_specific_data().supported_features
        )

        if not feature_set_in_template_data.issubset(supported_feature_set):
            terminal.fail(
                'You are attempting to use Resemble features in your .proto '
                'file that are not yet supported.\n'
                '\n'
                f'Unsupported features: {feature_set_in_template_data - supported_feature_set}'
            )

    def get_file_for_message_name(
        self,
        message_name: str,
        current_file: FileDescriptor,
    ) -> FileDescriptor:
        if '.' not in message_name:
            # If we don't have a package name, assume it is the same
            # package as the current file.
            package_name = current_file.package
            message_name = f'{package_name}.{message_name}'

        try:
            return self.pool.FindFileContainingSymbol(message_name)
        except KeyError as e:
            raise UserProtoError(
                f"Cannot resolve message type: '{message_name}'"
            ) from e

    def template_render(
        self,
        template_data: BaseFile,
    ) -> str:
        template = load_template(
            self.plugin_specific_data().template_filename,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            extensions=['jinja2_strcase.StrcaseExtension'],
        )

        return template.render(asdict(template_data))
