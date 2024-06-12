# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import os
import urllib.request
import hashlib
from drawlib.v0_1.private.logging import logger


def download_if_not_exist(file_path: str, download_url: str, md5_hash: str):

    def is_file_exist():
        return os.path.exists(file_path)

    def is_checksum_correct():
        md5_hash2 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash2.update(chunk)

        return md5_hash2.hexdigest().lower() == md5_hash.strip().lower()

    def download():
        try:
            with urllib.request.urlopen(download_url) as response:
                # create parent directory
                directory = os.path.dirname(file_path)
                os.makedirs(directory, exist_ok=True)

                # save file
                with open(file_path, "wb") as fout:
                    data = response.read()
                    fout.write(data)

        except Exception as e:
            raise RuntimeError(f"File download error happens. {str(e)}")

    # if file exist and checksum ok, do nothing
    if is_file_exist():
        if is_checksum_correct():
            return

    # if file not exist or checksum has problem, try download
    logger.info(f'No font on local machine. Downloading from "{download_url}".')
    download()

    # after download, check file exist and checksum
    if not is_file_exist():
        raise RuntimeError("File download completed. But not saved. Abort.")
    if not is_checksum_correct():
        raise RuntimeError("File download completed. But checksum has problem. Abort.")
    logger.info("Download completed without troubles.")
