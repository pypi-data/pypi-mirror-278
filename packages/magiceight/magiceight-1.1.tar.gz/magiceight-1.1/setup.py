from setuptools import setup


with open("README.md", 'r') as readme:
    long_description = readme.read()



setup(
    name="magiceight",
    version="1.1",
    description="A magic eight ball CLI program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LordUbuntu/MENACE",
    keywords=["python", "fortune", "magic eight ball", "eight ball"],
    license="MIT",
    author="Jacobus Burger",
    author_email="therealjacoburger@gmail.com",
    packages=["magiceight"],
    extras_require={
        "dev": ["pytest>=7.2", "twine>=4.0.2", "color50>=1.0.1"],
    },
    python_requires=">=3.10",
    platforms=["any"],
    py_modules=["magiceight"],
    entry_points={
        "console_scripts": ["magiceight=magiceight.__main__:main"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ]
)
