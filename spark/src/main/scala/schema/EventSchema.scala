package schema

import org.apache.spark.sql.types._

object EventSchema {
  val schema: StructType = StructType(Array(
    StructField("user_id", IntegerType),
    StructField("event_type", StringType),
    StructField("timestamp", TimestampType),
    StructField("game_id", IntegerType),
    StructField("payload", MapType(StringType, StringType))
  ))
}
