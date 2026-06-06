from setup.installation.seb import install_seb
from setup.installation.patch import install_patch


def run():
    """
    Runs the installation process for Patching Safe Exam Browser.
    """

    install_seb()
    install_patch()
