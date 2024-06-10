# from setuptools import setup, find_packages

# setup(
#     name='chatbot_code',
#     version='110.3',
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         'django>=3.2,<4.0',
#         'requests',
#         'bs4',
#         'fitz',
#         'python-docx',
#         'textract',
#         'pillow',
#         'pytesseract',
#         'numpy',
#         'nltk',
#         'sentence-transformers',
#         'scikit-learn',
#         'boto3',
#         'PyMuPDF',
#         'python-pptx',
#         'openai',
#         'django-admin',
#         'frontend',
#         'tools',
#         'inflect',
#         'PyPDF2'
#     ],
#     entry_points={
#         'console_scripts': [
#             'manage.py = chatbot.manage:main',
#             'configure-aws = chatbot.scripts.configure_aws:main',
#             'readme = chatbot.scripts.readme:main',
#         ],
#     },
#     package_data={
#         '': ['README.md'],
#         'app1': ['static/*', 'templates/*' , 'templatetags/*'],
#     },
#     author='Swati Saini',
#     author_email='swati@mixorg.com',
#     description='A Django app for chatbot functionality.',
#     long_description=open('README.md').read(),
#     long_description_content_type='text/markdown',
#     url='https://github.com/saini2001/chatbot_code',
#     classifiers=[
#         'Framework :: Django',
#         'Programming Language :: Python :: 3.11',
#     ],
# )


# include README.md
# include LICENSE
# include post_install.py
# recursive-include app1/static *
# recursive-include app1/templates *


















from setuptools import setup, find_packages

setup(
    name='chatbot-code',
    version='110.11',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2,<4.0',
        # List other actual dependencies here
    ],
    package_data={
        '': ['*.html', '*.css', '*.js', 'requirements.txt', 'manage.py'],
        'static': ['*'],  # Include all files in the static directory
    },
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Framework :: Django',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

