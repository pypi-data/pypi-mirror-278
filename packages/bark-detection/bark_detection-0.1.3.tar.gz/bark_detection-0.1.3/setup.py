from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = 'Package for bark detection in audio file'

# Setting up
setup(
    name="bark_detection",
    version=VERSION,
    author="jgab",
    #author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    package_data={'bark_detection': ['model/model.json','model/model.h5']},
    install_requires=['librosa==0.10.1','tensorflow==2.13.0','matplotlib==3.7.2','pandas==2.1.1','numpy==1.24.3','tensorflow-io-gcs-filesystem==0.34.0'],
    keywords=['python', 'ML', 'bark', 'detection'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
    ]
)