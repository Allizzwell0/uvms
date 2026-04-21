from setuptools import setup

package_name = 'my_uvms_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/auv_arm_grasp.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='OpenAI',
    maintainer_email='user@example.com',
    description='Simple UVMS control node.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'auv_arm_grasp = my_uvms_control.auv_arm_grasp:main',
        ],
    },
)
