package spark

import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.{cume_dist, dense_rank, lag, last, lead, lit, max, monotonically_increasing_id, nth_value, percent_rank, rank, row_number, sum, to_date, window}
import org.apache.spark.sql.types.TimestampType

/**
 * rowsBetween
 * - Window.unboundedPreceding : indicates that the window starts at the first row of the partition
 * - Window.currentRow : indicates the window begins or ends at the current row
 * - Window.unboundedFollowing : indicates that the window ends at the last row of the partition
 * -
 */
class Windows {
  val spark: SparkSession = SparkSessions.createSparkSession()
  import spark.implicits._

  private val df: DataFrame = Read.getParquetDataFrame()
  df.drop()
    df.withColumn("num",
      row_number.over(
        //window 범위 설정
        Window
          .partitionBy("pattern_id", "error_message")
          .orderBy("pattern_id", "error_message")

          //default
          //  - orderBy가 있으면, 처음부터 현재 row까지
          //  - orderBy가 없으면, 처음부터 끝까지
          // 현재 row를 기준으로 +,- 범위 설정
          .rowsBetween(Window.unboundedPreceding, Window.currentRow)
      )
    )

  def window_functions() = {
    row_number()//frame내에서 순서(공통된 값이 있어도, 정렬된 순서에 따라 숫자가 정해짐
    rank()//공동1등이 있으면, 둘다 1이 되고, 그 다음은 3임.
    dense_rank()//공통1등이 있으면, 둘다 1이 되고, 그 다음은 2임.
    nth_value($"col_name", 5)//window에서 몇번째 row
    percent_rank() // percentile 형식으로 rank를 매김. 0, 0.5, 1 이런식으로. percentile로 seg를 구분할 때 사용.
  }

  def row_number_by_saved_order() = {
    row_number().over(Window.orderBy(lit(1))) // 1부터 시작
    monotonically_increasing_id() //순서대로 숫자가 정해짐. 0부터 시작
  }

  def getFirstRowOfGroup() = {
    import org.apache.spark.sql.SaveMode
    import org.apache.spark.sql.expressions.Window

    val w = Window.partitionBy("type").orderBy("type")
    df.withColumn("rn", row_number.over(w))
      .where($"rn" === 1).drop("rn")
      .write
      .mode(SaveMode.Overwrite)
      .parquet("s3://hyun/temp/test")
  }

  def aggregateColumnByGroup() = {
    val w = Window.partitionBy("name").orderBy($"date".desc)
    Seq(
      ("a", "2021-05-20"),
      ("a", "2021-05-21"),
      ("a", "2021-05-22"),
      ("a", "2021-05-23"),
      ("b", "2021-04-20"),
      ("b", "2021-04-21"),
      ("b", "2021-04-22"),
      ("b", "2021-04-23")
    ).toDF("name", "date")
      .withColumn("date", to_date($"date"))
      .withColumn("last_time", max($"date").over(w))
      .show()
  }

  def groupByDateRange() = {
    val a = Seq(System.currentTimeMillis() / 1000,2,3,4,5)

    a.toDF().withColumn("date", $"value".cast(TimestampType))
      .groupBy(window($"date", "1 day"))
      .count()

      .show(truncate = false)

    //    [1970-01-01 00:00:00, 1970-01-02 00:00:00]	4
    //    [2021-02-17 00:00:00, 2021-02-18 00:00:00]	1
  }

  def cumulate() = {
    //value로 오름차순해서, 누적 합계를 보여준다.
    df.withColumn("cum_sum", sum("value").over(Window.orderBy("value")))
  }

  def totalSumCumSum() = {
//    val w_group = Window.partitionBy("group").orderBy($"count".desc)
    val w_from_first_to_current = Window.partitionBy("group").orderBy($"count".desc)
      .rowsBetween(Window.unboundedPreceding, Window.currentRow)

    df
      //todo check bug reason :if use same partitionBy column on different window. only last window is reflected.
//      .withColumn("total_count_over_group", sum($"count").over(w_group))
      .withColumn("cum_count_over_group", sum($"count").over(w_from_first_to_current))
  }

  /**
   * 전체를 1로 봤을 때, 현재의 row가 몇번 째에 있는지를 나타냄
   * todo percent_rank 와 차이점은?
   * +---+------+------------------+
    | id|bucket|         cume_dist|
    +---+------+------------------+
    |  0|     0|0.3333333333333333|
    |  3|     0|0.6666666666666666|
    |  6|     0|               1.0|
    |  1|     1|0.3333333333333333|
    |  4|     1|0.6666666666666666|
    |  7|     1|               1.0|
    |  2|     2|0.3333333333333333|
    |  5|     2|0.6666666666666666|
    |  8|     2|               1.0|
    +---+------+------------------+
   */
  def cume_dists(df: DataFrame) = {
    val windowSpec = Window.partitionBy('bucket).orderBy('id)
    df.withColumn("cume_dist", cume_dist over windowSpec).show
  }

  /**
   * 이전 row 값 조회.
   * lag는 뒤쳐지다는 의미. 다음 row들을 조회하는데, 뒤쳐진 이전 row들의 값을 보여줌.
   */
  def lags(df: DataFrame) = {
    val windowSpec = Window.partitionBy('bucket).orderBy('id)
    df.withColumn("lag", lag('id, 1) over windowSpec).show
  }

  /**
   * window상에 마지막 값을 가져오는데, null을 제외할지 설정할 수 있음
   * 가령, 현재 row의 이전 row들 중에서 null이 아닌 마지막 값을 가져오고 싶으면, lag와 결합해서 쓰면 됨
   */
  def lasts(df: DataFrame) = {
    val windowSpec = Window.partitionBy('bucket).orderBy('id)
    df.withColumn("last", last('id, true) over windowSpec).show
  }

  /**
   * 이후 row 값 조회.
   * 먼저 리드해서, 다음 값을 보여줌.
   * default로 첫번째 row에서 현재row까지가 확인 범위인데,
   * 확인 범위 밖에 있는 값을 보여주네?? lead만의 별도의 로직이 있는듯..
   */
  def leads(df: DataFrame) = {
    val windowSpec = Window.partitionBy('bucket).orderBy('id)
    df.withColumn("lead", lead('id, 1) over windowSpec).show
  }

  def totalCount(df: DataFrame) = {
    //전체 groupby내에서 전체 count를 구하기. 보통, df.count()를 가져와서, total을 구하는데, 이렇게 하면, 동일한 job내에서 처리 가능한 듯? 테스트 해보지 못했고, 성능이 괜찮은지는 잘 모름.
    df.withColumn("total_count", sum($"count").over(Window.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)))
  }
}
