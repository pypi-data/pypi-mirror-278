import setuptools

requirements = [
    'jupyter>=1.0.0',
    'numpy>=1.21.5',
    'matplotlib>=3.5.1',
    'requests>=2.25.1',

    'pandas>=1.2.4',
    'torch',
    'torchvision',
    'opencv-python',
]

setuptools.setup(
    name="PepperPepper",
    version="0.0.7.41",
    python_requires='>=3.11',
    author="Aohua Li",
    author_email="pepper2024jlu@163.com",
    description="It is a DeepLearning package to foster developed by Aohua Li",
    url="",
    packages=setuptools.find_packages(),
    zip_safe=True,
    install_requires=requirements,
)


