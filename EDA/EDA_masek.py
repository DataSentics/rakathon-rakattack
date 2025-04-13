# Databricks notebook source
from pyspark.sql.functions import length, col, size

# COMMAND ----------

# MAGIC %md
# MAGIC # Load data

# COMMAND ----------

amb = spark.table("rakathon_hackathon.onkominer.ambulant_reports")
pac = spark.table("rakathon_hackathon.onkominer.pac_documentation")
pat = spark.table("rakathon_hackathon.onkominer.pathology")
ren = spark.table("rakathon_hackathon.onkominer.rentgen")
all = spark.table("rakathon_hackathon.onkominer.all_reports_data")

# COMMAND ----------

# MAGIC %md
# MAGIC # Get basic info

# COMMAND ----------

print(amb.count())
print(pac.count())
print(pat.count())
print(ren.count())

# COMMAND ----------

# MAGIC %md
# MAGIC # Hledani

# COMMAND ----------

amb.filter(col('CISPAC') == 735265).display()


# COMMAND ----------

amb.filter(col('AMBULANT_REPORT').contains('Alina')).display()

# COMMAND ----------

amb.display()

# COMMAND ----------

# MAGIC %md
# MAGIC # Ambulantni zpravy

# COMMAND ----------

amb.orderBy('CISPAC', ascending=False).display()

# COMMAND ----------

amb.display()

# COMMAND ----------

df_amb = amb.withColumn("report_len", length(col("AMBULANT_REPORT")))

# COMMAND ----------

df_amb.display()

# COMMAND ----------

df_amb.orderBy("report_len").display()

# COMMAND ----------

df_amb.orderBy("report_len", ascending=False).display()

# COMMAND ----------

print(df_amb.orderBy("CISPAC").count())
print(df_amb.dropDuplicates(subset=["CISPAC"]).count())

# COMMAND ----------

duplicate_cispac = df_amb.groupBy("CISPAC").count().filter(col("count") > 1).select("CISPAC")
df_with_duplicates = df_amb.join(duplicate_cispac, on="CISPAC", how="inner")


# COMMAND ----------

# MAGIC %md
# MAGIC # Pacienti

# COMMAND ----------

pac.display()

# COMMAND ----------

print(pac.count())
print(pac.dropDuplicates(subset=["CISPAC"]).count())

# COMMAND ----------

# MAGIC %md
# MAGIC # Patologie

# COMMAND ----------

pat.display()

# COMMAND ----------

print(pat.count())
print(pat.dropDuplicates(subset=["CISPAC"]).count())

# COMMAND ----------

# MAGIC %md
# MAGIC # All reports

# COMMAND ----------

# all.display()

# COMMAND ----------

# all.filter(col('ALL_REPORTS').contains('Alina')).orderBy('ALL_RENTGEN_REPORTS', ascending=False).limit(50).display()

# COMMAND ----------

(all
#  .filter(col('ALL_REPORTS').contains('Pavel'))
#  .filter(col('ALL_REPORTS').contains('C50'))
 .withColumn('length_of_report', length(col('ALL_REPORTS')))
 .orderBy('length_of_report', ascending=True)
 .filter(col('length_of_report')>2000)
 .filter(col('ALL_PATHOLOGY_REPORTS').isNotNull())
 .display())

# COMMAND ----------

(all
 .filter(col('ALL_REPORTS').contains('Pavel'))
 .filter(col('ALL_REPORTS').contains('C50'))
 .withColumn('length_of_report', length(col('ALL_REPORTS')))
 .orderBy('length_of_report', ascending=True)
 .filter(col('length_of_report')>2000)
 .display())

# COMMAND ----------

(all
 .withColumn('length_of_report', length(col('ALL_REPORTS')))
 .orderBy('length_of_report', ascending=False)
 .filter(col('ALL_PATHOLOGY_REPORTS').isNotNull())
 
 .display()
 )

# COMMAND ----------

(all
 .withColumn('length_of_report', length(col('ALL_REPORTS')))
 .orderBy('length_of_report', ascending=False)
 .filter(col('ALL_REPORTS').contains('VZP'))
 .display()
 )

# COMMAND ----------

(all
 .withColumn('length_of_report', length(col('ALL_REPORTS')))
 .orderBy('length_of_report', ascending=False)
 .filter(col('ALL_REPORTS').contains('VZP'))
 .count()
 )

# COMMAND ----------

# MAGIC %md
# MAGIC # Output testing

# COMMAND ----------

(all
 .filter(col('CISPAC') == '28872')
 .display()
 )

# COMMAND ----------

(all
 .filter(col('CISPAC') == '28872')
 .display()
 )

# COMMAND ----------

# MAGIC %md
# MAGIC # Laborky

# COMMAND ----------

import pandas as pd

# COMMAND ----------

volume_path = "/Volumes/rakathon_hackathon/onkominer/source_data/023_RAKATHON/023_RAKATHON/DATA/LAB_23/BIO23/BIO23.csv"

# COMMAND ----------

lab_23 = pd.read_csv(volume_path)

# COMMAND ----------

df = spark.read.csv(volume_path, header=True, inferSchema=True)

# COMMAND ----------

df.display()

# COMMAND ----------

all.display()

# COMMAND ----------

