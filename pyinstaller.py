import PyInstaller.__main__

if __name__ == "__main__":
    PyInstaller.__main__.run([
    "main.py",
    "--onefile",
    "--windowed",
    "--clean",
    "--icon",
    "Media\\logo.ico",
    "-n Tickets System"
    ])