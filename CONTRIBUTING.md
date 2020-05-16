# Contributing

If you are in any way interested in this project and you would like to help, feel free to contact me (refer to the contact info on my profile)

## Development process

### General guidelines

* Be uniform with the already written code
* Avoid too many comments, write code that is readable using appropriate variable names
* Try to avoid really long functions
* Keep the documentation up-to-date

### Technical information

#### Formatter

The formatter used in the project is [**YAPF** (*Yet Another Python Formatter*)](https://github.com/google/yapf). It can be installed easily via pip: `pip3 install yafp`

To format all the files in the project, run `yapf -ir .` from the top project folder

#### Branch names

* The name of every branch shall be coherent with the existing ones and will follow the nomenclature `module/specific_feature`

* All successive reworks/improvements to the same module should be indicated appending to the original branch name

##### Examples

```
crawler/piemonte
crawler/piemonte_v2
```

### Workflow

#### Pull requests

For external contributions, every new branch shall require a pull request to review the changes before merging