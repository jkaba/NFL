# Random Forest
# Author: Jameel Kaba

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from statistics import mean

iteration = 1
year_iteration = 1

stat_list = ['adj_att','adj_ruyds','adj_rutd','adj_rec','adj_reyds','adj_retd','adj_scrim_yds','adj_off_td'\
             ,'adj_tkl','adj_ast_tkl','adj_tot_tkl','adj_run_stuff','adj_sk','adj_tfl','adj_int','adj_pass_def'\
             ,'adj_ff','adj_fr','disruption','ktd','ptd','int_td','fr_td','non_off_td','off_pass_cmp','off_pass_att'\
             ,'off_rush_att','def_pass_att','def_rush_att','team_sp','offense_sp','defense_sp','schedule_sp'\
             ,'off_usage','rel_usage','rel_disruption','weighted_def_sp']

depth_list = []
rms_list = []
prediction_log = []
importance_dict = {}
hyperparameters = {'WR':[100,10,10,14],
                   'FS':[50,5,10,3],
                   'CB':[50,10,20,2],
                   'SS':[250,15,10,3],
                   'ILB':[100,10,20,10],
                   'RB':[250,10,10,1],
                   'TE':[100,5,15,14],
                   'EDGE_LB':[100,15,5,2],
                   'EDGE_DL':[250,15,20,1],
                   'C':[20,5,10,3],
                   'DT':[20,5,10,10],
                   'OT':[250,15,20,1],
                   'OG':[250,5,20,18]}

# Include adjacent position groups in dataset
fuzzy_pos_groups = {'WR':['WR','RB','TE','CB'],
                    'FS':['FS','CB','SS','RB'],
                    'CB':['CB','FS','WR'],
                    'SS':['SS','FS','ILB'],
                    'ILB':['ILB','EDGE_LB','SS','WR'],
                    'RB':['RB','WR','ILB'],
                    'TE':['TE','WR','OT'],
                    'EDGE_LB':['EDGE_LB','EDGE_DL','ILB'],
                    'EDGE_DL':['EDGE_DL','DT','EDGE_LB','TE'],
                    'C':['OG','C'],
                    'DT':['EDGE_DL','DT','EDGE_LB','ILB'],
                    'OT':['OT','OG','C','EDGE_DL'],
                    'OG':['OT','OG','C']}


