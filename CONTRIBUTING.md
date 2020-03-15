# Contributing

## Development process

### General guidelines

* Be uniform with the already written code
* Avoid too many comments, prefer code that is readable without them
* Avoid methods/function that are too long
* Keep the documentation up-to-date

*WIP*

### Technical information

#### Formatter

The formatter used in the project is [**YAPF** (*Yet Another Python Formatter*)](https://github.com/google/yapf). It can be installed easily via pip: `pip install yafp`

To format all the files in the project, run `yapf -ir .` from the root of the project

#### Branch names

The name of every branch shall be coherent with the existing ones and will follow the nomenclature `module/specific_feature`, for example `crawler/piemonte` to indicate an implementation related to the data crawler for the Piemonte region

#### Pull requests

For each new branch a pull request shall be created in order to review the changes before merging it to the master