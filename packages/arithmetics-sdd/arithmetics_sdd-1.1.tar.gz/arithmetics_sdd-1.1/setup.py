from setuptools import setup, find_packages

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="arithmetics_sdd",
    version="1.01",
    author="Shayem Quazi",
    url="https://github.com/Shayem1/Understanding-Arithmetics-Interactive-Experience",
    description="This program is designed to develop basic arithmetic skills",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "pyttsx3",
        "Pillow",
    ],
    entry_points={
        "gui_scripts": [
            "arithmetics-ctk = arithmetics_sdd.main:main"
        ]
    },
    classifiers=[
        "Topic :: Multimedia",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Games/Entertainment"
    ]
)