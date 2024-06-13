from setuptools import setup, find_packages

setup(
    name="wartsila_ai",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[], # requirements
    author="Abdelrahman Abounida",
    author_email="abdelrahman.abounida@wartsila.com",
    description="Useful tools for further development of AI projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AbdelrahmanAbounida/wartsila-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

#  python setup.py sdist bdist_wheel    
# twine upload  dist/*     