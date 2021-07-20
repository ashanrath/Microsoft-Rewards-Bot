import os
import zipfile
import requests

def update_driver():
    '''
    Auto deletes Chrome driver to ensure no errors - this forces an autoupdate of chrome drivers. There is probably a more efficient way of doing this.
    '''
    os.remove("drivers/chromedriver.exe")

def download_driver(driver_path, system):
    # determine latest chromedriver version
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    r = requests.get(url)
    latest_version = r.text
    if system == "Windows":
        url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(
            latest_version)
    elif system == "Darwin":
        url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_mac64.zip".format(
            latest_version)
    elif system == "Linux":
        url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip".format(
            latest_version)

    response = requests.get(url, stream=True)
    zip_file_path = os.path.join(os.path.dirname(
        driver_path), os.path.basename(url))
    with open(zip_file_path, "wb") as handle:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep alive chunks
                handle.write(chunk)
    extracted_dir = os.path.splitext(zip_file_path)[0]
    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(extracted_dir)
    os.remove(zip_file_path)

    driver = os.listdir(extracted_dir)[0]
    os.rename(os.path.join(extracted_dir, driver), driver_path)
    os.rmdir(extracted_dir)

    os.chmod(driver_path, 0o755)
    # way to note which chromedriver version is installed
    open(os.path.join(os.path.dirname(driver_path),
                      "{}.txt".format(latest_version)), "w").close()
