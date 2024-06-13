# Snakemake dag
1a) read data from kaggle
2a) preprocess data as baseline and save to "preproc_data_base"
2b) preprocess data as research and save to "preproc_data_research"
3a) fit small model with data 2a and save to "model_base"
3b) fit small model with data 2b and save to "model_research"
3c) fit large model with data 2a and save to "model_bigger_base"
3d) fit large model with data 2b and save to "model_bigger_research"

![Alt text](dag.svg?raw=true "Dag")

snakemake command inside docker:
```commandline
snakemake --cores 10
snakemake --dag | dot -Tsvg > dag.svg

docker ps
docker cp <CONTAINER ID>:/app/dag.svg .
```
