# MLOps ODS
This project for ml model with MLOps instruments

the methodology of repo (GitHub flow - one main branch, and developing in other brunches):
- main branch: 'master'
- other branches: 'fix-', 'feature-', 'model-', 'experiment-'

```commandline
poetry build --format=wheel
```

Docker image (build / run):
```commandline
docker build . -t mlops_ods_image
docker run -it mlops_ods_image /bin/bash
```
build for linux:
```commandline
docker build . -t mlops_ods_image --platform linux/amd64
```
run with port and volumes if necessary:
```commandline
docker run -p 8888:8888 -v {path-to-local-folder-(pwd)}:/app/volumes -it mlops_ods_image /bin/bash
```

documentation of jupyter notebooks with quarto:
```commandline
quarto render

quarto preview  src/mlops_ods/notebooks/eda.ipynb
quarto render src/mlops_ods/notebooks/eda.ipynb --to html
```

snakemake command inside docker:
```commandline
snakemake --cores 10
snakemake --dag | dot -Tsvg > dag.svg

docker ps
docker cp <CONTAINER ID>:/app/dag.svg .
```
