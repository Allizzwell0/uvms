from setuptools import setup

package_name = 'my_uvms_drivers'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='OpenAI',
    maintainer_email='user@example.com',
    description='Low-level wrappers for ROV and manipulator commands.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'rov_reference_command = my_uvms_drivers.rov_reference_command:main',
            'arm_joint_command = my_uvms_drivers.arm_joint_command:main',
        ],
    },
)
