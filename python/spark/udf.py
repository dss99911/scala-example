# %%
from pyspark.sql.functions import udf
from pyspark.sql.functions import col, asc, desc
from pyspark.sql.types import FloatType, StructType, StringType, StructField, DoubleType, ArrayType, IntegerType

from spark.read import create_by_row

def udf_by_lambda():
    # udf에 type을 정의 안하면, StringType()
    x2 = udf(lambda x: x * 2)
    x2 = udf(lambda x: x * 2, StringType())
    x2 = udf(lambda x: ["a","b"], ArrayType(StringType()))
    create_by_row().withColumn("a2", x2("a"))


def udf_by_func():
    def add_1(x):
        return x + 1
    create_by_row().withColumn("a1", udf(add_1)("a")).show()


def udf_by_annotation():
    # todo not yet tested
    @udf(FloatType())
    def add_1(x):
        return x + 1

    create_by_row().withColumn("a1", add_1("a")).show()

# %%


# https://docs.databricks.com/spark/latest/spark-sql/udf-python.html


from difflib import SequenceMatcher

from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType, StructType, StringType, StructField
from pyspark.sql.functions import udf
import pyspark.sql.functions as F


def getSentenceDiffRatio(stc1, stc2):
    # ratio = SequenceMatcher(lambda x: x == " ", stc1.split(), stc2.split())
    result = None
    try:
        if (stc1 != None) & (stc2 != None):
            ratio = SequenceMatcher(lambda x: x == " ", stc1.split(), stc2.split()).ratio()

            result = { \
                "ratio": ratio, \
                "status": 'SUCCESS', \
                "sentence1": stc1, \
                "sentence2": stc2, \
                "errorMessage": None}
        else:
            result = { \
                "ratio": None, \
                "status": 'FAILURE', \
                "sentence1": stc1, \
                "sentence2": stc2, \
                "errorMessage": None}

    except Exception as error:
        result = { \
            "ratio": None, \
            "status": 'FAIL', \
            "sentence1": stc1, \
            "sentence2": stc2, \
            "errorMessage": error.getMessage()}

    finally:
        return result

def udf_with_schema():
    diffRatioSchema = StructType([ \
        StructField('ratio', FloatType(), False) \
        , StructField('status', StringType(), False) \
        , StructField('sentence1', StringType(), False) \
        , StructField('sentence2', StringType(), False) \
        , StructField('errorMessage', StringType(), True) \
        ])

    getSentenceDiffRatioUDF = udf(lambda x, y: getSentenceDiffRatio(x, y), diffRatioSchema)

    # use on sql
    spark = SparkSession.builder.appName("acs_tx_extractor").getOrCreate()
    spark.udf.register('getSentenceDiffRatioUDF', getSentenceDiffRatio, diffRatioSchema)

#%% pandas udf : pandas의 기능을 쓰고 싶을 때 쓰는듯. 성능이 더 빠름
# https://spark.apache.org/docs/3.1.2/api/python/reference/api/pyspark.sql.functions.pandas_udf.html
# https://pizzathief.oopy.io/spark3-pandas-udf
# https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html
from pyspark.sql.functions import pandas_udf
import pandas as pd
import numpy as np


def process_pandas_udf(spark):
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    def func(pdf: pd.DataFrame) -> pd.Series:
        out = pdf.apply(lambda x: np.dot(x["target_vector"].toArray(), x["right_vector"].toArray()), axis=1)
        return out

    my_udf = pandas_udf(func, returnType=DoubleType())

    out = spark.read.parquet("some")\
        .select(my_udf("two_vectors").alias("cosine_similarity"))

@pandas_udf("double")  # return type col type
def mean_udf(v: pd.Series) -> float:
    return v.mean()

@pandas_udf(IntegerType())
def slen(s: pd.Series) -> pd.Series:
    return s.str.len()

print(df.groupby("id").agg(mean_udf(df['v'])).collect())