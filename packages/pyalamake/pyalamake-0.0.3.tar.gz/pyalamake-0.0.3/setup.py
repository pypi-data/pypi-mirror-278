from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.3')
print('     setup: module :  pyalamake')

# @formatter:off
setup(
    description='generate Makefile using python description',
    keywords=['makefile', 'generation', 'python'],
    install_requires=[
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='pyalamake',
    packages=find_packages(include='./pyalamake*', ),
    include_package_data=True,
    exclude_package_data={'./pyalamake/lib': ['.gitignore']},
    version='0.0.3',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/pyalamake/src/master',
    download_url='https://bitbucket.org/arrizza-public/pyalamake/get/master.zip',
)
# @formatter:on

print('     setup: done')
