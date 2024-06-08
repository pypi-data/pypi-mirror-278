from setuptools import setup, find_packages

setup(
    name="arcodeai",
    version="0.1.2",
    description="Holistic software development via LLM",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Alexandria Redmon",
    author_email="alexandria@example.com",
    url="https://github.com/alexdredmon/arcode",
    packages=find_packages(),
    install_requires=[
        "inquirerpy==0.3.4",
        "openai==1.30.5",
        "pyperclip==1.8.2",
        "langchain==0.2.1",
        "langchain-community==0.2.1",
        "langchain-core==0.2.3",
        "langchain-openai==0.1.8",
        "langchain-text-splitters==0.2.0",
        "pydantic==2.7.3",
        "pydantic_core==2.18.4",
        "docarray==0.40.0",
        "python-dotenv==1.0.0",
        "dill==0.3.6",
        "litellm==1.40.0",
        "tiktoken",
        "pyinstaller==5.7.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'arcode=arcode:main',
        ],
    },
    include_package_data=True,
)