Test locally
===

```bash
$ python -m pip install -e .
```

Build new release
===

```bash
$ git checkout master
$ git merge develop --no-ff
$ git push
$ git tag vX.Y.Z
$ git push origin vX.Y.Z
```

- Publish a release on github.com

Follow instructions to build and publish to pypi
===

```bash
# Setup your ~/.pypirc
[distutils]
index-servers =
  tempyenv
  tempyenv-test

[tempyenv]
repository = https://upload.pypi.org/legacy/
username = xyz
password = xyz

[tempyenv-test]
repository = https://test.pypi.org/legacy/
username = xyz
password = xyz

# Build
$ python3 -m build
#$ python setup.py bdist_wheel --universal

# Upload
$ rm -f dist/*
$ twine upload --repository-url https://upload.pypi.org/legacy/ dist/tempyenv-*
```
