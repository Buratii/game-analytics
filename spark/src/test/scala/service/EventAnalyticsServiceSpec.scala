package service

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.scalatest.funsuite.AnyFunSuite
import org.scalatest.BeforeAndAfterAll
import java.sql.Timestamp

class EventAnalyticsServiceSpec extends AnyFunSuite with BeforeAndAfterAll {

  private val spark = SparkSession.builder()
    .appName("EventAnalyticsServiceTest")
    .master("local[*]")
    .getOrCreate()

  import spark.implicits._

  private val testData = Seq(
    ("user1", "login", Timestamp.valueOf("2023-01-01 10:00:00")),
    ("user1", "click", Timestamp.valueOf("2023-01-01 10:05:00")),
    ("user1", "logout", Timestamp.valueOf("2023-01-01 10:15:00")),
    ("user2", "login", Timestamp.valueOf("2023-01-01 11:00:00")),
    ("user2", "click", Timestamp.valueOf("2023-01-01 11:10:00")),
    ("user3", "login", Timestamp.valueOf("2023-01-01 12:00:00")),
    ("user3", "click", Timestamp.valueOf("2023-01-01 12:01:00")),
    ("user3", "click", Timestamp.valueOf("2023-01-01 12:05:00")),
    ("user3", "logout", Timestamp.valueOf("2023-01-01 12:10:00"))
  ).toDF("user_id", "event_type", "timestamp")

  private val service = new EventAnalyticsService(spark, testData)

  override def afterAll(): Unit = {
    spark.stop()
  }

  /**
   * Helper method to compare DataFrames ignoring the processed_at timestamp
   * which can change between test runs
   */
  private def compareDataFrames(actual: DataFrame, expected: DataFrame, columns: Seq[String]): Boolean = {
    val actualFiltered = actual.select(columns.head, columns.tail: _*).collect().sortBy(_.toString())
    val expectedFiltered = expected.select(columns.head, columns.tail: _*).collect().sortBy(_.toString())
    actualFiltered.sameElements(expectedFiltered)
  }

  test("countEvents should count events grouped by event_type") {
    // Execute
    val result = service.countEvents()

    // Create expected result
    val expectedData = Seq(
      ("login", 3L),
      ("click", 4L),
      ("logout", 2L)
    ).toDF("event_type", "total_events")
      .withColumn("processed_at", lit(null).cast(TimestampType))

    // Verify column structure
    assert(result.columns.toSet === Set("event_type", "total_events", "processed_at"))

    // Verify data (ignoring processed_at timestamp)
    assert(compareDataFrames(result, expectedData, Seq("event_type", "total_events")))
  }

  test("countUniqueUsers should count unique users for each event type") {
    val result = service.countUniqueUsers()

    val expectedData = Seq(
      ("login", 3L),
      ("click", 3L),
      ("logout", 2L)
    ).toDF("event_type", "unique_users")
      .withColumn("processed_at", lit(null).cast(TimestampType))

    // Verify column structure
    assert(result.columns.toSet === Set("event_type", "unique_users", "processed_at"))

    // Verify data (ignoring processed_at timestamp)
    assert(compareDataFrames(result, expectedData, Seq("event_type", "unique_users")))
  }

  test("avgTimeBetweenEvents should calculate average time between events for each user") {
    val result = service.avgTimeBetweenEvents()

    // Expected time differences (in seconds)
    // user1: (300 + 600) / 2 = 450 seconds average (5 min + 10 min between 3 events)
    // user2: 600 seconds (10 min between 2 events)
    // user3: (60 + 240 + 300) / 3 = 200 seconds average (1 min + 4 min + 5 min between 4 events)

    // Verify column structure
    assert(result.columns.toSet === Set("user_id", "avg_time_between_events_seconds", "processed_at"))

    // Collect results and convert to a map for easier verification
    val resultMap = result.select("user_id", "avg_time_between_events_seconds")
      .collect()
      .map(row => (row.getString(0), row.getDouble(1)))
      .toMap

    // Verify average times for each user with tolerance for floating point precision
    assert(math.abs(resultMap("user1") - 450.0) < 1.0)
    assert(math.abs(resultMap("user2") - 600.0) < 1.0)
    assert(math.abs(resultMap("user3") - 200.0) < 1.0)
  }
}