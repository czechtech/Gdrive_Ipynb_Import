import setuptools
setuptools.setup(     
    name="gdrive_ipynb_import",
    version="2024.11.26.02",
    python_requires=">=3.6",
    py_modules=["gdrive_ipynb_import"],
    install_requires=['pydrive2','google','oauth2client','importlib','nbformat'],
)
