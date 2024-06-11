import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kbot-py-client",
    version="1.0.5",
    author="Konverso",
    author_email="contact@konverso.ai",
    description="Client for Konverso Kbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.konverso.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
