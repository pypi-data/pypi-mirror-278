from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = "echoss_s3handler"

setup(
    name='echoss_s3handler',
    version='0.1.2',
    url='',
    install_requires=['boto3~=1.19.0', 'opencv-python==4.8.0.74', 'tqdm==4.63.2', 'pillow==10.1.0'],
    license='',
    author='incheolshin',
    author_email='incheolshin@12cm.co.kr',
    description='echoss AI Bigdata Solution - S3 handler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['echoss', 'echoss_s3handler', 's3handler', 's3_handler'],
    package_data={},
    python_requires= '>3.7',
)
