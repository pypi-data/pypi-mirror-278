from setuptools import setup, find_packages

setup(
    name= "duyll",
    version= "0.5",
    packages=["duyll/basicsr/data", 
              "duyll/basicsr/utils",
              "duyll/basicsr/models",
              "duyll/pretrained_weights",
              "duyll",
              ],
    install_requires=[]

)