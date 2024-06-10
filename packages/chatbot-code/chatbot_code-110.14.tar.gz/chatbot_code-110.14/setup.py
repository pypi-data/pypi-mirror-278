from setuptools import setup, find_packages

setup(
    name='chatbot_code',
    version='110.14',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 'Django>=3.2,<4.0',
    ],
    entry_points={
        'console_scripts': [
            'manage.py = chatbot.manage:main',
            'configure-aws = chatbot.scripts.configure_aws:main',
            'readme = chatbot.scripts.readme:main',
        ],
    },
    package_data={
        '': ['README.md', 'manage.py', 'requirements.txt'],
        'app1': ['static/*', 'templates/*', 'templatetags/*'],
        'chatbot': ['*'],  # Include all files in the chatbot directory
    },
    author='Swati Saini',
    author_email='swati@mixorg.com',
    description='A Django app for chatbot functionality.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/saini2001/chatbot_code',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3.11',
    ],
)
