
from setuptools import setup, find_packages

setup(
    name="airiallm",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'scikit-learn==1.5.0',
        'numpy==1.26.4',
        'requests==2.32.3',
        'python-decouple==3.8'
    ],
    entry_points={
        'console_scripts': [
            'airiallm=airiallm.airiallm:main',
        ],
    },
    author="Ashutosh Renu",
    author_email="ashutosh@airia.in",
    description="AiriaLLM is a client tool connected to AiriaCognition, leveraging the power of LLaMA3 8B and 70B models to deliver advanced generative AI features. This package enables seamless integration of cutting-edge AI capabilities into your projects, enhancing content creation, natural language understanding, and complex problem-solving.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/airia-in/airiallm.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)