# Databricks notebook source
# Telemetry ETL Pipeline
# This notebook is part of the telemetry data processing pipeline. 
# It reads raw .jsonl data from Azure Blob Storage, processes it using PySpark (Silver layer), 
# and saves it in Delta Lake format.

STORAGE_KEY = ""

path_all = "wasbs://telemetry@telemetrystorage321.blob.core.windows.net/*.jsonl"

df_all = spark.read \
    .option(f"fs.azure.account.key.telemetrystorage321.blob.core.windows.net", STORAGE_KEY) \
    .json(path_all)

print(f"Number of all records in Azure: {df_all.count()}")
df_all.show(10)

# COMMAND ----------

from pyspark.sql.functions import col, from_unixtime


df_silver = df_all.select(
    col("player_id"),
    col("weapon"),
    col("event_type"),
    # Conversion of timestamp to human-readable format
    from_unixtime(col("timestamp")).alias("event_time"),
    # Get position as separate columns
    col("position.x").alias("pos_x"),
    col("position.y").alias("pos_y")
)

display(df_silver)

# COMMAND ----------

# Number of events per weapon
weapon_stats = df_silver.groupBy("weapon").count().orderBy("count", ascending=False)

display(weapon_stats)

# COMMAND ----------


silver_path = "wasbs://telemetry@telemetrystorage321.blob.core.windows.net/silver_data"

# Save the Silver data back to Azure in Delta format
df_silver.write.format("delta") \
    .mode("overwrite") \
    .option(f"fs.azure.account.key.telemetrystorage321.blob.core.windows.net", STORAGE_KEY) \
    .save(silver_path)

print("Dane Silver zostały zapisane pomyślnie w Azure!")

# COMMAND ----------


df_recovered = spark.read.format("delta") \
    .option(f"fs.azure.account.key.telemetrystorage321.blob.core.windows.net", STORAGE_KEY) \
    .load(silver_path)

# Show the recovered data
print(f"Odtworzono {df_recovered.count()} rekordów.")
display(df_recovered)