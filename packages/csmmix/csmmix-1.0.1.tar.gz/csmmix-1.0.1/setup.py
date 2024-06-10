from setuptools import setup, find_packages

setup(
    name='csmmix',
    version='1.0.1',
    author='Qiang Ren',
    author_email='690799557@qq.com',
    description='A plug-and-play label-invariant mixup method  that  achieves  data  augmentation  by  mixing  class-specific  magnitude',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rqfzpy/csmmix',
    packages=find_packages(),
    install_requires=[
        'torch',  # Add torch as a dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add more classifiers as needed
    ],
)
