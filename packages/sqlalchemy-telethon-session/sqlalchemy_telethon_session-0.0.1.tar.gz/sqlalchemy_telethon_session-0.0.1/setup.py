import setuptools

setuptools.setup(
    name="sqlalchemy-telethon-session",
    version="0.0.1",
    url="https://github.com/AI-Stratov/telethon-session-sqlalchemy",

    author="Tulir Asokan",
    author_email="tulir@maunium.net",

    description="SQLAlchemy backend for Telethon session storage",
    long_description=open("README.rst").read(),

    packages=setuptools.find_packages(),

    install_requires=[
        "SQLAlchemy>=2",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires="~=3.5",
)
