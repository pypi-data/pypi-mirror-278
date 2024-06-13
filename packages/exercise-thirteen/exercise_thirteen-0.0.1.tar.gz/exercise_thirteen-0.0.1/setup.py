from distutils.core import setup

setup(
    name            = 'exercise_thirteen',
    packages        = ['exercise_thirteen'],
    author          = 'alevellop',
    version         = '0.0.1',
    license         = 'MIT',
    description     = 'Library of simple mathematical operations',
    keywords        = ['mathematical', 'operations', 'addition', 'subtraction', 'multiplication', 'division'],
    install_requires= ['pytest'],
    classifiers     = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
)