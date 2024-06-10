# SharedKernel
this a shared kernel package

# Change Log
### Version 1.3.0
- Implement Sentry For Log Exceptions
### Version 1.2.0
- Implement Regex Masking
# Create Package
    py -m pip install --upgrade build
    py -m build
    cd dist
    py -m pip install --upgrade twine
    py -m twine upload dist/*

# Pypi
pip install sharedkernel
