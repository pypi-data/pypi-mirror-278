from setuptools import setup, find_packages
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xml2dcm',
    version='0.0.6',
    description='Packages to convert XML files to DICOM format written by SNUH VitalLab ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='seunghojun',
    author_email='danuri.jun@gmail.com',
    url='https://github.com/SeungHoJUN/XML2DCM',
    install_requires=['pybase64', 'xml-python', 'numpy', 'pydicom', 'datetime', 'traceback2'],
    keywords=['xml2dcm', 'XML', 'DICOM', 'ECG DICOM', 'SNUH'],
    python_requires='>=3.11',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)