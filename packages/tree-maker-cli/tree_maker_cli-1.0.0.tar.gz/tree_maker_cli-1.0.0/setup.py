from setuptools import setup, find_packages

setup(
    name='tree_maker_cli',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tree-maker = tree_maker:main'
        ]
    },
    install_requires=['pyperclip'],
    author='Timothy Czerniec',
    author_email='teczerniec@gmail.com',
    description='A command-line tool to generate a tree structure of a folder and its contents, useful for when you need to add context to your GPT prompts.',
    license='MIT',
    keywords='tree cli folder structure',
    url='https://github.com/tecz/tree_maker_cli'
)
