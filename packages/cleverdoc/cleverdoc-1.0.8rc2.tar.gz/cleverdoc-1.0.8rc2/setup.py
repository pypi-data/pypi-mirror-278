from distutils.core import setup
from setuptools import setup, find_packages
import os

if os.path.exists('../cleverdoc'):
    import package_obfuscator
    package_obfuscator.obfuscate('../cleverdoc', output='cleverdoc', force_output_overwrite=True)

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'cleverdoc', 'VERSION')) as version_file:
    version = f"{version_file.read().strip()}"

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    install_requires=[
            "pyspark>=3.0.2,<=3.4.2",
            "pyarrow",
            "tesserocr",
            "numpy",
            "pandas",
            "pillow",
            "PyMuPDF",
            "pyJWT",
            "cryptography",
            "imagesize",
            "img2pdf"
        ],
    extras_require={
        "llm": ["openai"],
        "inference": ["optimum[onnxruntime]", "onnx"],
        "inference-gpu": ["optimum[onnxruntime-gpu]"],
        },
    name='cleverdoc',
    version=version,
    #packages=['cleverdoc'],
    packages=find_packages(include=['cleverdoc', 'cleverdoc.*'], exclude=["__pycache__", "tests"]), #find_packages(exclude=["tests"]),
    #packages=find_packages(exclude=["tests"]),
    #package_data={"cleverdoc.resources": ["*/*"]},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://apicom.pro',
    license='',
    author='ApicomPro',
    author_email='info@apicom.pro',
    description='AI lib for processing and de-identification medical documents and images.',
    python_requires='>=3.9',
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    project_urls = {
        "Documentation": "https://cleverdoc.apicom.pro/",
        "Workshop": "https://github.com/ApiComPro/cleverdoc-workshop",
        },
    )
