# Run H2O on docker

```bash
curl -O http://h2o-release.s3.amazonaws.com/h2o/rel-zipf/4/h2o-3.32.1.4.zip
unzip h2o-3.32.1.4.zip
cd h2o-3.32.1.4
docker run --rm -it -v $(pwd):/app/h2o -p 54321:54321 --name h2o-server openjdk:15 java -jar /app/h2o/h2o.jar
```

Open http://localhost:54321/.


## Run from Python
```bash
docker run --rm -it --link h2o-server:h2o-server python:3.9.7 bash
pip install sklearn seaborn h2o==3.32.1.4
```
