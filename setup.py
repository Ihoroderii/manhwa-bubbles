from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="manhwa-bubbles",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for creating manhwa-style speech bubbles and narration boxes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/manhwa-bubbles",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Artistic Software",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=8.0.0",
    ],
    keywords="manhwa, comics, speech bubbles, graphics, PIL, drawing",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/manhwa-bubbles/issues",
        "Source": "https://github.com/yourusername/manhwa-bubbles",
    },
)