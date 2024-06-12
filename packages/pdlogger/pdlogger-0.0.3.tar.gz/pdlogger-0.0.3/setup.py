from setuptools import setup, find_packages

setup(
    name="pdlogger",
    version="0.0.3",
    packages=find_packages(),
    install_requires=["streamlit==1.23.0","PyPika==0.48.9","pandas==1.1.5","mysql-connector-python==8.0.33","pika==0.13.0"],
    author="parallelldots",
    author_email="dsteam-wiki@paralleldots.com",
    description="An example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://bitbucket.org/paralleldots/pdlogger/src/main/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
