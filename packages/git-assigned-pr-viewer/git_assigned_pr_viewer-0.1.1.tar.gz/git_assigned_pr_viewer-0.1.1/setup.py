from setuptools import setup, find_packages

setup(
    name="git-assigned-pr-viewer",
    version="0.1.1",
    author="Mathieu Montgomery",
    author_email="mathieu.montgomery@mailbox.org",
    description="A better viewer of github pending reviews",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/L1ttleM/git-assigned-pr-viewer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "certifi>=2024.6.2",
        "charset-normalizer>=3.3.2",
        "click>=8.1.7",
        "humanize>=4.9.0",
        "idna>=3.7",
        "requests>=2.32.3",
        "tabulate>=0.9.0",
        "urllib3>=2.2.1",
    ],
    entry_points={
        'console_scripts': [
            'git-assigned-pr-viewer=src.main:git_assigned_pr_viewer',
        ],
    },
)