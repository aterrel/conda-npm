# conda-npm
run conda like npm

## Use case:
- you want to use conda to manage your python environment
- you want to add packages as you develop
- you want to save your packages without having to run `conda env export > environment.yml` every time you add a package
- you want to use `conda install` to install packages from your `environment.yml` file
- you want to share your environment with others

## Plan:

```shell
conda npm install <package>
```
- add package to environment.yml
- resolve dependencies with noarch or your platform
- rewrite conda lock file
- install in environment