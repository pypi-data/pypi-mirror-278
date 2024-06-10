from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='DeGourou',
    version='1.3.9',    
    description='Automate the process of getting decrypted ebook from InternetArchive without the need for Adobe Digital Editions and Calibre.',
    url='https://gitea.com/bipinkrish/DeGourou',
    author='Bipin krishna',
    license='GPL3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['DeGourou',"DeGourou/setup","DeGourou/decrypt"],
    install_requires=['pycryptodomex>=3.17',
                      'cryptography>=41.0.1', 
                      'lxml>=4.9.2',
                      'requests>=2.31.0',
                      'charset-normalizer>=3.1.0'      
                      ],

    entry_points={
        'console_scripts': [
            'degourou = DeGourou.DeGourou:main'
        ]
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)