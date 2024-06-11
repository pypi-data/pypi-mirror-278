from setuptools import setup

setup(
    name='ict_agent',
    version='1.0.13',
    authors='陈向学',
    description='智能ict三维编程拓展组件',
    packages=["ict_agent"],
    include_package_data=True,
    install_requires=[
        'websocket-client'
    ]
)