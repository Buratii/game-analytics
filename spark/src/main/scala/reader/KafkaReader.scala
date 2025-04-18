package reader

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.functions._

class KafkaReader(spark: SparkSession, topic: String, schema: StructType, bootstrapServer: String) {
  import spark.implicits._

  def read(): DataFrame = {
    try {
      val df = spark.read
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrapServer)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .option("endingOffsets", "latest")
        .load()
        .orderBy(desc("timestamp"))

      if (df.isEmpty) {
        println("Nenhum dado novo desde a última run.")
        return spark.emptyDataFrame
      }

      df.selectExpr("CAST(value AS STRING)")
        .select(org.apache.spark.sql.functions.from_json($"value", schema).as("data"))
        .select("data.*")

    } catch {
      case e: org.apache.kafka.common.errors.UnknownTopicOrPartitionException =>
        println(s"Tópico $topic não encontrado. Tentando novamente em breve...")
        spark.emptyDataFrame
      case e: Exception =>
        println(s"Erro ao ler do Kafka: ${e.getMessage}")
        spark.emptyDataFrame
    }
  }

}
