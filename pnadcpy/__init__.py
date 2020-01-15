"""PNADC-Downloader
This little script set helps to download PNADC's microdata files.
"""

import ftplib
import os

import pandas as pd

from .read_dicio import get_dicio


__version__ = "0.1"


def get_ftp(server):
    ftp = ftplib.FTP(server)
    ftp.login()

    return ftp


def download_doc(ftp, ftp_path, docdir):
    if not os.path.exists(docdir):
        os.makedirs(docdir)

    # Change current working directory to ftp_path
    ftp.cwd(ftp_path)

    files = ftp.nlst(ftp_path)
    for file in files:
        filename = file.split("/")[-1]
        filename = os.path.join(docdir, filename)
        print(file, "-->", filename)
        with open(filename, "wb") as f:
            ftp.retrbinary("RETR " + file, f.write)


def download_data(ftp, ftp_path, year, datadir):
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    # Change current working directory to ftp_path
    ftp.cwd(ftp_path)

    files = ftp.nlst(str(year))
    q = 1
    for file in files:
        filename = os.path.join(datadir, f"{year}Q{q}.zip")
        print(year, q, file, "-->", filename)
        with open(filename, "wb") as f:
            ftp.retrbinary("RETR " + file, f.write)
        q += 1


def open_pnadc(file_path, dicio):
    data = pd.read_fwf(
        file_path,
        compression="zip",
        widths=dicio["width"],
        names=dicio["name"])
    return data
