from setuptools import setup, find_packages

with open('README.rst', 'r',encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='galmoss',
    version='2.0.10',
    description='A Python-based, Torch-powered tool for two-dimensional fitting of galaxy profiles. By seamlessly enabling GPU parallelization, GalMOSS meets the high computational demands of large-scale galaxy surveys.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/Chenmi0619/GALMoss',
    keywords=['Astronomy data analysis', 'Astronomy toolbox', 'Galaxy profile fitting'],
    author='Chen Mi',
    author_email='chenmiastro@gmail.com',
    classifiers=[
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.9",
    packages=find_packages(),
)

