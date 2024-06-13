from setuptools import setup, find_packages

#with open("README.md", "r", encoding="utf-8") as fh:
#    long_description = fh.read()

setup(
    name='CTkSuggestions',
    version='0.2.1',
    author='Cadam',
    description='CTkSuggestions implements a suggestion dropdown for a customtkinter widget',
    #long_description=long_description,
    #long_description_content_type='text/markdown',
    url='https://github.com/CadamTechnology/CTkSuggestions',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'customtkinter',
    ],
)


