import os
from setuptools import setup


with open('install-requirements.txt', 'r') as install_reqf:
    install_req = [req.strip() for req in install_reqf]


def get_version():
    """Reading from a python module without importing it."""
    mod_dict = {}
    with open(os.path.join(os.path.dirname(__file__),
                           'hgext3rd', 'loggingmod', 'version.py')) as vf:
        exec(vf.read(), mod_dict)
    return mod_dict['version']


setup(
    name='hg-loggingmod',
    version=get_version(),
    author='Georges Racinet',
    author_email='georges.racinet@octobus.net',
    url='https://dev.heptapod.net/heptapod/hgext-loggingmod',
    description='Managing Mercurial logs with the '
    'standard Python logging module',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='hg mercurial',
    license='GPLv2+',
    packages=['hgext3rd', 'hgext3rd.loggingmod'],
    install_requires=install_req,
)
