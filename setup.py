from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name="bframe",
    version="0.0.1",
    author="Bean-jun",
    author_email="1342104001@qq.com",
    description="A simple python web server frame",
    long_description=readme(),
    long_description_content_type='text/markdown',
    # 项目主页
    url="https://github.com/Bean-jun/bframe", 

    packages=find_packages(),

    classifiers = [
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.9',
    ],
)