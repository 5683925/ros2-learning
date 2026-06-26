from setuptools import setup

package_name='turtle_tracker'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]), #向ament注册这个包，让找到你的包
         ('share/' + package_name, ['package.xml']), #安装xml到share目录
    ],
    install_requires=['setuptools'], #setuptools是PYTHON自带的工具
    zip_safe=True, #支持压缩打包，不用解压
    maintainer='coco',
    maintainer_email='3382793407@qq.com',
    description='turtle2追踪turtle1的ROS2节点',
    license='MIT',
    entry_points={
        'console_scripts':['turtle_tracker=turtle_tracker.turtle_chaser:main',], #命令名 = 包名.模块名:入口函数，终端可以用ros2 run 包名 命令名，不用python xx.py
    },

)