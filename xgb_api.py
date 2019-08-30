from flask import Flask, request, redirect, url_for, flash, jsonify
import xgboost as xgb
import numpy as np, pandas as pd
import pickle as p
import json

app = Flask(__name__)

def gen_discrete_test(arr_df):
    max_int=336
    out_df = {}
    event_col = {0: 'pt_age', 1: 'dx_to_sct', 2: 'height_tx', 3: 'weight_tx', 4: 'bmi', 5: 'cbt_tnc_kg_cryop', 6: 'cbt_cfugm_kg',
                 7: 'cbt_cd34_kg', 8: 'cbt_tnc_kg_cryop_mis', 9: 'source', 10: 'donor_cd', 11: 'sct_type', 12: 'pt_sex', 13: 'sex_mismatch1',
                 14: 'ps24', 15: 'abo_mismatch', 16: 'diagnosis', 17: 'stage5', 18: 'stage_dri', 19: 'tbi', 20: 'cond', 21: 'tcd_invivo',
                 22: 'hctci_points_corr', 23: 'seromis6abdr', 24: 'genomis6abdr', 25: 'rcmvab', 26: 'dcmvab', 27: 'cmvab_cat1'}
    out_df['event']=[]
    for i,k in event_col.items():
        out_df[k] = []
    for i in range(max_int):
        out_df["D_"+str(i+1)] = []
    # start looping through each patient
    for pat in range(arr_df.shape[0]):
        # looping through each event-free interval
        pat_len = np.int(np.ceil(arr_df[:,-1][pat]+0.0001))
        for i,k in event_col.items():
            out_df[k] += [arr_df[pat,i]]*max_int
        for i in range(max_int):
            out_df["D_"+str(i+1)] += [1 if k==i else 0 for k in range(max_int)]
        out_df['event'] += [0]*(pat_len-1)
        out_df['event'] += [arr_df[pat,-2]]*(max_int-pat_len+1)
    out_df = pd.DataFrame(out_df)
    out_df = out_df.loc[out_df.D_1==1]
    return out_df.values

@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    data = pd.DataFrame(data)
    data = gen_discrete_test(data.values)
    X_test = data[:,1:]
    dtest = xgb.DMatrix(data=X_test)
    pred = model.predict(dtest)
    return jsonify(pred.tolist())

@app.route('/check/', methods=['GET'])
def hello():
    return 'hello'

if __name__ == '__main__':
    modelfile = 'xgboost.pickle'
    model = p.load(open(modelfile, 'rb'))
    app.run(debug=True, host='0.0.0.0', port=80)
