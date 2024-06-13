from setuptools import setup, find_packages
from setuptools import setup, find_packages
import setuptools
import subprocess
import sys

def install_conda_packages():
    try:
        # List of conda packages with channels
        conda_packages = [
            "pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia",
        ]
        
        # Install each conda package
        for package in conda_packages:
            subprocess.check_call(f"conda install -y {package}", shell=True)
            
    except subprocess.CalledProcessError as e:
        sys.exit(f"Conda package installation failed: {e}")

class CondaInstallCommand(setuptools.Command):
    """A custom command to run conda install."""
    description = 'Install conda packages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        install_conda_packages()

setup(
    name= "duyll",
    version= "0.5.4",
    packages=["duyll/basicsr/data", 
              "duyll/basicsr/utils",
              "duyll/basicsr/models",
              "duyll/pretrained_weights",
              "duyll/basicsr/models/archs",
              "duyll/basicsr/models/losses",
              "duyll",
              ],
    install_requires=[
          "matplotlib", "scikit-learn", "scikit-image", "opencv-python", "yacs", "joblib",
           "natsort", "h5py", "tqdm", "tensorboard", "einops", "gdown", "addict", "future", "lmdb",
            "numpy", "pyyaml", "requests", "scipy", "yapf", "lpips", "thop", "timm"
      ],
      cmdclass={
        'install_conda': CondaInstallCommand,
    }

)