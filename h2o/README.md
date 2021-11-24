# Run H2O on docker

```bash
curl -O http://h2o-release.s3.amazonaws.com/h2o/rel-zipf/4/h2o-3.32.1.4.zip
unzip h2o-3.32.1.4.zip
docker run --rm -it \
  -v $(pwd)/h2o-3.32.1.4:/app/h2o \
  -v notebook:/root/h2oflows/notebook \
  -p 54321:54321 \
  --name h2o-server \
  openjdk:15 \
  java -jar /app/h2o/h2o.jar
```

Open http://localhost:54321/.


## Run from Python
```bash
docker build -t h2o-python python   # build image under python directory.
docker run --rm -it --link h2o-server:h2o-server --name h2o-python h2o-python python
```

Access h2o server from python.

```
>>> import h2o
>>> h2o.init(url="http://h2o-server:54321")
Checking whether there is an H2O instance running at http://h2o-server:54321 . connected.
Warning: Your H2O cluster version is too old (4 months and 15 days)! Please download and install the latest version from http://h2o.ai/download/
--------------------------  ---------------------------------------------------------
H2O_cluster_uptime:         2 hours 2 mins
H2O_cluster_timezone:       UTC
H2O_data_parsing_timezone:  UTC
H2O_cluster_version:        3.32.1.4
H2O_cluster_version_age:    4 months and 15 days !!!
H2O_cluster_name:           root
H2O_cluster_total_nodes:    1
H2O_cluster_free_memory:    3.904 Gb
H2O_cluster_total_cores:    5
H2O_cluster_allowed_cores:  5
H2O_cluster_status:         locked, healthy
H2O_connection_url:         http://h2o-server:54321
H2O_connection_proxy:       null
H2O_internal_security:      False
H2O_API_Extensions:         Amazon S3, Algos, AutoML, Core V3, TargetEncoder, Core V4
Python_version:             3.9.7 final
--------------------------  ---------------------------------------------------------
```
