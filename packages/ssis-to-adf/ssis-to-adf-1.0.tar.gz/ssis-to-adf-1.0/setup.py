from setuptools import setup, find_packages

setup(
    name='ssis-to-adf',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='Convert ssis to pyspark script',
    long_description=open('README.md').read(),  # assuming you have a README.md file
    url='https://github.com/PrakashDeloitte/ssis-to-adf',  # link to your project's repository
    author='Prakash Soni',
    author_email='prakasoni@deloitte.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license again
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',  # replace "X" as appropriate
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=3.2.0',  # adjust the version according to your project's requirements
        # add any other dependencies your project needs
    ],
)
