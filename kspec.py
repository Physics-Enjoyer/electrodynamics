# import nbformat
# from glob import glob

# for file in glob("**/*.ipynb", recursive=True):
#     nb = nbformat.read(open(file), as_version=4)
#     nb["metadata"]["kernelspec"] = {
#         "name": "jbenv",
#         "display_name": "Python (jbenv)",
#         "language": "python"
#     }
#     nbformat.write(nb, open(file, "w"))


import nbformat
import os

# Path to your notebooks
directory = 'electrodynamics'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.ipynb'):
            path = os.path.join(root, file)
            print(f"Cleaning metadata for: {path}")
            
            # Load the notebook
            nb = nbformat.read(path, as_version=4)
            
            # Reset kernelspec to a generic default
            nb.metadata.kernelspec = {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
            
            # Save it back
            nbformat.write(nb, path)

print("Done! All notebooks updated to generic 'python3' kernel.")