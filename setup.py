from setuptools import setup

setup(
	name='expense_reclassification_streamlit_app',
	author = 'Shishir Deshpande',
	packages = ['expense_reclassification',],
	package_dir = {'expense_reclassification':'expense_reclassification',},
	package_data = {'expense_reclassification':['mappings/*.csv','sql/*.txt']},
	version='0.0.1',
	description = 'library to help classify transactions',
	install_requires=[
        'pandas>=1.2.4',
        'numpy>=1.21.1',
        'datetime>=4.3',
        'python-dateutil>=2.7.0',
        'pyodbc',
    ],
)
