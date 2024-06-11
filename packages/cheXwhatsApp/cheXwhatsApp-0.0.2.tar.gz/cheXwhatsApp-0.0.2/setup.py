import setuptools
setuptools.setup(
    name='cheXwhatsApp',
    version='0.0.2',
    author="Sahil Lathiya",
    author_email="sahilm@iisc.ac.in",
    description="",
    packages=setuptools.find_packages(),
    install_requires=['os', 'torch', 'imageio', 'scikit-image', 'numpy', 'tqdm', 'pandas', 'warnings'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)