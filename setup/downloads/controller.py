from setup.downloads.seb import download_seb
from setup.downloads.patch import download_patch


def run():
    """
    Runs the download process for Patching Safe Exam Browser.
    """

    download_seb()
    download_patch()
