## How to publish the package to PYPI?

Install dependencies:

```
pip install -r requirements.txt
```

Run this command to build the package:

```
python3 setup.py sdist bdist_wheel
```

Then, run this command to publish it:

```
twine upload dist/*
```
or
```
python3 -m twine upload dist/*
```

On MacOS 14, pip install throws error: externally-managed-environment:
https://discuss.python.org/t/on-macos-14-pip-install-throws-error-externally-managed-environment/50352/6
