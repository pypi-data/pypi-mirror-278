from setuptools import setup, find_packages

setup(
    name="image-bucket",
    version="0.8",
    packages=find_packages(),
    install_requires=[
        'opencv-python==4.10.0.82',
    ],
    entry_points={
        'console_scripts': [
            'image-bucket = image_bucket.image_bucket:main',
        ],
    },
)
