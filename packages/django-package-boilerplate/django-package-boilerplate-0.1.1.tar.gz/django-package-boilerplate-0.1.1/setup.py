from setuptools import setup, find_packages

setup(
    name="django-package-boilerplate",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "django>=3.0",
        "requests",
    ],
    author="Runners Co., Ltd.",
    author_email="dev@runners.im",
    description="A boilerplate Django app package for easy integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RUNNERS-IM/django-package-boilerplate",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
