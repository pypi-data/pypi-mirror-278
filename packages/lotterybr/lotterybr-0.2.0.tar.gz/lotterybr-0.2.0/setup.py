from setuptools import setup, find_packages


with open("README.md") as f:
    README = f.read()

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Database",
    "Topic :: Internet"
]

REQUIREMENTS = [
    'pandas',
    'pyreadr',
    'shiny',
    'shinywidgets',
    'plotly',
    'numpy',
]

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/salvnetto/lotterybr-py/issues",
    "Documentation": "https://salvnetto.github.io/lotterybr-py",
    "Source Code": "https://github.com/salvnetto/lotterybr-py",
}

setup(
    name='lotterybr',
    version='0.2.0',
    description= "A collection of functions designed to streamline the retrieval of data from Brazilian lottery games operated by Caixa Econômica Federal, accessible through the official website at <https://loterias.caixa.gov.br/Paginas/default.aspx/>.",
    packages= find_packages(),
    long_description= README,
    long_description_content_type= "text/markdown",
    url= "https://github.com/salvnetto/lotterybr-py",
    author= "Salvador Netto, Tomas Bernardes, Fabio Demarqui",
    author_email= "salvnetto@ufmg.br, tomasbp@ufmg.br, fndemarqui@est.ufmg.br",
    license= "MIT",
    platforms="any",
    classifiers= CLASSIFIERS,
    install_requires= REQUIREMENTS,
    zip_safe=False,
    python_requires='>3.5',
    project_urls=PROJECT_URLS,
        
)