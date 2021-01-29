# Run on local
sh run.sh

# Spark Study

- [x] [Overview & install](https://spark.apache.org/docs/latest/)
- [x] [Download](https://spark.apache.org/downloads.html)
- [x] [Install on Mac](https://medium.com/beeranddiapers/installing-apache-spark-on-mac-os-ce416007d79f)

## Programming Guides:
- [x] [Quick Start](https://spark.apache.org/docs/latest/quick-start.html): a quick introduction to the Spark API; start here!
- [x] [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html): overview of Spark basics - RDDs (core but old API), accumulators, and broadcast variables
- [ ] [Spark SQL, Datasets, and DataFrames](https://spark.apache.org/docs/latest/sql-getting-started.html): processing structured data with relational queries (newer API than RDDs)

## Deployment Guides:
- [ ] [Cluster Model Overview](https://spark.apache.org/docs/latest/cluster-overview.html)
- [ ] [Submitting Application](https://spark.apache.org/docs/latest/submitting-applications.html)
  - [ ] Standalone Deploy Mode: simplest way to deploy Spark on a private cluster
  - [ ] Apache Mesos
  - [ ] Hadoop YARN
  - [ ] Kubernetes
Cluster Overview: overview of concepts and components when running on a cluster
Submitting Applications: packaging and deploying applications
Deployment modes:
Amazon EC2: scripts that let you launch a cluster on EC2 in about 5 minutes
Standalone Deploy Mode: launch a standalone cluster quickly without a third-party cluster manager
Mesos: deploy a private cluster using Apache Mesos
YARN: deploy Spark on top of Hadoop NextGen (YARN)
Kubernetes: deploy Spark on top of Kubernetes

## Other Documents:

- [ ] [Configuration](https://spark.apache.org/docs/latest/configuration.html): customize Spark via its configuration system
Monitoring: track the behavior of your applications
- [ ] [Tuning Guide](https://spark.apache.org/docs/latest/tuning.html): best practices to optimize performance and memory use
Job Scheduling: scheduling resources across and within Spark applications
Security: Spark security support
Hardware Provisioning: recommendations for cluster hardware
Integration with other storage systems:
Cloud Infrastructures
OpenStack Swift
Migration Guide: Migration guides for Spark components
Building Spark: build Spark using the Maven system
Contributing to Spark
Third Party Projects: related third party Spark projects

## External Resources:
- [ ] Code Examples: more are also available in the examples subfolder of Spark (Scala, Java, Python, R)

## Example
- [ ] [Spark Program](https://spark.apache.org/examples.html)
- [ ] [Scala](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples)
- [ ] [Python](https://github.com/apache/spark/tree/master/examples/src/main/python)

## Later
- [ ] [UnitTest](https://spark.apache.org/docs/latest/rdd-programming-guide.html#unit-testing)
- [ ] [MLlib](https://spark.apache.org/docs/latest/ml-guide.html): applying machine learning algorithms
- [ ] [GraphX](https://spark.apache.org/docs/latest/graphx-programming-guide.html): processing graphs
- [ ] [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html): processing structured data streams with relation queries (using Datasets and DataFrames, newer API than DStreams)
- [ ] Spark Streaming: processing data streams using DStreams (old API)
- [ ] [Spark Security](https://spark.apache.org/docs/latest/security.html)