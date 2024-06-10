import io
import re
from setuptools import setup, find_packages

from agi_med_utils import __version__


def read(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


readme = read('README.md')
# вычищаем локальные версии из файла requirements (согласно PEP440)
requirements = '\n'.join(
    re.findall(
        r'^([^\s^+]+).*$',
        read('requirements.txt'),
        flags=re.MULTILINE,
    )
)

setup(
    # metadata
    name='agi_med_utils',
    version=__version__,
    author='AGI-MED-TEAM',
    description='Utils for agi-med team',
    long_description=readme,
    # options
    packages=find_packages(),
    install_requires='\n'.join([requirements]),
    include_package_data=True,
)
