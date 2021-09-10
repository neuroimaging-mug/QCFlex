"""
Name    : utils.py.py
Author  : Stefan Eggenreich
Contact : stefan.eggenreich@gmail.com
TIME    : 31.07.2021 20:05
Desc    : 
"""
from pathlib import Path
import pandas as pd
from settings import REQUIRED_TABLE_COLUMNS

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

        if "ID" not in df.columns.values:
            # If ID is not found in headers, select the 1th row as Patient Identifier!
            new_header = list(df.columns.values)
            #new_header[0] = "PatientID"
            #df.columns = new_header
        return df

    except ValueError:
        return None


def evaluateTableHeader(header):
    """Evaluate the table header if all required columns are defined!"""
    for key in REQUIRED_TABLE_COLUMNS:
        if key not in header:
            return False
    return True

def evaluateProvidedTable(fname):
    out = loadTableFile(fname)

    if isinstance(out, pd.DataFrame) and evaluateTableHeader(list(out.columns)):
        print("Building Table Window!")
        return True
    else:
        return False