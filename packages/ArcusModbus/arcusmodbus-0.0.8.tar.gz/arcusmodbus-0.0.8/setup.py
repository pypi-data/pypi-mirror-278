from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'Titan IMX servo controller'
LONG_DESCRIPTION = 'Package for controlling Arcus Titan IMX servos over Ethernet using Modbus TCP'


setup(
    name ="ArcusModbus",
    version=VERSION,
    author="Daniel Curtis",
    author_email = "dwc00012@mix.wvu.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    py_modules=['ArcusModbus'],
    install_requires=['pymodbus'],
    keywords=['python','Arcus Titan IMX'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3"
    ]
)