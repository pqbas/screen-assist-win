from setup.installation.seb import install_seb
from setup.installation.patch import install_patch


def run(autopilot: bool):
    """
    Runs the installation process for Patching Safe Exam Browser.
    """

    install_seb(autopilot)
    install_patch(autopilot)
