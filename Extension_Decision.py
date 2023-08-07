 # Run scoring script on file extension detection

import pathlib
import subprocess

# function to return the file extension

file_extension = pathlib.Path('/Users/otema/ReginaOdoi.csv').suffix
print("File Extension: ", file_extension)


# Run the other scripts

if file_extension == '.csv':
    subprocess.run(["python", "CSVeditingLoanDecisioning.py"])
    print("Done")
    
elif file_extension == '.pdf'::
    subprocess.run(["python", "processpdf.py"])
    print("Submitted")
