from setuptools import setup, find_packages

setup(
    name="cucumber_s",
    version="0.1.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for creating various programs based on objectives",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python_library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'create-python-file=cucumber_s.library:create_python_file',
        ],
    },
)
