from sys import path
from pyspark.sql import SparkSession
from dependency_detector import logger

def readData(spark: SparkSession, path: str, file_format: str = "parquet"):
    """Load CSV or Parquet file(s) into a Spark DataFrame."""
    
    logger.info("Loading data → %s (format=%s)", path, file_format)
    
    if file_format == "csv":
        
        df = spark.read.option(
            "header", "true"
            ).option(
                "inferSchema", "true"
                ).csv(
                    path
                    )
                
    elif file_format == "parquet":
        
        df = spark.read.parquet(
            path
            )
    else:
        raise ValueError("Unsupported file format. Use 'csv' or 'parquet'.")
    
    logger.debug("Loaded DataFrame with %d rows / %d columns", df.count(), len(df.columns))
    return df