import datetime
import os
import tempfile
import rustfs

DEFAULT_REMOTE_DIR = "s3://union-cloud-oc-staging-dogfood/test"
DEFAULT_REMOTE_PATH = f"{DEFAULT_REMOTE_DIR}/file2.txt"
fs = rustfs.RustS3FileSystem()


def upload_file(size_mb: int) -> str:
    temp_dir = tempfile.TemporaryDirectory()
    file_path = os.path.join(temp_dir.name, "file_upload.txt")
    with open(file_path, "w") as f:
        f.write(str(os.urandom(size_mb * 1024 * 1024)))
    remote_path = DEFAULT_REMOTE_PATH
    print("uploading a file...")
    fs.put(file_path, remote_path)
    temp_dir.cleanup()
    return remote_path


def download_file(remote_path: str):
    temp_dir = tempfile.TemporaryDirectory()
    file_path = os.path.join(temp_dir.name, "file_download.txt")
    print("downloading a file...")
    fs.get(remote_path, file_path)
    temp_dir.cleanup()


def upload_directory(num_files: int, size_mb: int):
    temp_dir = tempfile.TemporaryDirectory()
    for i in range(num_files):
        file_path = os.path.join(temp_dir.name, f"file_{i}.txt")
        with open(file_path, "w") as f:
            f.write(str(os.urandom(size_mb * 1024 * 1024)))
    print("uploading a directory...")
    fs.put(temp_dir.name, DEFAULT_REMOTE_DIR, True)
    temp_dir.cleanup()


def download_directory(remote_dir: str):
    temp_dir = tempfile.TemporaryDirectory()
    print("downloading a directory...")
    fs.get(remote_dir, temp_dir.name, True)
    temp_dir.cleanup()


if __name__ == "__main__":
    # upload
    start_upload = datetime.datetime.now()
    remote_path = upload_file(size_mb=1)
    end_upload = datetime.datetime.now()
    print(f"Upload time taken: {end_upload - start_upload}")

    # download
    start_download = datetime.datetime.now()
    download_file(remote_path=remote_path)
    end_download = datetime.datetime.now()
    print(f"Download time taken: {end_download - start_download}")

    # upload directory
    start_upload_dir = datetime.datetime.now()
    upload_directory(num_files=2, size_mb=1)
    end_upload_dir = datetime.datetime.now()
    print(f"Upload directory time taken: {end_upload_dir - start_upload_dir}")

    # download directory
    start_download_dir = datetime.datetime.now()
    download_directory(remote_dir=DEFAULT_REMOTE_DIR)
    end_download_dir = datetime.datetime.now()
    print(f"Download directory time taken: {end_download_dir - start_download_dir}")
