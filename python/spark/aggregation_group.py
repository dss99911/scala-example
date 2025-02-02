from spark.util.util import *
import spark.read as r

# null imputation on pivot and aggregation is on null_imputation_on_aggregation.png.
df = r.create()

df.groupby('a').agg(
    first('b').alias('b'),
    expr("percentile(b, array(0.5))")[0].alias("median")
).show()

df.agg({'flag': 'sum', 'message': 'count'})

agg_by_dict(df.groupby("c"), {
    "a": ["count", "sum", "min", "max"],
    "b": count_distinct,
}, True, "test").show()

