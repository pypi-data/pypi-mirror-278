from setuptools import setup

setup(
    name="malh",
    version="0.0.1",
    py_modules=["main"],
    author="Ваше Имя",
    author_email="ваш_email@example.com",
    description="Краткое описание вашего пакета",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ваш_пользователь_на_github/my_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)