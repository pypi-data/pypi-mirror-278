from setuptools import setup, find_packages
from task_ai import __version__
version = __version__

def main():
    with open('README.md', 'r') as readme:
        long_description = readme.read()
    setup(
        name='task-ai',
        version=version,
        author_email="huseyim@gmail.com",
        license="CC BY-NC 4.0",
        packages=find_packages(),
        package_data={
            'task_ai': ['templates/*.yaml', 'prompts/examples/*.yaml'],
        },
        include_package_data=True,
        install_requires=[
            "setuptools >= 44.1.1",
            "click == 8.1.6",
            "PyYAML",
            "requests"
        ],
        author='Huseyin G.',
        description='A CLI tool for describing tasks using LLM tools',
        entry_points={
            'console_scripts': [
                'task-ai=task_ai.main:main'
            ]
        },
        python_requires='>=3.7',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown"
    )


if __name__ == '__main__':
    main()
