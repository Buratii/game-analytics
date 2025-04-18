package service

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

class EventAnalyticsService(spark: SparkSession, eventsDF: DataFrame) {

  import spark.implicits._

  def countEvents(): DataFrame = {
    eventsDF.createOrReplaceTempView("events")
    spark.sql("""
      SELECT event_type, COUNT(*) as total_events, CURRENT_TIMESTAMP() as processed_at
      FROM events
      GROUP BY event_type
    """)
  }

  def countUniqueUsers(): DataFrame = {
    spark.sql("""
      SELECT event_type, COUNT(DISTINCT user_id) as unique_users, CURRENT_TIMESTAMP() as processed_at
      FROM events
      GROUP BY event_type
    """)
  }

  def avgTimeBetweenEvents(): DataFrame = {
    val withNext = spark.sql("""
      SELECT user_id, event_type, timestamp,
             LEAD(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as next_event_time
      FROM events
    """)

    withNext
      .filter($"next_event_time".isNotNull)
      .withColumn("time_diff_seconds", unix_timestamp($"next_event_time") - unix_timestamp($"timestamp"))
      .groupBy("user_id")
      .agg(
        avg("time_diff_seconds").as("avg_time_between_events_seconds"),
        current_timestamp().as("processed_at")
      )
  }
}
