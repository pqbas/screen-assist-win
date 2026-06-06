import setup.downloads.controller
import setup.installation.controller


def run():
    """
    Runs the setup process for Patching Safe Exam Browser.
    """

    # Download Safe Exam Browser
    # Download Patch exe
    # Run Patch exe
    # Create a shortcut on the user's desktop for the patched thingy
    # Give them instructions on how to use it

    print()
    print("---------- SEB PATCH SETUP ----------")
    print()
    choice = input("Do you want to patch SEB? (y/n): ")
    if choice.lower() not in ["y", "yes"]:
        print()
        print("Setup cancelled by user.")
        return

    print()
    print("Handling control over to downloads.controller...")
    setup.downloads.controller.run()

    print()
    print("Handling control over to installation.controller...")
    setup.installation.controller.run()

    print()
    print("Setup completed successfully!")
    print()
    print("USAGE INSTRUCTIONS:")
    print("- A program with SEB icon and a configuration file has been added to your desktop.")
    print("- Everytime before opening SEB, or any link that opens in SEB, you have to double click and open that icon first.")
    print("- The overlay will automatically activate when SEB is on the screen.")
