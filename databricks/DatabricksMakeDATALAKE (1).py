# Databricks notebook source
STORAGE_KEY = ""

path_all = "wasbs://telemetry@telemetrystorage321.blob.core.windows.net/arena_logs.jsonl"

df_all1 = spark.read \
    .option(f"fs.azure.account.key.telemetrystorage321.blob.core.windows.net", STORAGE_KEY) \
    .json(path_all)

print(f"All records: {df_all.count()}")
df_all.show(10)

# COMMAND ----------

from pyspark.sql.functions import col, from_unixtime

# create a new DataFrame with selected columns and transformations
df_silver1 = df_all1.select(
    col("player_id"),
    col("weapon"),
    col("event_type"),
    # Convert timestamp from Unix time to human-readable format
    from_unixtime(col("timestamp")).alias("event_time"),
    # Extract x and y from the position struct

    col("position.x").alias("pos_x"),
    col("position.y").alias("pos_y"),
    col("victim_id"),
    col("players_remaining")
)

display(df_silver1)

# COMMAND ----------

# Weapons usage statistics
weapon_stats = df_silver1.groupBy("weapon").count().orderBy("count", ascending=False)

display(weapon_stats)

# COMMAND ----------


silver_path1 = "wasbs://telemetry@telemetrystorage321.blob.core.windows.net/silver_data"

# Save the Silver DataFrame as a Delta table in Azure
df_silver1.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option(f"fs.azure.account.key.telemetrystorage321.blob.core.windows.net", STORAGE_KEY) \
    .save(silver_path1)

print("Dane Silver zostały zapisane pomyślnie w Azure (z nowym schematem)!")

# COMMAND ----------

# Path to the Silver Delta table in Azure
# ODCZYT
df_recovered = spark.read.format("delta") \
    .option(f"fs.azure.account.key.telemetrystorage321.blob.core.windows.net", STORAGE_KEY) \
    .load(silver_path1)

# Wyświetlenie wyników
print(f"Odtworzono {df_recovered.count()} rekordów.")
display(df_recovered)

# COMMAND ----------

# Create a temporary view for SQL queries
df_silver1.createOrReplaceTempView("arena_telemetry")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     weapon, 
# MAGIC     COUNT(*) AS total_eliminations 
# MAGIC FROM arena_telemetry 
# MAGIC GROUP BY weapon 
# MAGIC ORDER BY total_eliminations DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     pos_x, 
# MAGIC     pos_y, 
# MAGIC     weapon,
# MAGIC     players_remaining
# MAGIC FROM arena_telemetry;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     player_id AS MVP, 
# MAGIC     COUNT(victim_id) AS total_eliminations
# MAGIC FROM arena_telemetry 
# MAGIC GROUP BY player_id 
# MAGIC ORDER BY total_eliminations DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     weapon,
# MAGIC     SUM(CASE WHEN players_remaining >= 70 THEN 1 ELSE 0 END) AS early_game_kills,
# MAGIC     SUM(CASE WHEN players_remaining BETWEEN 20 AND 69 THEN 1 ELSE 0 END) AS mid_game_kills,
# MAGIC     SUM(CASE WHEN players_remaining < 20 THEN 1 ELSE 0 END) AS late_game_kills,
# MAGIC     COUNT(*) AS total_kills
# MAGIC FROM arena_telemetry
# MAGIC GROUP BY weapon
# MAGIC ORDER BY total_kills DESC;