from pyspark.sql.functions import when

# Assuming you have already created a SparkSession as 'spark' and have a DataFrame named 'df'

# Populate columns B, C, and D based on the conditions specified
df = df.withColumn("B", when(df["A"] == "abc", 1).otherwise(0)) \
       .withColumn("C", when(df["A"].isin("x", "Y", "z"), 1).otherwise(0)) \
       .withColumn("D", when(df["B"] == 0 & df["C"] == 0, 1).otherwise(0))

# Show the DataFrame with the new columns
df.show()