for m in [1]:
    random_iteration = 1
    for i in range(0,1):

        year_iteration = 1
        for year in range(2006, 2015):
            iteration = 1
            for position_group in ['CB','FS','SS','ILB','EDGE_DL','EDGE_LB','DT','WR','RB','TE','OT','OG','C']:

                fuzzy_group = fuzzy_pos_groups[position_group]
                draftData = pd.read_csv(r'C:\Users\Walter King\Documents\Combine Data\data_files\combined_draft_classes_randomForest.csv')
                for s in stat_list:
                    try:
                        draftData[s].fillna(draftData.groupby(['position','pos_group'])[s].transform("median"), inplace=True)
                    except:
                        draftData[s].fillna(value = 0)
                draftData.fillna(value = 0)

                # Training data will include adjacent position groups
                train_data = draftData[draftData['position'].isin(fuzzy_group)]
                train_data = train_data[:].query("year != \"" + str(year) + "\"")
                same_pos = train_data[:].query('position == "' + position_group + "\"")

                # Ensure same position type is most prevalent in training set
                while train_data[train_data['position'] == position_group].count()['position'] <= \
                        train_data[train_data['position'] != position_group].count()['position']:
                    train_data = pd.concat([train_data, same_pos])
                test_data = draftData[:].query('position == "' + position_group + "\" and year == \"" + str(year) + "\"")
                test_data = test_data.reset_index(drop=True)
 
                exportfeatures = test_data.copy()
                labels_train = np.array(train_data['rating'])
                train_data = train_data.drop(['full_name','first_name','last_name','draft_team','college','position'
                                              ,'pos_group','round','pick','overall','rating','year','consensus'], axis = 1)
                if position_group in ['CB','FS','SS','ILB','EDGE_LB','EDGE_DL','DT']:
                    train_data = train_data.drop(['adj_att','adj_ruyds','adj_rutd','adj_rec','adj_reyds','adj_retd','adj_scrim_yds'
                                                  ,'adj_off_td','off_pass_cmp','off_pass_att','off_rush_att','off_usage','rel_usage'], axis = 1)
                else:
                    train_data = train_data.drop(['adj_tkl','adj_ast_tkl','adj_tot_tkl','adj_run_stuff','adj_sk','adj_tfl'
                                                  ,'adj_int','adj_pass_def','adj_ff','adj_fr','int_td','fr_td','def_td'
                                                  ,'def_pass_att','def_rush_att','disruption','rel_disruption','weighted_def_sp'], axis = 1)
                column_names = train_data.columns
                train_data = np.array(train_data)
                labels = np.array(test_data['rating'])
                test_data = test_data.drop(['full_name','first_name','last_name','draft_team','college','position'
                                            ,'pos_group','round','pick','overall','rating','year','consensus'], axis = 1)
                if position_group in ['CB','FS','SS','ILB','EDGE_LB','EDGE_DL','DT']:
                    test_data = test_data.drop(['adj_att','adj_ruyds','adj_rutd','adj_rec','adj_reyds','adj_retd','adj_scrim_yds'
                                                  ,'adj_off_td','off_pass_cmp','off_pass_att','off_rush_att','off_usage','rel_usage'], axis = 1)
                else:
                    test_data = test_data.drop(['adj_tkl','adj_ast_tkl','adj_tot_tkl','adj_run_stuff','adj_sk','adj_tfl'
                                                  ,'adj_int','adj_pass_def','adj_ff','adj_fr','int_td','fr_td','def_td'
                                                  ,'def_pass_att','def_rush_att','disruption','rel_disruption','weighted_def_sp'], axis = 1)
                test_data = np.array(test_data)
                train_features, test_features, train_labels, test_labels = \
                train_test_split(train_data, labels_train, test_size = 0.25, random_state = 42)
                rf = RandomForestRegressor(n_estimators = hyperparameters[position_group][0], 
                                           random_state = 42, 
                                           max_depth = hyperparameters[position_group][1], 
                                           max_features = hyperparameters[position_group][2], 
                                           min_samples_leaf = hyperparameters[position_group][3])

                # Replace null values with 0
                train_features[np.isnan(train_features)] = 0
                test_features[np.isnan(test_features)] = 0
                train_data[np.isnan(train_data)] = 0
                test_data[np.isnan(test_data)] = 0
                model = rf.fit(train_features, train_labels);
                feature_importances = pd.DataFrame(rf.feature_importances_,index = column_names,columns=['importance']).sort_values('importance',ascending=False)

                prediction = model.predict(test_data)
                exportfeatures['prediction'] = prediction
                exportfeatures.to_csv('dumpfile.csv') 
                if iteration == 1:
                    predicted_data = pd.read_csv('dumpfile.csv')
                else:
                    append_data = pd.read_csv('dumpfile.csv')
                    predicted_data = predicted_data.append(pd.DataFrame(data = append_data), ignore_index=True)
                iteration += 1
                predicted_data.to_csv('dumpfile.csv')

            if year_iteration == 1:
                master_data = pd.read_csv('dumpfile.csv')
                for n in range(len(feature_importances)):
                    importance_dict[feature_importances.iloc[n].name] = []
            else:
                year_append = pd.read_csv('dumpfile.csv')
                master_data = master_data.append(pd.DataFrame(data = year_append), ignore_index=True)
            for n in range(len(feature_importances)):
                importance_dict[feature_importances.iloc[n].name].append(feature_importances.iloc[n]['importance'])
            year_iteration += 1
            master_data.to_csv('dumpfile.csv')
            rating_list = master_data['rating'].tolist()
            prediction_list = master_data['prediction'].tolist()
            rms = sqrt(mean_squared_error(rating_list, prediction_list))
        depth_list.append(m)
        rms_list.append(rms)

        prediction = master_data['prediction'].tolist()
        if random_iteration == 1:    
            prediction_log = [[i] for i in prediction]
        else:
            for i in range(len(prediction)):
                prediction_log[i].append(prediction[i])
        random_iteration += 1
    prediction_list = []
    for i in range(len(prediction_log)):
        pred_avg = sum(prediction_log[i]) / len(prediction_log[0])
        prediction_list.append(pred_avg)     

    # Pull RMSE
    rating_list = master_data['rating'].tolist()
    prediction_list = master_data['prediction'].tolist()
    rms = sqrt(mean_squared_error(rating_list, prediction_list))
    print(rms)
    depth_list.append(m)
    rms_list.append(rms)

master_data['prediction'] = prediction_list
master_data.to_csv('dumpfile.csv') 