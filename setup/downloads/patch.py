from setup.utils import load_config, download_github_source, generate_download_path


def download_patch(autopilot: bool):
    """
    Downloads the latest version of the patch.
    """

    config = load_config()

    patch_version = config["patch"]["version"]
    target_url = config["patch"]["url"]
    target_file_path = generate_download_path(config["patch"]["name"])

    print()
    if not autopilot and (input(
        f"Do you agree to downloading the SEB Patch {patch_version}? (y/n): ")
        .lower() not in ["y", "yes"]):
        print()
        print("Patch download cancelled by user.")
        return

    with open(target_file_path, "wb") as file:
        file.write(b"")

    print()
    download_github_source(target_url, target_file_path)
