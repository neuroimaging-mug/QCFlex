# QCFlex: A flexible quality control tool for large MRI cohorts

---

This project was tested with python version 3.9.5, with the requirements being distributed in the _requirements.txt_ file.

In order to quickly setup a development environment, install venv from an installed version of Python 3.9.5 with 

Install virtualenv from pip
>  python3 -m venv <_ENVIRONMENT_NAME_>

On windows activate the installed environment by 
>  <_ENVIRONMENT_NAME_>\Scripts\activate 

and install all dependencies with 
> pip install -r requirements.txt

*Happy Coding!*

## Building Release
In order to distribute this project as an executable, run in the root folder of the repository:
> python setup.py bdist

Avoid running the build process in an Anaconda environment to keep the package size as small as possible!

![grafik](https://user-images.githubusercontent.com/67055436/115269796-f45fe600-a13b-11eb-8222-ce6f6709102a.png)

