from setuptools import setup 

setup(     
    name="gdrive_ipynb_import",
    version="2024.11.26.03",
    python_requires=">=3.6",
    py_modules=["gdrive_ipynb_import"],
    install_requires=['pydrive2','google','oauth2client'],
)
