# Contributing

If you are in interested in this project and you would like to help developing some features (crawlers, visualization, minor fixes...), feel free to contact me (refer to the contact info on [my GitHub profile](https://github.com/albertosantagostino))

## "I know Python and I would love to help! What can I do?"

Writing crawlers is the most helpful thing you can do at the moment! The target to reach is one crawler for each Italian region (two for the weird Bolzano-Trento situation in Trentino-Alto Adige), so a total of **21 crawlers**!

A **crawler** in ITAQA is essentialy a function that downloads data from a specific region ARPA website/database/open data website and converts it into a single AQSC object. For more information you can contact me directly or check the implementation of existing crawlers ([Lombardia's crawler](https://github.com/albertosantagostino/ITAQA-air-quality-aggregator/blob/master/itaqa/crawler/lombardia.py))

In order to contribute, you need to:

* Fork ITAQA from the repository page (upper right corner)
* Clone the forked repository on your PC
* Sync the fork upstream with the original ITAQA repository, running:
  ```bash
  git remote add upstream https://github.com/albertosantagostino/ITAQA-air-quality-aggregator.git
  git fetch upstream
  git pull upstream master
  ```
* Create a branch for development (check guidelines below) using `git checkout -b <branch-name>`
* After you have pushed your changes and your branch, just **create a pull request** from your fork's page and wait for a review

## Development process

### General guidelines

* Be uniform with the existing code
* Avoid too many comments, write code that is readable using appropriate variable name
* Try to keep functions short (if possible)
* Keep the documentation up-to-date

### Technical information

**Formatter**

The formatter used is [**YAPF** (*Yet Another Python Formatter*)](https://github.com/google/yapf). It can be installed easily via pip: `pip3 install yapf`
To format all the files in the project, run `yapf -irp .` from the top project folder

**Branch names**

* The name of every development branch shall be coherent with the existing ones and will follow the nomenclature `module/specific_feature`
* All successive reworks/improvements to the same module should be indicated appending to the original branch name

### Workflow

#### Pull requests

* For external contributions, every new branch shall require a pull request to review the changes before merging