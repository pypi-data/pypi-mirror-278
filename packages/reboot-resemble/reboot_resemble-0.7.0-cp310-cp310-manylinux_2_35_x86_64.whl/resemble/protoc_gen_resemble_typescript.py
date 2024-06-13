#!/usr/bin/env python3
import os
from google.protobuf.descriptor import Descriptor, FileDescriptor
from resemble.protoc_gen_resemble_generic import ResembleProtocPlugin


class TypescriptResembleProtocPlugin(ResembleProtocPlugin):
    """Helper class for the Resemble Protoc plugin. Used as based class
    for the NodeJS and React plugins."""

    @classmethod
    def _get_pb_file_name(cls, file: FileDescriptor) -> str:
        """Get gRPC Typescript module name from file descriptor name and package.
        """
        file_name = os.path.basename(file.name).removesuffix('.proto')

        # Generated "*_rsm_react" and "*_pb" files will always be in the same
        # directory.
        return file_name + '_pb'

    @classmethod
    def _get_typescript_type_from_proto_type(
        cls,
        message: Descriptor,
        file: FileDescriptor,
    ) -> str:
        """Get full name of generated gRPC message from message descriptor.
        'unique_name.MessageName' for NodeJS and React plugins.
        """
        if message.file.name == file.name or cls._is_google_or_resemble_package(
            message.file.package
        ):
            # Means that the proto type is described in the same file
            # and we can import it by a name or it is a non user defined type,
            # that comes from google or resemble.v1alpha1 package.
            return message.name

        unique_name = cls._get_unique_name_from_proto(message.file.name)
        return f"{unique_name}.{message.name}"

    @classmethod
    def _is_google_or_resemble_package(cls, package_name: str) -> bool:
        return package_name.startswith(
            'google.'
        ) or package_name == 'resemble.v1alpha1'

    @classmethod
    def _get_unique_name_from_proto(cls, proto_name: str) -> str:
        # We can't import types with their full names in ts, so we will use
        # the following structure:
        #       import * as <unique_name> from '<relative_path>'
        # To generate unique_name we will replace all '/' with '_' (since the '/'
        # is not allowed in the import statement) and all '_' symbols in the
        # source name with '__', to avoid conflicts with the '/' to '_' replacement.
        proto_name = proto_name.replace('.proto', '')
        proto_name = proto_name.replace('_', '__')
        proto_name = proto_name.replace(os.path.sep, '_')
        return proto_name

    @classmethod
    def _analyze_imports(cls, file: FileDescriptor) -> dict[str, str]:
        # We need to import all the dependencies of the file, so we can use
        # the types from them. We will import them by their unique names.
        # 'imports' is a dictionary where the key is the relative path to the
        # file and the value is the unique name of the file.
        imports: dict[str, str] = {}

        # Also include each 'import' in the .proto file.
        for dependency in file.dependencies:
            if cls._is_google_or_resemble_package(dependency.package):
                # We shouldn't import google.* and resemble.v1alpha1 packages, since
                # we ship them with the plugin, so they are already available.
                continue

            unique_name = cls._get_unique_name_from_proto(dependency.name)
            folder = os.path.dirname(dependency.name)
            relative_path = os.path.relpath(folder, os.path.dirname(file.name))

            imports[os.path.join(
                relative_path,
                os.path.basename(dependency.name).replace('.proto', '_pb')
            )] = unique_name

        return imports

    @classmethod
    def _get_google_protobuf_messages(cls, file: FileDescriptor) -> set[str]:
        """Returns a set of message type names from the google.protobuf package.
        """
        google_protobuf_deps = []
        for dep in file.dependencies:
            if dep.package.startswith('google.protobuf'):
                google_protobuf_deps += list(dep.message_types_by_name.keys())

        return set(google_protobuf_deps)
