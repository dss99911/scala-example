# GPU 이해

## 메모리
https://blog.naver.com/julie_eun1014/221116312880

### on-chip
gpu칩 안에 있는 레지스터 메모리

### off-chip
DRAM
글로벌/디바이스 메모리라고도 함

#### 메모리 할당 방법
GPU 포인터를 선언 -> cudaMalloc 명령으로 메모리 할당해주기 -> 메모리 해제(cudaFree)

cudaMemcpy로 cpu메모리의 데이터를 gpu메모리로 전송. gpu처리 완료후, gpu메모리에서 cpu로 전송

### Shared Memory
off-chip은 시간이 오래 걸리므로, 캐시처럼 사용할 수 있는 메모리 공간
cpu의 캐시공간과 달리, 개발자가 데이터를 캐시에 설정가능하다고 함. syncthreads()를 통해서 설정하고, 블록마다 공유 메모리가 있어, 블럭안의 스레드들에서 공유 가능함.

### pinning memory
cudaHostAlloc을 사용하면, GPU와 통신하는 CPU메모리 공간 강제 할당하여, 통신 속도 향상

### Unified Memory
CPU와 GPU가 동시에 같은 메모리 포인터를 사용할 수 있게 한 CUDA 6.0의 새로운 기능
cudaMalloc이나 cudaMemcpy 대신에
cudaMallocManaged 함수를 사용하여 쉽게 GPU 병렬화 작업을 할 수 있음





# Spark with GPU

## Reference
- [book](https://images.nvidia.com/aem-dam/Solutions/deep-learning/deep-learning-ai/solutions/Accelerating-Apache-Spark-3-08262021.pdf)
  - [korean](https://www.nvidia.com/ko-kr/ai-data-science/spark-ebook/getting-started-spark-3/)
- [Get Started](https://nvidia.github.io/spark-rapids/docs/get-started/getting-started-aws-emr.html)
  - [AWS doc](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-rapids.html)
  - UCX라는 것을 통해, shuffle시간을 gpu를 통해 개선할 수 있다
  - com.nvidia.spark.SQLPlugin 라는 내부 플러그인을 사용하는데, 제대로 설정안하면, CPU사용 함
- [Get Started on AWS EMR](https://nvidia.github.io/spark-rapids/docs/get-started/getting-started-aws-emr.html)
  - jar를 spark에 돌릴려면 local에서 jar를 빌드해야 하는데, xgboost4j-spark jar는 scala 3.0을 사용하여 jar를 직접 추가해야 함.
  - [Using EMR notebook](https://github.com/NVIDIA/spark-xgboost-examples/blob/spark-2/getting-started-guides/csp/aws/Using_EMR_Notebook.md)
    - EMR jupyter notebook에서 GPU사용하기
    - notebook은 Livy를 통해서 spark와 통신함
  - [multiple GPU](https://github.com/NVIDIA/spark-xgboost-examples/blob/spark-2/advanced-topics/multi-gpu.md)
    - 하나의 노드에 gpu가 여러개인 경우, executor수는 gpu수와 같거나 작아야 함.
    - 뭔가 추가적으로 설정해줘야 하는 듯.
- [Xgboost Spark GPU]()

## Samples
- [Agaricus - Scala](https://github.com/NVIDIA/spark-xgboost-examples/blob/spark-3/examples/notebooks/scala/agaricus-gpu.ipynb)
  - model fit하면 features가 없다는 에러남(features does not exist. Available)
- [AWE EMR with pyspark](https://github.com/NVIDIA/spark-rapids/blob/main/docs/demo/AWS-EMR/Mortgage-ETL-GPU-EMR.ipynb)


## Understanding
1. Spark 3.0부터 plugin을 사용하면, GPU를 사용할 수 있게 됨.
2. cuDF, RAPIDS Accelerator, xgboost4j-spark는 EMR cluster에 이미 설치되어 있음
   1. xgboost 라이브러리를 jar추가 없이도 사용할 수 있고, explain을 했을 때 GPU를 쓴다고 되어 있는게 그 근거
3. xgboost featureCol에 vector대신에 컬럼 리스트를 입력할 수 있음.
   1. https://xgboost.readthedocs.io/en/latest/jvm/xgboost4j_spark_gpu_tutorial.html
      1. 2021년 최신 버전(xgboost에서 공식 지원) : https://mvnrepository.com/artifact/ml.dmlc/xgboost4j-gpu_2.12/1.3.1
         1. https://s3-us-west-2.amazonaws.com/xgboost-maven-repo
      2. 2020년 버전(nvidia로 이관) : https://mvnrepository.com/artifact/com.nvidia/xgboost4j-spark_3.0/1.2.0-0.1.0
      3. 2019년 (ai.rapids에서 시작) : https://mvnrepository.com/artifact/ai.rapids/xgboost4j
   2. EMR에서 features doesn't not exist 에러가 뜸. xgboost4j-gpu 1.6.0이 stable해지면, 시도해보는게 좋을듯(EMR문서상 해당 기능이 공식적으로 가능한 것은 아닌 것 같음)

## TODO
- spark.conf.set('spark.rapids.sql.enabled','true')

## 직접설치
- https://nvidia.github.io/spark-rapids/docs/get-started/getting-started-on-prem.html
- cuda 설치
  - GPU 하드웨어 관련,
  - 재시작 필요
- cudf 설치
  - cuda버전에 맞춰야 함
- rapids 설치
  - cudf버전에 맞춰야 함
- Install the GPU Discovery Script
- setting Yarn config

## EMR에 최신버전 설치
- http://www.openkb.info/2021/04/how-to-use-latest-version-of-rapids.html
- Install CUDA Toolkit 11.0 and cuda-compat-11-0

## [Qualification profiling tool](https://nvidia.github.io/spark-rapids/docs/get-started/getting-started-workload-qualification.html)
- gpu로 migration하기 이전에, 어떤 작업들을 gpu로 수행가능한지 확인가능

## [Tuning](https://nvidia.github.io/spark-rapids/docs/tuning-guide.html)

- spark.task.resource.gpu.amount
  - 한 task가 사용하는 gpu양
  - 소수. 한 executor의 각 core가 task를 처리할 때, 사용할 수 있는 gpu의 비율.
  - 1이면, 한 task가 gpu전체를 사용
  - 8개 core가 있고, 값이 0.125이면, 각 core의 task가 1/8만큼의 gpu를 나눠서 사용
- spark.executor.resource.gpu.amount
  - 한 executor가 가지는 gpu 갯수
- spark.executor.cores
  - It is recommended to run more than one concurrent task per executor as this allows overlapping I/O and computation. For example one task can be communicating with a distributed filesystem to fetch an input buffer while another task is decoding an input buffer on the GPU. Configuring too many concurrent tasks on an executor can lead to excessive I/O, overload host memory, and spilling from GPU memory. Counter-intuitively leaving some CPU cores idle may actually speed up your overall job. We typically find that two times the number of concurrent GPU tasks is a good starting point.
  

## Outdated References
- https://github.com/NVIDIA/spark-rapids/blob/branch-22.06/docs/get-started/getting-started.md
- https://xgboost.readthedocs.io/en/latest/jvm/xgboost4j_spark_gpu_tutorial.html
- https://medium.com/@nhanwei/xgboost-with-spark-on-gpu-abddfd78d091
    - jar직접 다운 받아서 실행
    - pyspark
- https://developer.nvidia.com/blog/gpu-accelerated-spark-xgboost/
    - 옛날 방식인듯 2019년
