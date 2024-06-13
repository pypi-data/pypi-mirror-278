from setuptools import setup, find_packages
from get_version import read_version

setup(
    name='aicastle',
    version=read_version(),
    packages=find_packages(include=['aicastle', 'aicastle.*']),
    include_package_data=True,
    package_data={
        'aicastle': ['package_data/*'],
    },
    install_requiress=[ # 의존성
        # 'tqdm', 'pandas', 'scikit-learn', 
        'openai',
        'azure-identity',
        'boto3',
        'pillow'
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
