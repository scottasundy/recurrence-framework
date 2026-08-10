#!/usr/bin/env python3
from pathlib import Path
import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold, cross_val_predict

ROOT=Path(__file__).resolve().parents[1]
inp=ROOT/'data/periods/5x5-sample.csv'
out=ROOT/'supplemental/period-predictor.csv'
with inp.open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
features=[f'collision_t{i}' for i in range(30)]+[f'hamming_t{i}' for i in range(30)]+[
    'analytic_period_divisor','initial_collision_sites','mean_collision_sites_30',
    'max_collision_sites_30','nonzero_collision_steps_30','mean_step_hamming_30',
    'unique_density_frames_31']
X=np.asarray([[float(r[c]) for c in features] for r in rows])
y=np.asarray([float(r['log10_period']) for r in rows])
model=RandomForestRegressor(n_estimators=500,min_samples_leaf=3,max_features=0.7,
                            random_state=20260809,n_jobs=1)
cv=KFold(n_splits=5,shuffle=True,random_state=20260809)
pred=cross_val_predict(model,X,y,cv=cv,n_jobs=1)
err=10**np.abs(pred-y)
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['sample_states','feature_count','history_updates','model',
        'cross_validated_r2','median_multiplicative_error','p90_multiplicative_error','interpretation'])
    w.writerow([len(rows),len(features),30,'RandomForestRegressor',f'{r2_score(y,pred):.12f}',
        f'{np.median(err):.12f}',f'{np.percentile(err,90):.12f}',
        'empirical period-scale signal only; not an exact or universal period law'])
print(out)
