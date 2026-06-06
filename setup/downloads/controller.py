from setup.downloads.seb import download_seb
from setup.downloads.patch import download_patch


def run(autopilot: bool):
    """
    Runs the download process for Patching Safe Exam Browser.
    """

    download_seb(autopilot)
    download_patch(autopilot)
