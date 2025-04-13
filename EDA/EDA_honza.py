# Databricks notebook source
from pyspark.sql import functions as f

# COMMAND ----------

# MAGIC %md
# MAGIC # EDA

# COMMAND ----------

ambulance_reports = spark.table("rakathon_hackathon.onkominer.ambulant_reports")
pac_documentation = spark.table("rakathon_hackathon.onkominer.pac_documentation")
pathology = spark.table("rakathon_hackathon.onkominer.pathology")
rentgen = spark.table("rakathon_hackathon.onkominer.rentgen")

# COMMAND ----------

ambulance_reports.display()
pac_documentation.display()
pathology.display()
rentgen.display()

# COMMAND ----------

ambulance_reports.printSchema()
pac_documentation.printSchema()
pathology.printSchema()
rentgen.printSchema()

# COMMAND ----------

from pyspark.sql import functions as f

# Total number of records
display(ambulance_reports.select(f.count("*").alias("Total Records")))

# Nulls per column
display(ambulance_reports.select([
    f.count(f.when(f.col(c).isNull(), c)).alias(c) for c in ambulance_reports.columns
]))

# Stats for numeric columns
display(ambulance_reports.select(
    "CISPAC", "EVENT_YEAR", "EVENT_MONTH", "YEAR_OF_BIRTH", "SEX", "UNKNOW_VALUE_FROM_THE_HEADER"
).summary())

# Distribution by year/month – useful for plotting
event_distribution = ambulance_reports.groupBy("EVENT_YEAR", "EVENT_MONTH").count()
display(event_distribution)  # plot as stacked bar chart or heatmap

# Gender distribution
display(ambulance_reports.groupBy("SEX").count())  # pie or bar chart


# COMMAND ----------

# Total records
display(pac_documentation.select(f.count("*").alias("Total Records")))

# Null value count
display(pac_documentation.select([
    f.count(f.when(f.col(c).isNull(), c)).alias(c) for c in pac_documentation.columns
]))

# Numeric stats
display(pac_documentation.select(
    "POR", "UDALOST_CISLO", "DELKA", "HODNOCENI", "AMBNUM", "CISPAC",
    "VEKR", "VEKM", "VEKD", "DATUM_ROK", "DATUM_MESIC", "SEX",
    "EVENT_YEAR", "EVENT_MONTH"
).summary())

# Top diagnoses from array field
diag_counts = pac_documentation.select(f.explode("DIAGNOZA").alias("DIAG")).groupBy("DIAG").count().orderBy(f.desc("count"))
display(diag_counts)  # bar chart for top diagnoses

# Most common event types
display(pac_documentation.groupBy("UDALOST").count().orderBy(f.desc("count")))  # bar chart


# COMMAND ----------

diag_counts = (
    pac_documentation.select(f.explode("DIAGNOZA").alias("DIAG")).groupBy("DIAG").count().orderBy(f.desc("count"))
    .orderBy(f.desc("count"))
    .limit(15)
    
)
display(diag_counts)

import matplotlib.pyplot as plt

diag_counts_pd = diag_counts.toPandas()

plt.figure(figsize=(10, 7))
plt.pie(diag_counts_pd['count'], labels=diag_counts_pd.apply(lambda row: f"{row['DIAG']} ({row['count']})", axis=1), autopct='%1.1f%%', startangle=140)
plt.title('Top 15 Diagnoses Distribution')
plt.axis('equal')
plt.show()

# COMMAND ----------


diag_counts = (
    pac_documentation.select(f.explode("DIAGNOZA").alias("DIAG")).groupBy("DIAG").count().orderBy(f.desc("count"))
    .orderBy(f.desc("count"))
    .limit(15)
    
)
import matplotlib.pyplot as plt

# Set up the plot
plt.figure(figsize=(10, 8))
labels = diag_counts_pd.apply(lambda row: f"{row['DIAG']} ({row['count']})", axis=1)
colors = plt.cm.tab20.colors

# Create pie chart
plt.pie(
    diag_counts_pd['count'],
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors[:len(diag_counts_pd)]
)

# Move the title upward
plt.title('Top 15 Diagnoses Distribution', fontsize=16, y=1.08)  # y > 1 moves it above the default
plt.axis('equal')  # Keeps pie chart circular
plt.tight_layout()
plt.show()


# COMMAND ----------

import pyspark.sql.functions as f

# Explode DIAGNOZA while keeping DATUM associated
diag_counts_with_DATUM = (
    pac_documentation
    .select(f.explode("DIAGNOZA").alias("DIAG"), "DATUM")
    .groupBy("DIAG", "DATUM")
    .count()
    .orderBy(f.desc("count"))
)

