import os
import sys
import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession
from importlib.resources import files
from cleverdoc.image.BinaryToImage import BinaryToImage
from cleverdoc.image.ImageDrawBoxes import ImageDrawBoxes
from cleverdoc.models.recognizers.ImageToString import ImageToString
from cleverdoc.models.ner.Ner import Ner
from cleverdoc.models.ner.NerMerger import NerMerger
from cleverdoc.models.ner.NerLLM import NerLLM
from cleverdoc.models.ner.StringToKeyValue import StringToKeyValue
from cleverdoc.pdf.ImageToPdf import ImageToPdf
from cleverdoc.pdf.SingleImageToPdf import SingleImageToPdf
from cleverdoc.pdf.PdfToImage import PdfToImage
from cleverdoc.utils.display_utils import show_image, show_images, show_pdf_file
from cleverdoc.pdf.PdfAssembler import PdfAssembler
from cleverdoc.utils import get_aws_version, get_name
from cleverdoc.enums import Device
__all__ = ['BinaryToImage',
           'ImageDrawBoxes',
           'ImageToString',
           'Ner',
           'NerMerger',
           'NerLLM',
           'StringToKeyValue',
           'ImageToPdf',
           'SingleImageToPdf',
           'PdfToImage',
           'PdfAssembler',
           'show_image',
           'show_images',
           'get_aws_version',
           'start',
           'get_name',
            'Device',
            'show_pdf_file'
           ]

def version():
    version_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(version_path, 'VERSION'), encoding="utf-8") as version_file:
        return version_file.read().strip()


__version__ = version()

def info():
    print(f"Spark version: {pyspark.__version__}")
    print(f"CleverDoc version: {version()}\n")


def start(license,
          extra_conf=None,
          master_url="local[*]",
          with_aws=False,
          logLevel="ERROR"):
    """
    Start Spark session with CleverDoc configuration
    @param extra_conf: Instance of SparkConf or dict with extra configuration.
    """
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ["CLEVERDOC_LICENSE"] = license

    os.environ["TRANSFORMERS_VERBOSITY"] = logLevel.lower()

    jars = [str(files("cleverdoc").joinpath("resources").joinpath("jars").joinpath("spark-pdf-0.1.0.jar")),]
    default_conf = {"spark.driver.memory": "8G",
                    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
                    "spark.kryoserializer.buffer.max": "200M",
                    "spark.sql.repl.eagerEval.enabled": "true"
                    }

    builder = SparkSession.builder \
        .appName("CleverDoc") \
        .master(master_url)

    jars_packages = []
    if with_aws:
        jars_packages.append("org.apache.hadoop:hadoop-aws:" + get_aws_version())

    if extra_conf:
        if not isinstance(extra_conf, dict):
            extra_conf = dict(extra_conf.getAll())
        default_conf.update(extra_conf)
        extra_jars_packages = default_conf.get("spark.jars.packages")
        if extra_jars_packages:
            jars_packages.append(extra_jars_packages)
        extra_jars = default_conf.get("spark.jars")
        if extra_jars:
            jars.append(extra_jars)

    for k, v in default_conf.items():
        builder.config(str(k), str(v))

    builder.config("spark.jars", ",".join(jars))
    builder.config("spark.jars.packages", ",".join(jars_packages))

    info()
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(logLevel=logLevel)
    return spark
