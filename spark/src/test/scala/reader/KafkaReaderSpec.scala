package reader

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.scalatest.funsuite.AnyFunSuite
import org.scalatest.BeforeAndAfterAll

class KafkaReaderSpec extends AnyFunSuite with BeforeAndAfterAll {

  private val spark = SparkSession.builder()
    .appName("KafkaReaderTest")
    .master("local[*]")
    .getOrCreate()

  override def afterAll(): Unit = {
    spark.stop()
  }


  test("KafkaReader should correctly parse JSON messages from Kafka") {
    import spark.implicits._

    val schema = new StructType()
      .add("id", IntegerType)
      .add("name", StringType)

    val jsonData = Seq("""{"id":1, "name":"Alice"}""", """{"id":2, "name":"Bob"}""")
    val kafkaDF = jsonData.toDF("value")  // mimics DataFrame returned from Kafka read

    val transformedDF = kafkaDF
      .select(from_json($"value", schema).as("data"))
      .select("data.*")

    val expected = Seq((1, "Alice"), (2, "Bob")).toDF("id", "name")

    assert(transformedDF.collect().sameElements(expected.collect()))
  }
}
