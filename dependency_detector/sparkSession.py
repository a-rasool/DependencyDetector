from pyspark.sql import SparkSession
from dependency_detector import logger

def getSparkSession(app_name="DependencyDetector", memory="4g"):

    logger.info("Creating SparkSession — app_name=%s, memory=%s", app_name, memory)
    
    spark = (
        SparkSession.builder
        .master("local[*]")                     # ← always use local JVM
        .appName(app_name)
        .config("spark.driver.bindAddress", "127.0.0.1")  # ← NEW: pin the bind IP
        .config("spark.driver.host", "127.0.0.1")         #    (extra safety)
        .config("spark.driver.memory", memory)
        .config("spark.sql.shuffle.partitions", "200")
        .getOrCreate()
    )
    
    logger.debug("SparkSession created: %s", spark)
    
    return spark

if __name__ == "__main__":
    pass