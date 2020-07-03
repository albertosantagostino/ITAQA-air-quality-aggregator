# Contributing

If you are in interested in this project and you would like to help developing some features (crawlers, visualization, minor fixes...), feel free to contact me (refer to the contact info on [my GitHub profile](https://github.com/albertosantagostino))

## Development process

### General guidelines

* Be uniform with the existing code
* Avoid too many comments, write code that is readable using appropriate variable name
* Try to keep functions short (if possible)
* Keep the documentation up-to-date

### Technical information

**Formatter**
The formatter used is [**YAPF** (*Yet Another Python Formatter*)](https://github.com/google/yapf). It can be installed easily via pip: `pip3 install yafp`
To format all the files in the project, run `yapf -ir .` from the top project folder

**Branch names**

* The name of every development branch shall be coherent with the existing ones and will follow the nomenclature `module/specific_feature`
* All successive reworks/improvements to the same module should be indicated appending to the original branch name

### Workflow

#### Pull requests

* For external contributions, every new branch shall require a pull request to review the changes before merging