from setup.utils import generate_download_path, load_config, download_github_source


def download_seb():
    """
    Downloads a compatible version of Safe Exam Browser.
    """

    config = load_config()

    target_file_path = generate_download_path(config["seb"]["name"])
    seb_version = config["seb"]["version"]
    target_url = config["seb"]["url"]

    print()
    choice = input(f"Do you agree to downloading and installing Safe Exam Browser {seb_version}? (y/n): ")
    if choice.lower() not in ["y", "yes"]:
        print()
        print("SEB installation cancelled by user.")
        return

    with open(target_file_path, "wb") as file:
        file.write(b"")

    print()
    download_github_source(target_url, str(target_file_path))
