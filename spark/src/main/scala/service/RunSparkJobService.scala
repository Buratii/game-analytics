package service

import org.apache.spark.sql.SparkSession
import reader.KafkaReader
import schema.EventSchema
import writer.PostgresWriter

object RunSparkJobService {
  def run(): Unit = {
    val spark = SparkSession.builder()
      .appName("GameAnalytics")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint")
      .getOrCreate()

    val kafkaBroker = sys.env.getOrElse("KAFKA_BROKER", throw new RuntimeException("KAFKA_BROKER env var not set"))
    val kafkaTopic = sys.env.getOrElse("KAFKA_TOPIC", throw new RuntimeException("KAFKA_TOPIC env var not set"))

    val postgresUser = sys.env.getOrElse("POSTGRES_USER", throw new RuntimeException("POSTGRES_USER env var not set"))
    val postgresPassword = sys.env.getOrElse("POSTGRES_PASSWORD", throw new RuntimeException("POSTGRES_PASSWORD env var not set"))
    val postgresDb = sys.env.getOrElse("POSTGRES_DB", throw new RuntimeException("POSTGRES_DB env var not set"))

    val reader = new KafkaReader(spark, kafkaTopic, EventSchema.schema, kafkaBroker)
    val eventsDF = reader.read()

    eventsDF.show()

    if (eventsDF.isEmpty) {
      println("Nenhum dado para processar.")
      return
    }

    val analytics = new EventAnalyticsService(spark, eventsDF)

    val eventCounts = analytics.countEvents()
    val uniqueUsers = analytics.countUniqueUsers()
    val avgTime = analytics.avgTimeBetweenEvents()

    val postgresUrl = s"postgres:5432/$postgresDb"

    val writer = new PostgresWriter(postgresUrl, postgresUser, postgresPassword)
    writer.write(eventCounts, "event_counts")
    writer.write(uniqueUsers, "unique_users")
    writer.write(avgTime, "avg_time_between_events")

    println("Processamento concluído!")
  }
}

