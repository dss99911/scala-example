from py4j.java_gateway import java_import
from util.util import *

def access_java_obj_on_drivder(spark):
    # driver 노드에서만 가능한 방법
    model = spark._sc._jvm.com.model.SomeModel.Builder().build()

    # call static method
    spark._sc._jvm.com.model.SomeModel.someMethodCall("d")

    java_import(spark._sc._jvm, "com.model.SomeModel")
    model = spark._sc._jvm.SomeModel.Builder().build()
    

def access_java_udf(spark, df):
    # https://dzone.com/articles/pyspark-java-udf-integration-1
    # org.apache.spark:spark-core_2.11:2.0.0
    # org.apache.spark
    # 1. add java dependency
    # <dependency>
    #   <groupId>org.apache.spark</groupId>
    #   <artifactId>spark-core_2.11</artifactId>
    #   <version>2.0.0</version>
    # </dependency>
    # <dependency>
    #   <groupId>org.apache.spark</groupId>
    #   <artifactId>spark-sql_2.11</artifactId>
    #   <version>2.0.0</version>
    # </dependency>

    # 2. use java UDF1 and create jar
    # package com.JavaUDFProj;
    # import org.apache.spark.sql.api.java.UDF1;
    # public class AddNumber implements UDF1<Long, Long> {
    # private static final long serialVersionUID = 1L;
    # @Override
    # public Long call(Long num) throws Exception {
    # return (num + 5);
    #    }
    # }


    # 3. add jar or repository "spark.jars.packages": "com:artifact:version"
    spark.udf.registerJavaFunction("nerUdf", "com.module.NerUdf")
    df.withColumn("result", expr("nerUdf(message)"))


def access_java_by_column():
    # https://github.com/databricks/spark-xml/blob/c529e1f65493871f705bcd8cbac41a19f73f143f/src/main/scala/com/databricks/spark/xml/functions.scala
    # https://github.com/databricks/spark-xml#pyspark-notes
    # use CatalystSqlParser.
    # use extends UnaryExpression with CodegenFallback with ExpectsInputTypes
    pass