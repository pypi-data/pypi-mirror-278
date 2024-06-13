# DVC research

```commandline
git init
dvc init
dvc remote add --default myremote gdrive://your_folder_hash
dvc add folder_with_data

dvc repro
dvc push
```
add remote with creds: https://stackoverflow.com/questions/74017026/automate-dvc-authentication-when-using-github-actions

Metrics
```commandline
dvc metrics show
dvc metrics diff
```
Comparison logreg with catboost:
```
Path          Metric                  HEAD     workspace    Change
summary.json  0.f1-score              0.00025  0.05346      0.05321
summary.json  0.precision             0.25     0.43786      0.18786
summary.json  0.recall                0.00012  0.02847      0.02834
summary.json  1.f1-score              0.02893  0.02843      -0.0005
summary.json  1.precision             0.35609  0.38233      0.02624
summary.json  1.recall                0.01508  0.01476      -0.00031
summary.json  2.f1-score              0.89713  0.89735      0.00022
summary.json  2.precision             0.81514  0.81612      0.00098
summary.json  2.recall                0.99747  0.99655      -0.00092
summary.json  accuracy                0.81227  0.81265      0.00037
summary.json  macro avg.f1-score      0.30877  0.32642      0.01764
summary.json  macro avg.precision     0.47374  0.54543      0.07169
summary.json  macro avg.recall        0.33756  0.34659      0.00904
summary.json  weighted avg.f1-score   0.73283  0.73512      0.00229
summary.json  weighted avg.precision  0.72453  0.7369       0.01237
summary.json  weighted avg.recall     0.81227  0.81265      0.00037
```
### Confusion matrices for log reg and catboost
![log reg conf matrix](../../../dvc_plots/static/HEAD_conf_matrix.png)
![catboost conf matrix](../../../dvc_plots/static/workspace_conf_matrix.png)

On same data preprocessing catboost performed much better than logistic regression.
'/dvc_plots/index.html'
