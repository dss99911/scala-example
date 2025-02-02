from pyspark.sql import SparkSession
from pyspark.sql.functions import upper
from pyspark.sql.functions import col, asc,desc
from pyspark.sql.types import DoubleType

spark = SparkSession.builder.getOrCreate()

df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])

df.select(df.c).show()
df.withColumn('upper_c', upper(df.c)).show()
df.filter(df.a == 1).show()

# 컬럼이 많은 경우, 타입 변환할 때 withColumn이 많으면, 성능 문제가 발생함. 이 경우, select를 사용하기.
# withColumn할 때마다. Catalyst analysis를 매번하게되어, 시간이 오래 걸린다는 듯.
# https://medium.com/@manuzhang/the-hidden-cost-of-spark-withcolumn-8ffea517c015
cols = [col(f.name).cast(DoubleType()) if (f.dataType != DoubleType()) else col(f.name) for f in df.schema.fields]
df.select(cols)

# replace
mapping = {
    'string1': "1",
    'string2': "2"
}
df.withColumn("c2", col("c"))\
    .replace(mapping, subset=['c'])

# Sort
df.sort(col("count").desc())