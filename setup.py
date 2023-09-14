from setuptools import setup, find_packages, find_namespace_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

def version():
    from bframe import __version__
    return __version__

setup(
    name="bframe",
    version=version(),
    author="Bean-jun",
    author_email="1342104001@qq.com",
    description="A simple python web server frame",
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT License',
    url="https://github.com/Bean-jun/bframe", 

    packages=find_packages(),

    classifiers = [
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.9',
    ],
)