from setuptools import setup

setup(
    name='HuRo',
    version='0.0.1',
    packages=['scripts'],  # Python 패키지로 설정
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yerim',
    maintainer_email='yerim@todo.todo',
    description='Python package for HuRo project',
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'gui2effort = scripts.gui2effort:main',
            'joint_state_bridge = scripts.joint_state_bridge:main',
            'auto_terra = scripts.auto_terra:main',
            'manualPLUSauto = scripts.manualPLUSauto:main',
            'effort_bridge = scripts.effort_bridge:main',
        ],
    },
)

