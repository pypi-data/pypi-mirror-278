import rustfs
import tempfile
import os

DEFAULT_REMOTE_DIR = "s3://my-s3-bucket/test"
fs = rustfs.RustS3FileSystem()
temp_dir = tempfile.TemporaryDirectory()
file_name = "file.txt"
downloaded_file_name = "file_download.txt"


def create_file(size_mb: int):
    print("creating a file...")
    file_path = os.path.join(temp_dir.name, file_name)
    with open(file_path, "w") as f:
        f.write(str(os.urandom(size_mb * 1024 * 1024)))


def upload_file() -> str:
    file_path = os.path.join(temp_dir.name, file_name)
    remote_path = f"{DEFAULT_REMOTE_DIR}/{file_name}"
    print("uploading a file...")
    fs.put(file_path, remote_path)


def download_file():
    remote_path = f"{DEFAULT_REMOTE_DIR}/{file_name}"
    file_path = os.path.join(temp_dir.name, downloaded_file_name)
    print("downloading a file...")
    fs.get(remote_path, file_path)


def check_file_equality(file1, file2):
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            # check if the files are equal
            return f1.read() == f2.read()


if __name__ == "__main__":
    create_file(1000)
    upload_file()
    download_file()
    if check_file_equality(
        os.path.join(temp_dir.name, file_name),
        os.path.join(temp_dir.name, downloaded_file_name),
    ):
        print("Files are equal")
    else:
        print("Files are not equal")
    temp_dir.cleanup()
