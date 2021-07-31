"""
Name    : utils.py.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 31.07.2021 20:05
Desc    : 
"""
from pathlib import Path
import pandas as pd

def loadTableFile(fpath: Path):
    '''
    Loads the table provided with the filepath and perform check if PatientID is found in the headers.
    (Fallback to 1th row for subject id)
    :param fpath: Source path for the table (csv) to be loaded
    :return:
    '''
    try:
        filepath = fpath
        df = pd.read_csv(filepath, sep=';', decimal=',', header=0)

        if "PatientID" not in df.columns.values:
            # If PatientID is not found in headers, select the 1th row as Patient Identifier!
            new_header = list(df.columns.values)
            new_header[0] = "PatientID"
            df.columns = new_header
        return df

    except ValueError:
        return None


def evaluateProvidedTable(fname):
    out = loadTableFile(fname)
    if isinstance(out, pd.DataFrame):
        print("Building Table Window!")
        return True
    else:
        return False