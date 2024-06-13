from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='drivepy',
    version='1.0.3',
    description='A tool for managing USB drives and flashing ISOs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://mrfidal.in/cyber-security/DrivePy',
    author='Fidal',
    author_email='mrfidal@proton.me',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'drivepy=drivepy.main:main',
        ],
    },
    python_requires='>=3.6',
)
