# Tracebloc package
This package is pre-requiste to run tracebloc jupyter notebook.


This package helps to create and start the experiment for training ML models in 
tracebloc environment.


# Deployment Steps

Pre Requisite - Make sure you have a PyPi account and have access to tracebloc-package and tracebloc-package-dev

### Step 1 - Clean up:

Delete the following folders if they exist

- dist
- tracebloc_package.egg-info
- tracebloc_package_dev.egg-info

### Step 2 - Update Config:

Update the following details in setup.py

- name
    - For Production: `tracebloc_package`
    - For Dev: `tracebloc_package-dev`
- url
    - For tracebloc_package use https://gitlab.com/tracebloc/tracebloc-py-package
    - For tracebloc_package-dev use https://gitlab.com/tracebloc/tracebloc-py-package/-/tree/dev
- version
    - As applicable

### Step 3 - Build and Upload:

```
pip install -r requirements.txt
python setup.py sdist
twine upload dist/*
    username: __token__
    password: <your auth token>
```

 