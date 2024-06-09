from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='phi-3-vision-mlx',
    url='https://github.com/JosefAlbers/Phi-3-Vision-MLX', 
    py_modules=['phi_3_vision_mlx'],
    version='0.0.3-alpha',
    packages=find_packages(),
    readme="README.md",
    author_email="albersj66@gmail.com",
    descriptions="Phi-3-Vision on Apple silicon with MLX",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Josef Albers",
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements
)