
# TGFParser

A Python module for parsing the TGF (Trivial Graph Format) output of the Maven Dependency Tree plugin (`mvn dependency:tree`). This module helps in understanding and navigating through Maven project dependencies by providing a structured way to read the TGF formatted dependency tree.

## Features

- Parse TGF files to extract packages and their dependency relations.
- Retrieve direct dependencies of a package.
- Recursively retrieve the full dependency tree of a package.
- Retrieve a list of all packages defined in the TGF file.

## Installation

Install the `tgfparser` module using pip:

```sh
pip install tgfparser
```

## Usage

### Generate dependency tree of a maven project

```bash
mvn clean package org.apache.maven.plugins:maven-dependency-plugin:3.7.1:tree
```  
or  

if you define this plugin in pom.xml then run:
```
mvn dependency:tree
```  

### Importing the Module

```python
from tgfparser import TGFParser, Package
```

### Parsing a TGF File

Initialize the parser and parse a TGF file:

```python
parser = TGFParser()
parser.parse('path/to/your/dependency-tree.tgf')
```

### Accessing the Root Package

Get the root package of the parsed TGF:

```python
root_package = parser.root_package
print(f"Root Package: {root_package}")
```

### Getting Direct Dependencies

Get the direct dependencies of a specific package:

```python
direct_deps = parser.direct_dependencies(parser.root_package.package_id)
print("Direct Dependencies:", direct_deps)
```

### Getting the Full Dependency Tree

Get all dependencies of a specific package recursively:

```python
full_dependency_tree = parser.dependency_tree(parser.root_package.package_id)
print("Full Dependency Tree:", full_dependency_tree)
```

### Retrieving All Packages

Get a list of all packages defined in the TGF file:

```python
all_packages = parser.packages()
print("All Packages:", all_packages)
```

## Example

Here is a complete example for parsing and accessing the data:

```python
from tgfparser import TGFParser

# Initialize the parser
parser = TGFParser()

# Parse the TGF file
parser.parse('example.tgf')

# Access the root package
root_package = parser.root_package
print(f"Root Package: {root_package}")

# Get direct dependencies of the root package
direct_deps = parser.direct_dependencies(root_package.package_id)
print("Direct Dependencies:", direct_deps)

# Get the full dependency tree
full_dependency_tree = parser.dependency_tree(root_package.package_id)
print("Full Dependency Tree:", full_dependency_tree)

# Get all packages defined in the TGF file
all_packages = parser.packages()
print("All Packages:", all_packages)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Authors

- Malayke - [Malayke](https://github.com/malayke)

