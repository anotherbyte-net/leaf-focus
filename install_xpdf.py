"""Download and extract the xpdf tools."""

from __future__ import annotations

import argparse
import dataclasses
import logging
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

logging.basicConfig(
    format="%(asctime)s [%(levelname)-8s] %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class XpdfInstallArgs:
    """Arguments for xpdf install command."""

    download_dir: pathlib.Path
    """path to the download dir"""

    install_dir: pathlib.Path
    """path to the installation dir"""

    gpg_key_url: str
    """url to the gpg key file"""

    file_sig_url: str
    """url to the signature file"""

    file_comp_url: str
    """url to the compress file containing the xpdf binaries"""


class XpdfInstall:
    """Install the xpdf tools."""

    def __init__(self, xpdf_install_args: XpdfInstallArgs) -> None:
        """Create a new instance of the xpdf install class."""
        self._xpdf_install_args = xpdf_install_args

    def run(self) -> bool:
        """Download the xpdf files and extract."""
        logger.info("Downloading and installing xpdf tools.")

        download_dir = self._xpdf_install_args.download_dir.absolute()
        download_dir.mkdir(parents=True, exist_ok=True)

        install_dir = self._xpdf_install_args.install_dir.absolute()
        install_dir.mkdir(parents=True, exist_ok=True)

        gpg_key_url = self._xpdf_install_args.gpg_key_url
        file_sig_url = self._xpdf_install_args.file_sig_url
        file_comp_url = self._xpdf_install_args.file_comp_url

        available_urls = [gpg_key_url, file_sig_url, file_comp_url]

        # downloaded file names
        gpg_key_name = self._get_url_file_name(gpg_key_url)
        gpg_key_path = download_dir / gpg_key_name

        file_sig_name = self._get_url_file_name(file_sig_url)
        file_sig_path = download_dir / file_sig_name

        file_comp_name = self._get_url_file_name(file_comp_url)
        file_comp_path = download_dir / file_comp_name

        available_paths = [gpg_key_path, file_sig_path, file_comp_path]

        # if the download dir contains more than the 3 expected files,
        # delete the download dir
        download_dir_files = {i.name for i in download_dir.iterdir() if i.is_file()}
        expected_files = {i.name for i in available_paths}
        if download_dir.exists() and download_dir_files != expected_files:
            logger.warning("Deleting download directory.")
            shutil.rmtree(download_dir, ignore_errors=True)

        # re-create the installation dir
        shutil.rmtree(install_dir, ignore_errors=True)
        install_dir.mkdir(parents=True, exist_ok=True)

        # ensure download folder is created
        download_dir.mkdir(parents=True, exist_ok=True)

        # download any missing files
        for file_url, file_path in zip(available_urls, available_paths):
            if not file_path.exists():
                logger.info("Downloading '%s'.", file_url)
                self._download_file(file_url, file_path)

        # verify the downloaded files
        verify_result = self._gpg_verify(gpg_key_path, file_sig_path, file_comp_path)
        if verify_result is not True:
            return False

        # extract the compared file to the installation dir
        logger.info("Extracting '%s' to '%s'.", file_comp_path, install_dir)
        if file_comp_path.suffixes[-2:] == [".tar", ".gz"]:
            compressed = tarfile.open(file_comp_path)
            compressed.extractall(install_dir)
            compressed.close()
        elif file_comp_path.suffixes[-1:] == [".zip"]:
            compressed = zipfile.ZipFile(file_comp_path)
            compressed.extractall(install_dir)
            compressed.close()
        else:
            msg = f"Cannot extract file '{file_comp_path}'."
            raise ValueError(msg)

        logger.info("Finished.")
        return True

    def _get_url_file_name(self, url: str) -> str:
        parsed_url = urlparse(url)
        path_only = parsed_url.path.split(";")[0]
        parsed_path = pathlib.Path(path_only)
        file_name = parsed_path.name
        return file_name

    def _download_file(self, file_url: str, file_path: pathlib.Path) -> None:
        if not file_url or not file_url.startswith("https"):
            msg = "Invalid file url: %s"
            raise ValueError(msg, file_url)

        r = urlopen(Request(file_url))
        try:
            with file_path.open("wb") as f:
                shutil.copyfileobj(r, f)
        finally:
            r.close()

    def _gpg_verify(
        self,
        key_path: pathlib.Path,
        sig_path: pathlib.Path,
        file_path: pathlib.Path,
    ) -> bool:
        expected_email = '"-Xpdf- <xpdf@xpdfreader.com>"'

        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir = pathlib.Path(temp_dir_name)
            temp_keyring = temp_dir / "temp_keyring"

            cmd = (
                r"C:\Program Files\Git\usr\bin\gpg.exe"
                if sys.platform.startswith("win32")
                else "gpg"
            )

            cmd_import = [
                cmd,
                "--no-default-keyring",
                "--keyring",
                self._path_to_str(temp_keyring),
                "--import",
                self._path_to_str(key_path),
            ]
            result_import = subprocess.run(cmd_import, capture_output=True)
            expected_import_return_codes = [0, 2]
            if result_import.returncode not in expected_import_return_codes:
                logger.warning("Unexpected return code '%s'.", result_import)
                # expecting return code 2 because there is no ultimately trusted key
                return False
            contains_email = [
                line
                for line in result_import.stderr.splitlines()
                if expected_email in line.decode()
            ]
            if len(contains_email) != 1:
                logger.warning("Unexpected stderr '%s'.", result_import)
                # gpg key must contain the expected email address
                return False

            cmd_verify = [
                cmd,
                "--no-default-keyring",
                "--keyring",
                self._path_to_str(temp_keyring),
                "--verify",
                self._path_to_str(sig_path),
                self._path_to_str(file_path),
            ]
            result_verify = subprocess.run(cmd_verify, capture_output=True)
            if result_verify.returncode != 0:
                logger.warning("Unexpected return code '%s'.", result_verify)
                # expecting status code 0
                return False
            contains_good_email = [
                line
                for line in result_verify.stderr.splitlines()
                if f"Good signature from {expected_email}" in line.decode()
            ]
            if len(contains_good_email) != 1:
                logger.warning("Unexpected stderr code '%s'.", result_verify)
                # must be a 'good' signature with the expected key
                return False

            return True

    def _path_to_str(self, path: pathlib.Path) -> str:
        posix_path = pathlib.PurePosixPath(path)
        str_path = str(posix_path).replace(":/", "/").replace(":\\/", "/")
        str_path = "/" + str_path[0].lower() + str_path[1:]
        return str_path


def main(args: list[str] | None = None) -> int:
    """Download and extract the xpdf tools."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="install-xpdf",
        description="Download and extract the xpdf tools.",
    )
    parser.add_argument(
        "--download-dir",
        type=pathlib.Path,
        required=True,
        help="path to the download dir",
    )
    parser.add_argument(
        "--install-dir",
        type=pathlib.Path,
        required=True,
        help="path to the installation dir",
    )
    parser.add_argument(
        "--gpg-key-url",
        required=True,
        help="url to the gpg key file",
    )
    parser.add_argument(
        "--file-sig-url",
        required=True,
        help="url to the signature file",
    )
    parser.add_argument(
        "--file-comp-url",
        required=True,
        help="url to the compress file containing the xpdf binaries",
    )

    parsed_args = parser.parse_args(args)

    xpdf_install_args = XpdfInstallArgs(
        download_dir=parsed_args.download_dir,
        install_dir=parsed_args.install_dir,
        gpg_key_url=parsed_args.gpg_key_url,
        file_sig_url=parsed_args.file_sig_url,
        file_comp_url=parsed_args.file_comp_url,
    )

    xpdf_install = XpdfInstall(xpdf_install_args)
    result = xpdf_install.run()

    return 0 if result is True else 1


if __name__ == "__main__":
    sys.exit(main())
