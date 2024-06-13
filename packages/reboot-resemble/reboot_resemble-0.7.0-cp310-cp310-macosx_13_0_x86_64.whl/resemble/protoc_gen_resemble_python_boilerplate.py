import os
from dataclasses import dataclass
from google.protobuf.descriptor import FileDescriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from resemble.cli import terminal
from resemble.protoc_gen_resemble_generic import (
    BaseFile,
    PluginSpecificData,
    UserProtoError,
)
from resemble.protoc_gen_resemble_python import (
    PythonFile,
    PythonResembleProtocPlugin,
)


@dataclass
class PythonBoilerplateFile(PythonFile):
    # The `..._rsm` module name of the Resemble generated Python code for this
    # proto file.
    rsm_name: str
    has_reader_method: bool
    has_writer_method: bool
    has_transaction_method: bool
    has_workflow_method: bool
    has_streaming_method: bool


class PythonResembleBoilerplateProtocPlugin(PythonResembleProtocPlugin):

    @staticmethod
    def plugin_specific_data() -> PluginSpecificData:
        return PluginSpecificData(
            template_filename="servicer_boilerplate.py.j2",
            output_filename_suffix="_servicer.py",
            supported_features=[
                "reader",
                "writer",
                "transaction",
                "error",
                "streaming",
                "workflow",
            ]
        )

    def plugin_template_data(
        self, proto_file: FileDescriptorProto
    ) -> BaseFile:
        file = self.pool.FindFileByName(proto_file.name)
        python_file = super().plugin_template_data(proto_file)

        assert isinstance(python_file, PythonFile)

        python_boilerplate_file = PythonBoilerplateFile(
            proto=python_file.proto,
            services=python_file.services,
            legacy_grpc_services=python_file.legacy_grpc_services,
            imports=python_file.imports,
            pb2_name=python_file.pb2_name,
            pb2_grpc_name=python_file.pb2_grpc_name,
            rsm_name=self.rsm_module_name(file),
            has_reader_method=False,
            has_writer_method=False,
            has_transaction_method=False,
            has_workflow_method=False,
            has_streaming_method=False,
        )

        for service in python_boilerplate_file.services:
            for method in service.methods:
                if method.options.proto.kind == "reader":
                    python_boilerplate_file.has_reader_method = True
                elif method.options.proto.kind == "writer":
                    python_boilerplate_file.has_writer_method = True
                elif method.options.proto.kind == "transaction":
                    python_boilerplate_file.has_transaction_method = True
                elif method.options.proto.kind == "workflow":
                    python_boilerplate_file.has_workflow_method = True

                if method.proto.client_streaming or method.proto.server_streaming or method.options.proto.state_streaming:
                    python_boilerplate_file.has_streaming_method = True
                # We are doing re-export from the generated "*_rsm.py" file for
                # the messages described in the same proto file. So we can
                # remove the package prefix from the input and output types and
                # use the short name directly.
                if python_boilerplate_file.pb2_name in method.input_type:
                    method.input_type = method.input_type.replace(
                        python_boilerplate_file.pb2_name + ".",
                        "",
                    )
                if python_boilerplate_file.pb2_name in method.output_type:
                    method.output_type = method.output_type.replace(
                        python_boilerplate_file.pb2_name + ".",
                        "",
                    )

        return python_boilerplate_file

    @classmethod
    def rsm_module_name(cls, file: FileDescriptor) -> str:
        """Get Resemble Python generated module name from file descriptor name
        and package.
        """
        file_name = os.path.basename(file.name).removesuffix('.proto')
        return file.package + '.' + file_name + '_rsm'


# This is a separate function (rather than just being in `__main__`) so that we
# can refer to it as a `script` in our `pip_package` BUILD targets.
def main():

    try:
        PythonResembleBoilerplateProtocPlugin.execute()
    except UserProtoError as error:
        terminal.fail(str(error))


if __name__ == '__main__':
    main()
