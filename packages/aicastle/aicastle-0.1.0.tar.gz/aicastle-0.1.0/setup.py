from setuptools import setup, find_packages
import os

# 버전을 aicastle/__init__.py에서 읽어옴
def read_version():
    version_file = os.path.join('aicastle', '__init__.py')
    with open(version_file, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name='aicastle',
    version=read_version(),
    packages=find_packages(include=['aicastle', 'aicastle.*']),
    install_requires=[ # 의존성
        # 'tqdm', 'pandas', 'scikit-learn', 
    ],

    author='aicastle',
    author_email='dev@aicastle.io',
    description='AI Castle Package',
    url='https://github.com/ai-castle/aicastle',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    zip_safe=False,
)
