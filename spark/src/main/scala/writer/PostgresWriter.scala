package writer

import org.apache.spark.sql.{DataFrame, SaveMode}
import java.util.Properties

class PostgresWriter(
                      jdbcUrl: String,
                      user: String,
                      password: String,
                      driver: String = "org.postgresql.Driver"
                    ) {

  private val connectionProperties = new Properties()
  connectionProperties.put("user", user)
  connectionProperties.put("password", password)
  connectionProperties.put("driver", driver)

  def write(df: DataFrame, tableName: String): Unit = {
    val fullJdbcUrl = s"jdbc:postgresql://$jdbcUrl"

    df.write
      .mode(SaveMode.Append)
      .jdbc(fullJdbcUrl, tableName, connectionProperties)
  }
}
