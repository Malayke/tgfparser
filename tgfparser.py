import json
from pathlib import Path


class Package:
    def __init__(self, package_id, group_id, artifact_id, version, scope) -> None:
        self.package_id = package_id
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.scope = scope

    def __str__(self) -> str:
        return f"{self.group_id}:{self.artifact_id}:{self.version}"

    def __repr__(self) -> str:
        return f"{self.group_id}:{self.artifact_id}:{self.version}"

    def json(self):
        data = {}
        for key in self.__dict__:
            data[key] = getattr(self, key)
        return json.dumps(data)


class TGFParser:
    '''Class for parsing TGF files representing dependency trees'''

    def __init__(self):
        """
        Initialize the TGFParser.
        This can include setup for any internal data structures you might need.
        """
        self.package_lines = []
        self.relation_lines = []
        self.root_package = None

    def parse(self, file_path):
        """
        Parse the TGF file at the given path.

        :param file_path: Path to the TGF file.
        """
        tgf_content = self._read_tgf(file_path)
        package_lines, relation_lines = self._split_tgf(tgf_content)
        self.package_lines = package_lines.splitlines()
        self.relation_lines = relation_lines.splitlines()
        group_id, artifact_id, _, version = self.package_lines[0].split()[1].split(':')
        
        self.root_package = Package(
            package_id=self.package_lines[0].split()[0],
            group_id=group_id,
            artifact_id=artifact_id,
            version=version,
            scope=''
        )

    def _read_tgf(self, file_path: Path) -> str:
        """
        Read TGF file and return file content.

        :param file_path: Path to the TGF file.
        :return: TGF file content as a string.
        """
        with open(file_path) as f:
            data = f.read()
        return data

    def _split_tgf(self, tgf_content: str) -> list:
        """
        Split TGF content into package and relation sections.

        :param tgf_content: String data from the TGF file.
        :return: A tuple of (package_lines, relation_lines).
        """
        return tgf_content.split('#')

    def _tgf_line_to_package(self, tgf_line: str) -> Package:
        """
        Convert a TGF line to a Package object.

        :param tgf_line: A line from the TGF file representing a package.
        :return: A Package object.
        """
        splited_line = tgf_line.split()[1].split(':')
        if len(splited_line) == 4:
            group_id, artifact_id, _, version = splited_line
            scope = ''
        else:
            group_id, artifact_id = splited_line[:2]
            version, scope = splited_line[-2:]
        
        return Package(
            package_id=tgf_line.split()[0],
            group_id=group_id,
            artifact_id=artifact_id,
            version=version,
            scope=scope
        )
        
    def packages(self) -> list[Package]:
        """
        Get all packages defined in the TGF file.

        :return: A list of Package objects.
        """
        return [self._tgf_line_to_package(line) for line in self.package_lines]
    
    def get_dependencies_by_package_id(self, package_id: str) -> list[Package]:
        """
        Get dependencies of a package by its package ID.

        :param package_id: The package ID.
        :return: A list of Package objects representing dependencies.
        """
        dependencies = []
        deps_id = [line.split()[1] for line in self.relation_lines if line.startswith(package_id)]
        dep_lines = [line for line in self.package_lines if line.split()[0] in deps_id]
        for line in dep_lines:
            package = self._tgf_line_to_package(line)
            dependencies.append(package)
        return dependencies


    def get_package_by_id(self, package_id: str) -> Package:
        """
        Get a Package object by its package ID.

        :param package_id: The package ID.
        :return: A Package object.
        """
        package_line = [line for line in self.package_lines if line.startswith(package_id)][0]
        return self._tgf_line_to_package(package_line)

    def get_dependencies(self, package_id: str) -> dict:
        """
        Get direct dependencies of a package by its package ID.

        :param package_id: The package ID.
        :return: A dictionary representing the direct dependency tree.
        """
        deps = self.get_dependencies_by_package_id(package_id)
        result = {str(dep): {} for dep in deps}
        return result

    def dependency_tree(self, package_id: str) -> dict:
        """
        Get all dependencies of a package recursively by its package ID.

        :param package_id: The package ID.
        :return: A dictionary representing the recursive dependency tree.
        """
        def get_deps(package_id: str) -> dict:
            deps = self.get_dependencies_by_package_id(package_id)
            result = {}
            for dep in deps:
                result[str(dep)] = get_deps(dep.package_id)
            return result

        return get_deps(package_id)
