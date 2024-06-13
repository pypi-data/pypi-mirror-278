from setuptools import setup, find_packages

setup(
    name="django-nice-auth",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "django>=3.0",
        "requests",
        "pycryptodome",
        "nice_auth",
    ],
    author="RUNNERS",
    author_email="dev@runners.im",
    description="A Django app for NICE authentication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RUNNERS-IM/django-nice-auth",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
