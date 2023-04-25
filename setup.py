from setuptools import setup

setup(
	name='movie_recommender',
	author = 'Shishir Deshpande',
	packages = ['movie_recommender',],
	package_dir = {'movie_recommender':'movie_recommender',},
	package_data = {'movie_recommender':['mappings/*.csv','sql/*.txt']},
	version='0.0.1',
	description = 'App to recommend movies <2009',
	install_requires=[
        'pandas>=1.2.4',
        'numpy>=1.21.1',
        'datetime>=4.3',
        'python-dateutil>=2.7.0',
        'pyodbc',
    ],
)
