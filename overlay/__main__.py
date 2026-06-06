from overlay.controller import run


def main():
    run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl+C received — shutting down...")
