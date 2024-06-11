from setuptools import setup, find_packages

setup(
    name="ros_sensor_topic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    author="Katrin-Misel Ponomarjova",
    author_email="katrinmisel@gmail.com.com",
    description="A utility package to find ROS topic names for color and depth streams.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/katrinmisel/ros_sensor_topic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)