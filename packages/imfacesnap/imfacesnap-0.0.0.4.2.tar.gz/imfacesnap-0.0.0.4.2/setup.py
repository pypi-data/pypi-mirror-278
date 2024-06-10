from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
import gdown
import os


def get_deepface_home():
    """Get the home directory for storing weights and models.

    Returns:
        str: the home directory.
    """
    os.environ.setdefault("DEEPFACE_HOME", "/app") # This LINE cause error when we try to install in local environment, because APP folder is not initialized
    return str(os.getenv("DEEPFACE_HOME", default=str(Path.home())))

def initialize_folder():
    """Initialize the folder for storing weights and models.

    Raises:
        OSError: if the folder cannot be created.
    """
    home = get_deepface_home()
    deepface_homepath = home + "/.deepface"
    weights_path = deepface_homepath + "/weights"

    if not os.path.exists(deepface_homepath):
        os.makedirs(deepface_homepath, exist_ok=True)
        print("Directory ", home, "/.deepface created")

    if not os.path.exists(weights_path):
        os.makedirs(weights_path, exist_ok=True)
        print("Directory ", home, "/.deepface/weights created")



home_dir = get_deepface_home()
def download_weights():
    #url of the weights that need to be downloaded first
    facenet512_url = "https://github.com/serengil/deepface_models/releases/download/v1.0/facenet512_weights.h5"
    yolov8_url = "https://drive.google.com/uc?id=1UX8saXoKt36H9uMsZIPJt4jk3NoDvNTL"
    #path of the weights will be saved
    facenet512_weight_path = str(home_dir) + "/.deepface/weights/facenet512_weights.h5"
    yolov8_weight_path = str(home_dir) +"/.deepface/weights/yolov8m-face.onnx"
    
    if os.path.isfile(facenet512_weight_path) != True:
        print("facenet512_weights.h5 will be downloaded...")
        gdown.download(facenet512_url, facenet512_weight_path, quiet=False)

    if os.path.isfile(yolov8_weight_path) != True:
        print("yolov8 onnx will be downloaded...")
        gdown.download(yolov8_url, yolov8_weight_path, quiet=False)
        
class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        initialize_folder()
        download_weights()

with open("README.md", "r") as file:
    description = file.read()

requirements = ["deepfacesnap==0.0.2"]

setup(
    name='imfacesnap',
    version='0.0.0.4.2',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["imfacesnap=imfacesnap.main:main"]},
    author="Kevin Snap",
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5.5",
    cmdclass={
        'install': CustomInstallCommand,
    },
)