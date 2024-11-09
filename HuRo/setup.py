from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'HuRo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yerim',
    maintainer_email='yerim@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'hello_world_node = HuRo.hello_world_node:main', #노드실행 등록
        	'hello_publisher = HuRo.hello_publisher:main',
        	'hello_subscriber = HuRo.hello_subscriber:main',
        ],
    },
)
