import service.RunSparkJobService

import java.time.LocalDateTime

object Main {
  private val INTERVAL = 60000

  def main(args: Array[String]): Unit = {
    while (true) {
      println(s"Running Spark job at ${LocalDateTime.now()}")

      RunSparkJobService.run()

      println(s"Sleeping for 60 seconds...")
      Thread.sleep(INTERVAL)
    }
  }
}
