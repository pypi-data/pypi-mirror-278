# Py_RHT
#### Really Helpful Tools for developers

- [Py\_RHT](#py_rht)
      - [Really Helpful Tools for developers](#really-helpful-tools-for-developers)
  - [Structure](#structure)
  - [How to use](#how-to-use)
  - [Crypto submodule](#crypto-submodule)
    - [calling the submodule](#calling-the-submodule)
    - [Methods](#methods)
  - [Forensics submodule](#forensics-submodule)
  - [Programming submodule](#programming-submodule)


## Structure
```
PY_RHT                                                           
  |- Crypto: contains functions related to cryptography                        
  |- Forensics: contains forensics funtions                                    
  |- Programming: catchall folder for programming tools/file format classes   
```

## How to use
```
pip install Py_RHT
```

inside your python file then import the module like this:

```python
import Py_RHT as rht
```
this will then allow you to call all modules included in the package

call funtions like this
```python
rht.(modulename).(methodname)
```
Every function has a docstring labeling I/O and types

## Base module

#### methods
| name   | type     | call  |
| ------ | -------- | ----- |
| binary | datatype | bin() |

## Crypto submodule

#### Methods

| name     | type     | call                  |
| -------- | -------- | --------------------- |
| xor      | bitwise  | xor()                 |
| bitshift | bitwise  | bitshift()            |
| reverse  | bitwise  | reverse()             |
| base64   | encoding | b64_encode()/decode() |
|          |          |                       |


## Forensics submodule

#### methods
| name | type | call |
| ---- | ---- | ---- |
|      |      |      |

## Programming submodule

#### methods
| name | type | call |
| ---- | ---- | ---- |
|      |      |      |
