# use below if error comes chmod -R 777 Invoice
import logging
logging.getLogger().handlers = []
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
logger = logging.getLogger(__name__)

class readingInvoice:   
    
    def __init__(self):
        logger.info("Initializing readingInvoice class")
        from pyspark.sql import SparkSession

        try:
            self.spark = SparkSession.builder.appName("streaming example").getOrCreate()
            self.base_dir = "/home/jovyan/work/Invoice/"
            logger.info(f"Spark session initialized successfully")
        except Exception as e:
            logger.exception(f"Error initializing readingInvoice class: {e}")
            raise e

    def getSchema(self):
        logger.info("Getting schema")
        from pyspark.sql.types import (
            StructType,
            StructField,
            StringType,
            LongType,
            DoubleType,
            ArrayType,
        )

        schema = StructType(
            [
                StructField("CESS", DoubleType(), True),
                StructField("CGST", DoubleType(), True),
                StructField("CashierID", StringType(), True),
                StructField("CreatedTime", LongType(), True),
                StructField("CustomerCardNo", StringType(), True),
                StructField("CustomerType", StringType(), True),
                StructField(
                    "DeliveryAddress",
                    StructType(
                        [
                            StructField("AddressLine", StringType(), True),
                            StructField("City", StringType(), True),
                            StructField("ContactNumber", StringType(), True),
                            StructField("PinCode", StringType(), True),
                            StructField("State", StringType(), True),
                        ]
                    ),
                ),
                StructField("DeliveryType", StringType(), True),
                StructField(
                    "InvoiceLineItems",
                    ArrayType(
                        StructType(
                            [
                                StructField("ItemCode", StringType(), True),
                                StructField("ItemDescription", StringType(), True),
                                StructField("ItemPrice", DoubleType(), True),
                                StructField("ItemQty", DoubleType(), True),
                                StructField("TotalValue", DoubleType(), True),
                                StructField("ItemName", StringType(), True),
                            ]
                        )
                    ),
                ),
                StructField("InvoiceNumber", StringType(), True),
                StructField("NumberOfItems", LongType(), True),
                StructField("PaymentMethod", StringType(), True),
                StructField("PosID", StringType(), True),
                StructField("SGST", DoubleType(), True),
                StructField("StoreID", StringType(), True),
                StructField("TaxableAmount", DoubleType(), True),
                StructField("TotalAmount", DoubleType(), True),
            ]
        )
        logger.info("Schema retrieved successfully")
        return schema

    def getRawData(self):
        logger.info("Getting raw data")
        try:
            df = self.spark.readStream.format("org.apache.spark.sql.json") \
                 .schema(self.getSchema()) \
                 .load(f"{self.base_dir}/invoices-1.json" )            
            logger.info("Raw data retrieved successfully")
            df.printSchema()
        except Exception as e:
            logger.exception(f"Error getting raw data: {e}")
        return df

    def validateData(self, schema, rawData):
        logger.info("Validating data")
        logger.info("Data validated successfully")
        return rawData
        # from pyspark.sql.functions import from_json, col
        # validatedData = rawData.withColumn("parsed", from_json(col("value"), schema))
        # invalid_rows = validatedData.filter(col("parsed").isNull())
        # valid_rows = validatedData.filter(col("parsed").isNotNull())
        # return valid_rows
        # return validatedData

    def getFlattenedData(self, rawData):
        logger.info("Flattening data")
        import pyspark.sql.functions as F
        from pyspark.sql.functions import col

        try:
            rawDataFlattened = rawData.select(
            "CESS",
            "CGST",
            "CashierID",
            "CreatedTime",
            "CustomerCardNo",
            "CustomerType",
            F.col("DeliveryAddress.AddressLine").alias("DeliveryAddress_AddressLine"),
            F.col("DeliveryAddress.City").alias("DeliveryAddress_City"),
            F.col("DeliveryAddress.ContactNumber").alias(
                "DeliveryAddress_ContactNumber"
            ),
            F.col("DeliveryAddress.PinCode").alias("DeliveryAddress_PinCode"),
            F.col("DeliveryAddress.State").alias("DeliveryAddress_State"),
            "DeliveryType",
            F.col("InvoiceLineItems.ItemCode").alias("InvoiceLineItems_ItemCode"),
            F.col("InvoiceLineItems.ItemDescription").alias(
                "InvoiceLineItems_ItemDescription"
            ),
            F.col("InvoiceLineItems.ItemPrice").alias("InvoiceLineItems_ItemPrice"),
            F.col("InvoiceLineItems.ItemQty").alias("InvoiceLineItems_ItemName"),
            F.col("InvoiceLineItems.TotalValue").alias("InvoiceLineItems_TotalValue"),
            "InvoiceNumber",
            "NumberOfItems",
            "PaymentMethod",
            "PosID",
            "SGST",
            "StoreID",
            "TaxableAmount",
            )
        # rawDataFlattened.drop("CESS", "CGST", "SGST", "PosID", "StoreID")
        except Exception as e:
            logger.exception(f"Error flattening data: {e}")
            raise e
        return rawDataFlattened

    def writeData(self, flattenedData):
        logger.info("Writing data")
        import os
        output_path = f"{self.base_dir}/flattened"        
        os.makedirs(output_path, exist_ok=True)
        logger.info(f"file path is : {output_path}")
        checkpoint_path = f"{self.base_dir}/_checkpoints/flattened/"
        try:
            query = flattenedData.writeStream \
                .format("parquet") \
                .option("path", output_path) \
                .option("checkpointLocation", checkpoint_path) \
                .outputMode("append") \
                .start()
            logger.info("Data writing started successfully")
            return query
        except Exception as e:
            logger.exception(f"Error writing data: {e}")
            raise e
        logger.info("Data written successfully")
        return


if __name__ == "__main__":
   
    
    rd = readingInvoice()
    rawData = rd.getRawData()
    schema = rd.getSchema()
    validateData = rd.validateData(schema, rawData)
    flattenedData = rd.getFlattenedData(validateData)

    #rawData.show(n=1, vertical=True)
    # print(schema)
    #flattenedData.printSchema()
    rd.writeData(flattenedData)
