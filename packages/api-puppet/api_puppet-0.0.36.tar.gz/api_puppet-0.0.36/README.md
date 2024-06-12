# api-puppet Python package

This is an Python framework to accelerate REST API wrapper development.

## Deployment

The doc comes mostly from [Pypi](https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml) 
and with some references to [Microsoft](https://learn.microsoft.com/en-us/azure/devops/artifacts/quickstarts/python-cli?view=azure-devops)

To build the package: start by making sure to increment the version value in the pyproject.toml file. Then,
remove the files in the /dist directory:

On Windows:
```shell
$ rmdir /s /q dist
```
On Mac:
```shell
$ rm -rf dist
```

Then you can build the new version:

```shell
$ python3 -m pip install --upgrade build
$ python3 -m build
```

To push to Azure DevOps artefacts feed:
```shell
$ python3 -m twine upload --repository-url https://pkgs.dev.azure.com/ventrilochub/_packaging/ventriloctoolkit/pypi/upload dist/*
```

You will be prompted to enter your credentials.