selected_diagnosis = 'C504'

df_filtered = diag_counts_with_DATUM.filter(f.col('DIAG') == selected_diagnosis ).filter(f.col('DATUM') != 0)
display(df_filtered)

import matplotlib.pyplot as plt

# Convert to pandas for plotting
df_pd = df_filtered.toPandas().sort_values("DATUM")

# Plot
plt.figure(figsize=(14, 6))
plt.bar(df_pd['DATUM'], df_pd['count'])

plt.title(f"Diagnosis {selected_diagnosis } Count by Date", fontsize=16)
plt.xlabel("Age", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# C504: Zhoubný novotvar prsu, Horní zevní kvadrant prsu


# COMMAND ----------

import pyspark.sql.functions as f

# Explode DIAGNOZA while keeping VEKR associated
diag_counts_with_vekr = (
    pac_documentation
    .select(f.explode("DIAGNOZA").alias("DIAG"), "VEKR")
    .groupBy("DIAG", "VEKR")
    .count()
    .orderBy(f.desc("count"))
)

df_filtered = diag_counts_with_vekr.filter(f.col('DIAG') == 'C61').filter(f.col('VEKR') != 0)
display(df_filtered)

import matplotlib.pyplot as plt

# Convert to pandas for plotting
df_pd = df_filtered.toPandas().sort_values("VEKR")

# Plot
plt.figure(figsize=(14, 6))
plt.bar(df_pd['VEKR'], df_pd['count'])

plt.title("Diagnosis C61 Count by Age", fontsize=16)
plt.xlabel("Age", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# C504: Zhoubný novotvar prsu, Horní zevní kvadrant prsu


# COMMAND ----------

display(pac_documentation)

# COMMAND ----------

# Total records
display(pathology.select(f.count("*").alias("Total Records")))

# Nulls
display(pathology.select([
    f.count(f.when(f.col(c).isNull(), c)).alias(c) for c in pathology.columns
]))

# Year-wise distribution
year_counts = pathology.groupBy("ROK").count().orderBy("ROK")
display(year_counts)  # line or bar chart by year

# Top diagnoses
display(pathology.groupBy("DG").count().orderBy(f.desc("count")))  # bar chart

# LOKAL variations
display(pathology.select("LOKAL1", "LOKAL2", "LOKAL3").distinct().limit(10))

# Sample pathology text
display(pathology.select("TEXT").where(f.col("TEXT").isNotNull()).limit(5))


# COMMAND ----------

# Total records
display(rentgen.select(f.count("*").alias("Total Records")))

# Nulls per column
display(rentgen.select([
    f.count(f.when(f.col(c).isNull(), c)).alias(c) for c in rentgen.columns
]))

# Top diagnosis codes
display(rentgen.groupBy("DG1").count().orderBy(f.desc("count")))  # bar chart

# Date range check
display(rentgen.select(f.min("VYSLDAT").alias("Earliest"), f.max("VYSLDAT").alias("Latest")))

# Summary of height and weight
display(rentgen.select("VYSKA", "HMOTNOST").summary())  # good for box plot

# Text samples
display(rentgen.select("POPIS_TEXT").where(f.col("POPIS_TEXT").isNotNull()).limit(5))


# COMMAND ----------

# MAGIC %md
# MAGIC # Selecting zpravy for demo

# COMMAND ----------

### find ambulantni zprava from selected mentor
from pyspark.sql import functions as f

# mentor_name = 'Alina Pirshtuk'
mentor_name = 'Pavel Pacas'

# Filter rows where AMBULANT_REPORT contains the mentor's name
filtered_df = ambulance_reports.filter(f.col("AMBULANT_REPORT").contains(mentor_name))

# Display the matching rows
display(filtered_df)


# COMMAND ----------

### find ambulantni zprava from selected mentor
from pyspark.sql import functions as f

# mentor_name = 'Alina Pirshtuk'
mentor_name = 'Zdeněk Linke'

# Filter rows where AMBULANT_REPORT contains the mentor's name
filtered_df = ambulance_reports.filter(f.col("AMBULANT_REPORT").contains(mentor_name))

# Display the matching rows
display(filtered_df)

# COMMAND ----------

### Report with full join
join_type = 'inner'

pac_documentation_renamed = pac_documentation.select(
    [f.col(col).alias(f"pac_documentation_{col}") for col in pac_documentation.columns] + ["CISPAC"]
)
pathology_renamed = pathology.select(
    [f.col(col).alias(f"pathology_{col}") for col in pathology.columns] + ["CISPAC"]
)
rentgen_renamed = rentgen.select(
    [f.col(col).alias(f"rentgen_{col}") for col in rentgen.columns] + ["CISPAC"]
)

ambulance_reports_inner_join = (
    ambulance_reports
    .join(pac_documentation_renamed, on="CISPAC", how=join_type)
    .join(pathology_renamed, on="CISPAC", how=join_type)
    .join(rentgen_renamed, on="CISPAC", how=join_type)
)
display(ambulance_reports_inner_join.distinct())
display(ambulance_reports_inner_join.distinct().count())

# ambulance_reports.display()
# pac_documentation.display()
# pathology.display()
# rentgen.display()

# COMMAND ----------

### Report with left join
join_type = 'left'

pac_documentation_renamed = pac_documentation.select(
    [f.col(col).alias(f"pac_documentation_{col}") for col in pac_documentation.columns] + ["CISPAC"]
)
pathology_renamed = pathology.select(
    [f.col(col).alias(f"pathology_{col}") for col in pathology.columns] + ["CISPAC"]
)
rentgen_renamed = rentgen.select(
    [f.col(col).alias(f"rentgen_{col}") for col in rentgen.columns] + ["CISPAC"]
)

ambulance_reports_left_join = (
    ambulance_reports
    .join(pac_documentation_renamed, on="CISPAC", how=join_type)
    .join(pathology_renamed, on="CISPAC", how=join_type)
    .join(rentgen_renamed, on="CISPAC", how=join_type)
)
display(ambulance_reports_left_join.distinct())

# COMMAND ----------

### find ambulantni zprava from selected mentor
from pyspark.sql import functions as f

# mentor_name = 'Alina Pirshtuk'
# mentor_name = 'Pavel Pacas'
mentor_name = 'MKN-O-3'

# Filter rows where AMBULANT_REPORT contains the mentor's name
filtered_df = ambulance_reports.filter(f.col("AMBULANT_REPORT").contains(mentor_name))

# Display the matching rows
display(filtered_df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Tring to find nice plots

# COMMAND ----------

ambulance_reports = spark.table("rakathon_hackathon.onkominer.ambulant_reports")
pac_documentation = spark.table("rakathon_hackathon.onkominer.pac_documentation")
pathology = spark.table("rakathon_hackathon.onkominer.pathology")
rentgen = spark.table("rakathon_hackathon.onkominer.rentgen")

### Report with full join
join_type = 'left'

pac_documentation_renamed = pac_documentation.select(
    [f.col(col).alias(f"pac_documentation_{col}") for col in pac_documentation.columns] + ["CISPAC"]
)
pathology_renamed = pathology.select(
    [f.col(col).alias(f"pathology_{col}") for col in pathology.columns] + ["CISPAC"]
)
rentgen_renamed = rentgen.select(
    [f.col(col).alias(f"rentgen_{col}") for col in rentgen.columns] + ["CISPAC"]
)

ambulance_reports_left_join = (
    ambulance_reports
    .join(pac_documentation_renamed, on="CISPAC", how=join_type)
    .join(pathology_renamed, on="CISPAC", how=join_type)
    .join(rentgen_renamed, on="CISPAC", how=join_type)
)

display(ambulance_reports.count())
display(ambulance_reports_left_join.distinct())
display(ambulance_reports_left_join.distinct().count())

# COMMAND ----------

from pyspark.sql import functions as f

# Step 1: Filter non-null DIAGNOZA arrays
df_diagnoza = ambulance_reports_left_join.filter(f.col("pac_documentation_DIAGNOZA").isNotNull())

# Step 2: Explode the array so each diagnosis becomes a row
df_exploded = df_diagnoza.select(
    f.explode("pac_documentation_DIAGNOZA").alias("DIAG"),
    f.col("YEAR_OF_BIRTH")
)

# Step 3: Count diagnoses per year of birth
diag_counts = (
    df_exploded
    .groupBy("DIAG", "YEAR_OF_BIRTH")
    .count()
    .orderBy(f.desc("count"))
)

# Step 4: Show the result
display(diag_counts)


# COMMAND ----------

from pyspark.sql import functions as f

# Step 1: Filter non-null DIAGNOZA arrays
df_diagnoza = ambulance_reports_left_join.filter(f.col("rentgen_DG1").isNotNull())

# Step 2: Explode the array so each diagnosis becomes a row
df_exploded = df_diagnoza.select(
    f.col('rentgen_DG1'),
    f.col("YEAR_OF_BIRTH")
)

# Step 3: Count diagnoses per year of birth
diag_counts = (
    df_exploded
    .groupBy("rentgen_DG1", "YEAR_OF_BIRTH")
    .count()
    .orderBy(f.desc("count"))
)

# Step 4: Show the result
display(diag_counts)
