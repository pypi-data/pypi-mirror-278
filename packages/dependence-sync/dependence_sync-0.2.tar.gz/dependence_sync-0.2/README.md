# DSM: Dependency Sync Manager

## Introduction: 
DSM can centrally manage third-party and second-party dependencies in your code repository without the need for using LFS or any other cloud storage.

## Instructions
```shell
# View Help Information
dsm -h
dsm sync -h
dsm init -h

# Initialize Workspace
dsm init path
path: root directory

# Synchronize Dependency Code
dsm sync path [-f]
path: Directory where the dependency management file DEPS is located
-f: Force Pull Code, Ignore Cache
```

## Usage
1. `pip install dependence-sync`
2. `dsm init {your_workspace_root_path}`
3. Create a new DEPS file
```python
deps = {
    "local/path": {
        "type":"git", # Dependency type, currently only supports git
        "repo": "xxx.git", # Git repository address
        "commit": "xxxxxx",
        "ignore": True # Whether it is not managed by git after synchronization, default is True
    }
}
```
4. `dsm sync -f {DEPS_PATH}` eg `dsm sync -f .`
