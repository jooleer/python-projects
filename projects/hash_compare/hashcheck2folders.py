import hashlib
import os

def get_hash_value(folder):
  """Gets the hash value of all files in a folder.

  Args:
    folder: The path to the folder.

  Returns:
    A dictionary mapping file paths to their hash values.
  """
  hash_values = {}
  for root, directories, files in os.walk(folder):
    for file in files:
      full_path = os.path.join(root, file)
      with open(full_path, "rb") as f:
        hash_value = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b""):
          hash_value.update(chunk)
        hash_values[full_path] = hash_value.hexdigest()
  return hash_values

def compare_hash_values(folder1, folder2):
  """Compares the hash values of two folders.

  Args:
    folder1: The path to the first folder.
    folder2: The path to the second folder.

  Returns:
    True if the hash values of the two folders are identical, False otherwise.
  """
  hash_values1 = get_hash_value(folder1)
  hash_values2 = get_hash_value(folder2)
  if hash_values1 == hash_values2:
    return True
  else:
    return False