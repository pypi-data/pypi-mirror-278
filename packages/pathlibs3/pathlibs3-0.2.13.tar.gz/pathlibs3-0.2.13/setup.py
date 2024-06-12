# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathlibs3']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'urllib3']

extras_require = \
{'docs': ['Sphinx', 'sphinx-rtd-theme', 'sphinxcontrib-napoleon']}

setup_kwargs = {
    'name': 'pathlibs3',
    'version': '0.2.13',
    'description': 'S3 navigation using object, inspired by pathlib.Path',
    'long_description': '# Installation\n\n```sh\npip install pathlibs3\n```\n\n# Usage\n\n## Create a PathlibS3 Object\n```python\nfrom pathlibs3.pathlibs3 import S3Path\n# Create a pathlibs3\n\nclient = boto3.client("s3", region_name="us-east-1")\nbucket = "test-bucket"\n\n# Create an object to s3://test-bucket/myfolder\ns3_path_to_myfolder = S3Path(client, bucket, "myfolder/")\n\n\n# You can also concatenate object\n# Create an object to s3://test-bucket/myfile/random_file.txt\ns3_path_to_random_file = s3_path_to_myfolder / "random_file.txt"\n```\n\n## Iter over a directory\n\n```Python\n# Iter over this directory\nfor path in s3_path.iterdir():\n    print(path)\n\n# Iter over this directory recursively\nfor path in s3_path.iterdir(recursive=True):\n    print(path)\n```\n\n## Copy file or folder\n\n### Copy from s3 to local\n```python\n# Create an pathlibs3 object\ns3_path_to_myfolder = S3Path(client, bucket, "myfolder/")\n\n# Create a pathlib object\nlocal_path = Path("/tmp/local_folder")\n\n# Will download the s3 folder localy\nS3Path.copy(s3_path_to_myfolder, local_path)\n```\n\n### Copy from local to s3\n```python\n# Create an pathlibs3 object\ns3_path_to_myfolder = S3Path(client, bucket, "myfolder/")\n\n# Create a pathlib object\nlocal_path = Path("/tmp/local_folder")\n\n# Will download the s3 folder localy\nS3Path.copy(local_path, s3_path_to_myfolder)\n\n```\n\n\n### Copy from s3 to s3\n```python\n# Create an pathlibs3 object\ns3_path_to_myfolder = S3Path(client, bucket, "myfolder/")\n\n# Create another pathlibs3 object\ns3_path_to_anotherfolder = S3Path(client, bucket, "anotherfolder/")\n\n# Will download the s3 folder localy\nS3Path.copy(s3_path_to_myfolder, s3_path_to_anotherfolder)\n```\n\n# Contribution\n## run test\n\nrun test with `poetry run python -m pytest`\n',
    'author': 'thibault.blanc',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thibaultbl/s3_navigator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
