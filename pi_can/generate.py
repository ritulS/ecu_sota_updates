def main():
    with open("file.bin", "wb") as f:
        f.truncate(512 * 1024)


if __name__ == "__main__":
    main()
