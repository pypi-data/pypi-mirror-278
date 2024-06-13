from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='pycalc_permission',
    version='0.0.1',
    author='AE',
    author_email='AlekseevE2015@yandex.ru',
    description='A PyCalc permission package',
    long_description=readme(),
    long_description_content_type='text/markdown',
    # url='your_url',
    packages=find_packages(),
    install_requires=['Django>=5.0.6', 'djangorestframework>=3.15.1', 'PyJWT>=2.8.0'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='PyCalc ',
    # project_urls={
    #   'GitHub': 'your_github'
    # },
    python_requires='>=3.8'
)
