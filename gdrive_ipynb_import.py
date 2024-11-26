# Python Google Drive API
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
# Google Authentication
from google.colab import auth
from oauth2client.client import GoogleCredentials
# Components of Python's import protocol
import importlib.abc
import importlib.util
# For ipynb interpretation
import nbformat


class Gdrive_Ipynb_Import(importlib.abc.MetaPathFinder, importlib.abc.Loader):
  def __init__(self, file_id):
    """Initializes the importer without establishing an oauth."""
    self.file_id = file_id

  def find_spec(self, fullname, path, target=None):
    """
    Access and load a google drive file.
    :param fullname: -ignored-
    :param path: -ignored-
    :param target: -ignored-
    :return: Module spec if found, otherwise None
    """
    # Only able to find a module if a file_id has been set
    if not self.file_id or self.file_id == "":
      #print("Gdrive_Importer: file_id is None")
      return None
    # Purge the file_id so a new one is set for the next import
    file_id = self.file_id
    self.file_id = None
    # Grab the contents of the google drive file
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    self.txt = GoogleDrive(gauth).CreateFile({"id": file_id}).GetContentString(f"{fullname}.py")
    # Create a spec for the module
    return importlib.util.spec_from_file_location(fullname, self.file_id, loader=self)

  def create_module(self, spec):
    """
    Optionally create a module object.
    :param spec: Module spec
    :return: Module object or None to use default behavior
    """
    return None  # Use the default module creation behavior

  def exec_module(self, module):
    """
    Execute the module code.
    :param module: Module object to execute code within
    """
    # ipynb:
    if '{"nbformat":' in self.txt:
      nb = nbformat.reads(self.txt, as_version=4)
      code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
      for cell in code_cells:
        exec(cell.source, module.__dict__)
    # otherwise, assume python
    else:
      exec(self.txt, module.__dict__)


import re

def parse_id_from_url(url):
  """
  Parse a google drive file's url for the file id
  :param url: Example: https://colab.research.google.com/drive/...
  """
  pattern = r"(?:(?:drive\..*d\/)|(?:drive\/))([\w-]+)"
  success = re.search(pattern, url)
  if success:
    file_id = success.group(1)
    return file_id
  else:
    return None


from contextlib import contextmanager
import sys

@contextmanager
def file_url(gdrive_file_url):
  """
  ...
  :param gdrive_file_url: ...
  This will commandeer Python's import mechanism for the next import
  """
  # Parse the url
  file_id = parse_id_from_url(gdrive_file_url)
  if not file_id:
    raise ModuleNotFoundError(f"Could not parse file id from: {url}")
  # Create the makeshift importer
  importer = Gdrive_Ipynb_Import(file_id)
  # Insert the importer into the search path
  sys.meta_path.append(importer)
  # Attempt to use the importer...
  try:
    yield
  except ImportError as e:
    raise e
  finally:  # Now remove the module from the search path
    for importer in sys.meta_path:
      try:
        if importer.file_id:
          sys.meta_path.remove(importer)
          return True
      except AttributeError as e:
        pass
  return False
