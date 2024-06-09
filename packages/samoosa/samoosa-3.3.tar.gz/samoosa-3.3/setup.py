from setuptools import setup, find_packages

setup(
    name="samoosa",
    version="3.3",
    author="Pranav S V",
    author_email="thisispranavsv@yahoo.com",
    description="Samoosa is an innovative Python-based tool designed to provide concise and comprehensive summaries of YouTube videos.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/PRANAV-S-V/samoosa-tool.git",
    packages=find_packages(),
    install_requires=[
        'youtube_transcript_api>=0.4.4',
        'google-generativeai>=0.1.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'samoosa=samoosa:main_function',
        ],
    },
)
