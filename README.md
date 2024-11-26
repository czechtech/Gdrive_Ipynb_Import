# Gdrive_Ipynb_Import
Remote, in-memory import of Python (.py) &amp; Jupyter notebook files (.ipynb) from Google Drive

## Install:
```
pip install git+https://github.com/czechtech/Gdrive_Ipynb_Import.git
```

## Usage:
```
with gdrive_ipynb_import.file_url("https://colab.research.google.com/drive/some-file-id"):
  import your_notebook
```
The name of module on the import line (`your_notebook`) does not need to match the notebook file, it can be any name.

This is simlar to https://github.com/operatorequals/httpimport/
