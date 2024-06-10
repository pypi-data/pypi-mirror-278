from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as fd:
    long_description = fd.read()

setup(
    name='Sae203_Arnaud',
    version='1.0.11',
    author="Arnaud G",
    url="https://etulab.univ-amu.fr/g23015097/sae203_python",
    author_email="arnaud.gaillard@etu.univ-amu.fr",
    description="Récupération d'un certain type de fux rss, affichage d'une synthèse sur une page web",
    long_description=long_description,
    long_description_content_type='text/markdown',
    readme="README.md",
    packages=find_packages(),
    package_data={
        'Sae203_Arnaud': ['data/*'],
    },
    python_requires=">=3.8",
    install_requires=[
        "requests >= 2.31.0",
        "feedparser >= 6.0.8",
        "pyyaml >= 6.0.1",
        "beautifulsoup4 >= 4.12.2",
        "pytz >= 2024.1",
        "click >= 8.1.7",
        "inquirer >= 3.2.4",
    ],
    entry_points={
        "console_scripts":[
            "aggreg = Sae203_Arnaud.cli:app"
        ]
    }
)
