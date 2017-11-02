from setuptools import setup

setup(name='xis-image-indexer',
      version='0.1',
      description='XIS Image Classifier',
      url='https://github.com/XoriantOpenSource/XIS-Image-Classification',
      author='Sujit Nalawade',
      author_email='technosujit25@gmail.com',
      license='MIT',
      packages=['AppConfig', 'GCP_StorageOpsHandler', 'Minio_OpsHandler', 'XIS_Image_Indexer', 'XIS_RestApi'],
      entry_points={
 	'console_scripts':['image-indexer =XIS_Image_Indexer.__main__:main' ]	
      },
      zip_safe=False)
