from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType

spark = SparkSession.builder.master("local").appName("Word Count").getOrCreate()

# multiline是指json是一整行或是有換行符 (Spark while processing json data considers each new line as a complete json),
# You should keep your complete json in a single line in a compact form by removing all white spaces and newlines,
# like {"a":{"b":1}}. However adding option to read multi line JSON in the code as follows so that
# you could read the nested attribute.
df = spark\
        .read\
        .option("multiline","true")\
        .option("inferTimestamp", "true")\
        .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")\
        .json("json_string.json")

# single column cast (spark infers numeric type as longType by default)
df = df.withColumn("no2", col("no").cast(IntegerType()))

df.printSchema()

# nested type cast
df = df.selectExpr(
  "CAST(structureType AS array<struct<no:integer, sex:string, processTime:timestamp>>) structureType",
  "no2","address","name","no"
)

print(df.schema.json())

df.show()

with open("schema.json", "w") as f:
    f.write(df.schema.json())
