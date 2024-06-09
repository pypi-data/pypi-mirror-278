from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='dramacool',
    version='0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dramacool=dramacool.main:drama',
        ],
    },
    install_requires=[
        # List your package dependencies here
        'requests',
        'beautifulsoup4',
        'yt-dlp',
        'aria2',
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
