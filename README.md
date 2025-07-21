⚡ Scalable Enterprise Streaming with Spark + Kafka

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

✅ Key Features

    ✅ Exactly-once Semantics with Kafka + Spark checkpointing

    ✅ Explodes nested arrays for line-item level granularity

    ✅ Supports large volumes via Kafka partitioning & Spark parallelism

    ✅ Modular, testable code with parameterized paths

    ✅ Schema-first design using StructType for robust ETL

| Component     | Technology                        |
| ------------- | --------------------------------- |
| Messaging     | Apache Kafka                      |
| Processing    | Apache Spark Structured Streaming |
| Storage       | Parquet + HDFS / S3               |
| Serialization | JSON (with schema)                |
| Language      | Python (PySpark)                  |
| Coordination  | Spark Checkpointing (HDFS/Cloud)  |

Invoice-Streaming/
│
├── README.md
├── main.py                # Driver script
├── invoice_processor.py   # Class-based pipeline (read, validate, flatten, write)
├── config/
│   └── logging.yaml       # Custom logging config
├── data/
│   ├── raw/               # Landing zone for incoming Kafka batch (simulated here)
│   └── flattened/         # Output zone (Parquet format)
└── checkpoints/
    └── invoice/           # Spark checkpoints (required for exactly-once)

🛡️ Exactly-Once Semantics Explained

I'm building this project to ensure exactly-once delivery semantics from Kafka to my Spark Structured Streaming jobs. Here's how I plan to achieve it (and will keep this section updated as I progress):

    ✅ I use Kafka's built-in offset tracking to keep track of processed messages

    ✅ I'm setting a checkpointLocation in Spark (on HDFS, MinIO, or local disk) to store streaming state and enable fault tolerance

    ⏳ I'm working on using append mode and trigger once/micro-batch options in Spark to ensure consistent writes

    ⏳ I plan to implement idempotent writes by using deterministic paths and ensuring output directories don’t overwrite partially written files

    🚧 As I scale, I’ll monitor for duplicates and tune the system to maintain delivery guarantees at large volume

