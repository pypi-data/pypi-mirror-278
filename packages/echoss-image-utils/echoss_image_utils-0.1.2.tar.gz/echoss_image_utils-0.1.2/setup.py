from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = "echoss_image_utils"

setup(
    name='echoss_image_utils',

    version='0.1.2',
    url='',
    install_requires=['scikit-learn==1.0.2', 'labelme==5.2.1', 'echoss_s3handler'],
    license='',
    author='incheolshin',
    author_email='incheolshin@12cm.co.kr',
    description='echoss AI Bigdata Solution - image utils[image dataset split, labelme2yolo format]',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['echoss', 'echoss_image_utils', 'labelme2yolo', 'labelme', 'yolo'],
    package_data={},
    python_requires= '>3.7',
)
