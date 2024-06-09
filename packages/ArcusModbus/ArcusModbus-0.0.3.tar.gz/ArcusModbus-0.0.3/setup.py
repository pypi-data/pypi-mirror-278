from setuptools import setup, find_packages

setup(
    name="ArcusModbus",
    version='0.0.3',
    author='Daniel Curtis',
    author_email='dwc00012@mix.wvu.edu',
    description='Titan IMX servo controller',
    long_description='Package for controlling Arcus Titan IMX servos over Ethernet using Modbus TCP',
    py_modules=['ArcusModbus'],
    keywords=[
        'python',
        'Arcus Titan IMX'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows'
    ]

)