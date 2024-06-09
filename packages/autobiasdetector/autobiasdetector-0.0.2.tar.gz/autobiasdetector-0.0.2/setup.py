import setuptools
import re
import requests
from bs4 import BeautifulSoup

package_name = "autobiasdetector"


def curr_version():
    # Obtain the version number from the official website
    url = f"https://test.pypi.org/project/{package_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    latest_version = soup.select_one(".release__version").text.strip()
    return str(latest_version)

def get_version():
    return '0.0.2'
    # Extract three numbers from the version number string and convert them to integer type
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", curr_version())
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))

    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    new_version_str = f"{major}.{minor}.{patch}"
    return new_version_str

def upload():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setuptools.setup(
        name=package_name,
        version=get_version(),
        author="Zhouhao Sun",
        author_email="zhsun@ir.hit.edu.cn",
        description="tools for detecting bias patterns of LLMs",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/autobiasdetector/",
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.10',
        install_requires=required,
    )

def write_now_version():
    print("Current VERSION:", get_version())
    with open("VERSION", "w") as version_f:
        version_f.write(get_version())

def main():
    try:
        upload()
        print("Upload success , Current VERSION:", curr_version())
    except Exception as e:
        raise Exception("Upload package error", e)

if __name__ == '__main__':
    main()
