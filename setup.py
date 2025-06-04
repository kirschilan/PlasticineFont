from setuptools import setup, find_packages

setup(
    name="plasticinefont",
    version="0.0.1",
    description="Generate PNG images from plasticine-style letters",
    author="kirschilan",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "pygments",
        "olefile",
        "fs"
],
    include_package_data=True,  # Ensures data files (like images) are included
    entry_points={
        'console_scripts': [
            'string2png=plasticinefont.cli:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
