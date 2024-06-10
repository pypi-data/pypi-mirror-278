import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).cwd()

VERSION = '0.0.0.12' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'zerodai' #Debe coincidir con el nombre de la carpeta 
AUTHOR = '0dAI' #Modificar con vuestros datos
AUTHOR_EMAIL = 'luijait@zerodai.com' #Modificar con vuestros datos
URL = 'https://github.com/luijait' #Modificar con vuestros datos

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'AI Models and Agent Structures Wrapper for particularly offensive cybersecurity and cyberintelligence by 0dAI Company' #Short description

LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    'beautifulsoup4==4.12.3',
    'google==3.0.0',
    'googlesearch-python==1.2.4',
    'openai==0.28.0',
    'requests==2.32.3'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)