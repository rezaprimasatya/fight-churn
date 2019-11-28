import pandas as pd
import numpy as np
import os
from listing_7_5_fat_tail_scores import transform_fattail_columns, transform_skew_columns

def rescore_metrics(data_set_path):

    load_mat_df = reload_churn_data(data_set_path,'load_mat','6.4',is_customer_data=False)
    score_df = reload_churn_data(data_set_path,'score_params','7.5',is_customer_data=False)
    current_data = reload_churn_data(data_set_path,'current','8.2',is_customer_data=True)
    assert set(score_df.index.values)==set(current_data.columns.values),"Data to re-score does not match transform params"
    assert set(load_mat_df.index.values)==set(current_data.columns.values),"Data to re-score does not match load matrix"

    transform_skew_columns(current_data,score_df[score_df['skew_score']].index.values)
    transform_fattail_columns(current_data,score_df[score_df['fattail_score']].index.values)

    current_data=current_data[score_df.index.values]
    scaled_data=(current_data-score_df['mean'])/score_df['std']


    score_save_path=data_set_path.replace('.csv','_current_scores.csv')
    scaled_data.to_csv(score_save_path,header=True)
    print('Saving score results to %s' % score_save_path)

    scaled_data = scaled_data[load_mat_df.index.values]
    grouped_ndarray = np.matmul(scaled_data.to_numpy(), load_mat_df.to_numpy())

    current_data_grouped = pd.DataFrame(grouped_ndarray,columns=load_mat_df.columns.values, index=current_data.index)

    score_save_path=data_set_path.replace('.csv','_current_groupscore.csv')
    current_data_grouped.to_csv(score_save_path,header=True)
    print('Saving grouped results to %s' % score_save_path)


def reload_churn_data(data_set_path,suffix,listing,is_customer_data):
    data_path = data_set_path.replace('.csv', '_{}.csv'.format(suffix))
    assert os.path.isfile(data_path),'You must run listing {} to save {} first'.format(listing,suffix)
    ic = [0,1] if is_customer_data else 0
    churn_data = pd.read_csv(data_path, index_col=ic)
    return churn_data