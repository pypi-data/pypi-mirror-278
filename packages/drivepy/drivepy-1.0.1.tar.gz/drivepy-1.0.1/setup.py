from setuptools import setup, find_packages

setup(
    name='drivepy',
    version='1.0.1',
    description='A tool for managing USB drives and flashing ISOs',
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
)
