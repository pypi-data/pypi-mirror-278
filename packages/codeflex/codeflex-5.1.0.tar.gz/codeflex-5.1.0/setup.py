import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
  
setuptools.setup(
    name="codeflex",
    version="5.1.0", 
    author="CODEFLEX S.A.S.", 
    author_email="info@codeflex.com.co",
    license="This software is owned by CodeFlex S.A.S. and is protected by applicable copyright laws. The distribution and use of this software are subject to the terms and conditions outlined below.",
    description="¡Conecta a los Microservicios de CodeFlex desde una Sola Librería!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeflex.com.co/",
    project_urls={
        "Bug Tracker": "https://docs.codeflex.com.co/",
    },
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "idna", 
        "charset_normalizer",
        "chardet",
        "urllib3",
        "certifi",
        "werkzeug",
        "click",
        "blinker",
        "jinja2",
        "Flask",
        "itsdangerous"
    ]
)