from setuptools import setup, find_packages

setup(
    name='question_answer_db',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'psycopg2',  # Since we're using PostgreSQL
    ],
    package_data={
        'app1': ['*.py'],  # Include all Python files in question_answer_db
    },
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
