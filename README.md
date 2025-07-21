a# ⚡ Scalable Enterprise Streaming with Spark + Kafka

> 🚀 Real-time data pipeline handling **gigabytes to petabytes** of streaming data  
> 🛡️ Implements **exactly-once delivery semantics** using Kafka, Spark Structured Streaming, and checkpointing  
> 🏗️ Designed for **enterprise-grade production use** with modular architecture and fault tolerance

---

## 📦 Overview

This project demonstrates a scalable real-time streaming architecture using:
- **Apache Kafka** for ingestion and distributed messaging
- **Apache Spark Structured Streaming** for processing large-scale JSON invoice data
- **Parquet + HDFS/S3/MinIO** for durable, columnar output storage
- **Exactly-once semantics** to avoid data duplication or loss
- Clean logging, modular design, and extensible schema handling

---

## 🧱 Architecture

```text
[ Producers (POS / Sensors / APIs) ]
              ↓
        ┌─────────────┐
        │ Apache Kafka│  ← High-throughput ingest (Partitions = scale)
        └─────────────┘
              ↓
   ┌─────────────────────────────┐
   │ Spark Structured Streaming  │
   │ - Schema enforcement        │
   │ - JSON parsing & flattening │
   │ - explode() array data      │
   │ - Exactly-once checkpointing│
   └─────────────────────────────┘
              ↓
     ┌─────────────────────┐
     │ Parquet Output Store│ ← HDFS / S3 / File_dir
     └─────────────────────┘
