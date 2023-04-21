import pandas as pd
import numpy as np
from flask import Flask, request, redirect, url_for, session, abort, flash, jsonify, g, render_template
#from sqlalchemy import create_engine
import ast
import random as rn
import joblib



def home_page():
    if request.method == 'POST':
        test_dict = eval(request.form["arguments"])
        test_df = pd.DataFrame(test_dict,index=[0])
        # print(test_df.head().T)
        cols = ['tenure', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'TechSupport', 'Contract', 'PaymentMethod', 'MonthlyCharges',
                'TotalCharges']
        test_df.columns = cols

        netservice_dict = {'Fiber Optic':0, 'DSL':1, 'No':2}
        test_df['InternetService'] = test_df['InternetService'].map(netservice_dict) 

        onlinesecurity_dict = {'No':0, 'Yes':1, 'No Internet Service':2}
        test_df['OnlineSecurity'] = test_df['OnlineSecurity'].map(onlinesecurity_dict) 

        
        onlinebackup_dict = {'No':0, 'Yes':1, 'No Internet Service':2}
        test_df['OnlineBackup'] = test_df['OnlineBackup'].map(onlinebackup_dict) 


        techsupport_dict = {'No':0, 'Yes':1, 'No Internet Service':2}
        test_df['TechSupport'] = test_df['TechSupport'].map(techsupport_dict) 

        contract_dict = {'Month-to-month':0, 'Two Year':1, 'One Year':2}
        test_df['Contract'] = test_df['Contract'].map(contract_dict) 

        payment_dict = {'Electronic check':0, 'Mailed check':1, 'Bank transfer (automatic)':2, 'Credit card (automatic)' :3}
        test_df['PaymentMethod'] = test_df['PaymentMethod'].map(payment_dict) 
        

        filename = 'static/models/finalized_model.sav'
        loaded_model = joblib.load(filename)
        print(loaded_model)
        print(test_df.T)


        variable = loaded_model.predict(test_df)
        variable_prob = loaded_model.predict_proba(test_df)
        attrition_rate_yes = str(variable_prob[0][1])
        attrition_rate_no = str(variable_prob[0][0])

        print(variable_prob)

        return  jsonify({
                'Class' : str(variable[0]),
                'Rate_yes': attrition_rate_yes[:5],
                'Rate_no':attrition_rate_no[:5] 
                 })
    
    else:
        return render_template('Home_page.html')



def home_page_date():
    return render_template('Home_page.html')