from setuptools import setup, find_packages

# Nom du package PyPI ('pip install NAME')
NAME = "AAIT"

# Version du package PyPI
VERSION = "0.0.2.25"  # la version doit être supérieure à la précédente sinon la publication sera refusée

# Facultatif / Adaptable à souhait
AUTHOR = "Orange community"
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = "Advanced Artificial Intelligence Tools is a package meant to develop and enable advanced AI functionalities in Orange"
LICENSE = ""

# 'orange3 add-on' permet de rendre l'addon téléchargeable via l'interface addons d'Orange 
KEYWORDS = ["orange3 add-on",]

# Tous les packages python existants dans le projet
PACKAGES = find_packages()
PACKAGES = [pack for pack in PACKAGES if "orangecontrib" in pack]
print(PACKAGES)

# Fichiers additionnels aux fichiers .py (comme les icons ou des .ows)
PACKAGE_DATA = {
    "orangecontrib.AAIT.widgets": ["icons/*", "designer/*"],
    "orangecontrib.AAIT": ["tutorials/*"],
    # contenu du dossier 'icons' situé dans 'orangecontrib/hkh_bot/widgets'
}
# /!\ les noms de fichier 'orangecontrib.hkh_bot.widgets' doivent correspondre à l'arborescence

# Dépendances
INSTALL_REQUIRES = ["sentence-transformers==2.5.1", "gpt4all==2.7.0"]

# Spécifie le dossier contenant les widgets et le nom de section qu'aura l'addon sur Orange
ENTRY_POINTS = {
    "orange.widgets": (
        "Advanced Artificial Intelligence Tools = orangecontrib.AAIT.widgets",
    ),
    "orange.widgets.tutorials": (
        "AAIT Tutorials = orangecontrib.AAIT.tutorials",
    )
}
# /!\ les noms de fichier 'orangecontrib.hkh_bot.widgets' doivent correspondre à l'arborescence

NAMESPACE_PACKAGES = ["orangecontrib"]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      license=LICENSE,
      keywords=KEYWORDS,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      install_requires=INSTALL_REQUIRES,
      entry_points=ENTRY_POINTS,
      namespace_packages=NAMESPACE_PACKAGES,
      )
