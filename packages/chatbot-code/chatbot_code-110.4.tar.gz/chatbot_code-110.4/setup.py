from setuptools import setup, find_packages

setup(
    name='chatbot_code',
    version='110.4',
    packages=find_packages(include=['chatbot', 'chatbot.*', 'app1', 'app1.*']),
    include_package_data=True,
    install_requires=[
        'django>=3.2,<4.0',
        'requests',
        'bs4',
        'fitz',
        'python-docx',
        'textract',
        'pillow',
        'pytesseract',
        'numpy',
        'nltk',
        'sentence-transformers',
        'scikit-learn',
        'boto3',
        'PyMuPDF',
        'python-pptx',
        'openai',
        'django-admin',
        'frontend',
        'tools',
        'inflect',
        'PyPDF2'
    ],
    entry_points={
        'console_scripts': [
            'manage.py = chatbot.manage:main',
            'configure-aws = chatbot.scripts.configure_aws:main',
            'readme = chatbot.scripts.readme:main',
        ],
    },
    package_data={
        '': ['README.md'],
        'app1': ['static/*', 'templates/*', 'templatetags/*'],
        'chatbot': ['scripts/*'],
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
