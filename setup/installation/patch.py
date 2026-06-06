from setup.utils import load_config, generate_download_path, pause, run_exe


def install_patch():
    """
    Installs the patch for Safe Exam Browser.
    """

    config = load_config()

    target_file_path = generate_download_path(config["patch"]["name"])
    if not target_file_path.exists():
        print()
        print("Patch installation cancelled, setup not found.")
        return

    print()
    choice = input(f"Do you agree to installing the SEB Patch {config['patch']['version']}? (y/n): ")
    if choice.lower() not in ["y", "yes"]:
        print()
        print("Patch installation cancelled by user.")
        return

    print()
    print(f"Windows might ask you for permission for the setup to run. Proceed with it.")
    print(f"Click on 'PATCH' button on the popup that appears next.")
    print(f"After clicking on 'PATCH', close that popup and continue with this terminal.")
    print()
    pause()
    run_exe(target_file_path, elevated=True)
