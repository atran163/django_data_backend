import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from matplotlib import pyplot as plt 
from ipywidgets import interact
import requests
import json
import pickle
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("/Users/AmandaTran/mysite/ml_model/mh.csv")

# ----------- CLEANING THE DATA -----------
# Column rename
renamed_columns = ['self_empl_flag', 'comp_no_empl', 'tech_comp_flag', 'tech_role_flag', 'mh_coverage_flag',
                  'mh_coverage_awareness_flag', 'mh_employer_discussion', 'mh_resources_provided', 'mh_anonimity_flag',
                  'mh_medical_leave', 'mh_discussion_neg_impact', 'ph_discussion_neg_impact', 'mh_discussion_cowork',
                  'mh_discussion_supervis', 'mh_eq_ph_employer', 'mh_conseq_coworkers', 'mh_coverage_flag2', 'mh_online_res_flag',
                  'mh_diagnosed&reveal_clients_flag', 'mh_diagnosed&reveal_clients_impact', 'mh_diagnosed&reveal_cowork_flag', 'mh_cowork_reveal_neg_impact',
                  'mh_prod_impact', 'mh_prod_impact_perc', 'prev_employers_flag', 'prev_mh_benefits', 'prev_mh_benefits_awareness',
                  'prev_mh_discussion', 'prev_mh_resources', 'prev_mh_anonimity', 'prev_mh_discuss_neg_conseq', 'prev_ph_discuss_neg_conseq',
                  'prev_mh_discussion_cowork', 'prev_mh_discussion_supervisor', 'prev_mh_importance_employer', 'prev_mh_conseq_coworkers',
                  'future_ph_specification', 'why/why_not', 'future_mh_specification', 'why/why_not2', 'mh_hurt_on_career', 'mh_neg_view_cowork',
                  'mh_sharing_friends/fam_flag', 'mh_bad_response_workplace', 'mh_for_others_bad_response_workplace', 'mh_family_hist',
                  'mh_disorder_past', 'mh_disorder_current', 'yes:what_diagnosis?', 'maybe:whats_your_diag', 'mh_diagnos_proffesional',
                  'yes:condition_diagnosed', 'mh_sought_proffes_treatm', 'mh_eff_treat_impact_on_work', 'mh_not_eff_treat_impact_on_work',
                  'age', 'sex', 'country_live', 'live_us_teritory', 'country_work', 'work_us_teritory', 'work_position', 'remote_flag']
df.columns = renamed_columns

# Sex column needs to be recoded (number of unique values = 70)
df['sex'].replace(to_replace = ['Male', 'male', 'Male ', 'M', 'm',
       'man', 'Cis male', 'Male.', 'male 9:1 female, roughly', 'Male (cis)', 'Man', 'Sex is male',
       'cis male', 'Malr', 'Dude', 
       "I'm a man why didn't you make this a drop down question. You should of asked sex? And I would of answered yes please. Seriously how much text can this take? ",
       'mail', 'M|', 'Male/genderqueer', 'male ',
       'Cis Male', 'Male (trans, FtM)',
       'cisdude', 'cis man', 'MALE'], value = "Male", inplace = True)

df['sex'].replace(to_replace = ['Female', 'female', 'I identify as female.', 'female ',
       'Female assigned at birth ', 'F', 'Woman', 'fm', 'f', 'Cis female ', 'Transitioned, M2F',
       'Genderfluid (born female)', 'Female or Multi-Gender Femme', 'Female ', 'woman', 'female/woman',
       'Cisgender Female', 'fem', 'Female (props for making this a freeform field, though)',
       ' Female', 'Cis-woman', 'female-bodied; no feelings about gender',
       'AFAB'], value = "Female", inplace = True)

df['sex'].replace(to_replace = ['Bigender', 'non-binary', 'Other/Transfeminine',
       'Androgynous', 'Other', 'nb masculine',
       'none of your business', 'genderqueer', 'Human', 'Genderfluid',
       'Enby', 'genderqueer woman', 'mtf', 'Queer', 'Agender', 'Fluid',
       'Nonbinary', 'human', 'Unicorn', 'Genderqueer',
       'Genderflux demi-girl', 'Transgender woman'], value = "Other", inplace = True)

# Recode Comp size & country columns (for ease when doing plots)
df['comp_no_empl'].replace(to_replace = ['More than 1000'], value = '>1000', inplace = True)
df['country_live'].replace(to_replace = ['United States of America'], value = 'USA', inplace = True)
df['country_live'].replace(to_replace = ['United Kingdom'], value = 'UK', inplace = True)
df['country_work'].replace(to_replace = ['United States of America'], value = 'USA', inplace = True)
df['country_work'].replace(to_replace = ['United Kingdom'], value = 'UK', inplace = True)

# Max age is 323, min age is 3.
# There are only 5 people that have weird ages (3yo, 15yo, or 99yo or 323 yo.) 
# These people will take the average age of the dataset (the correct calculated one, w/out outliers)
mean_age = df[(df['age'] >= 18) | (df['age'] <= 75)]['age'].mean()
df['age'].replace(to_replace = df[(df['age'] < 18) | (df['age'] > 75)]['age'].tolist(),
                          value = mean_age, inplace = True)


# REPLACE NA 
df['age'].fillna((df['age'].mean()), inplace=True)
df['sex'].fillna(value="Other", inplace=True)
df['comp_no_empl'].fillna(value="26-100", inplace=True)
df['mh_diagnos_proffesional'].fillna(value="I don't know", inplace=True)
df['mh_family_hist'].fillna(value="Not Sure", inplace=True)
df['mh_resources_provided'].fillna(value="Not Sure", inplace=True)
df['mh_resources_provided'] = df['mh_resources_provided'].fillna(value= "Not Sure")
df['mh_coverage_flag'].fillna(value = "Not eligible for coverage / N/A", inplace=True)
df['mh_employer_discussion'].fillna(value="I don't know", inplace=True)
df['mh_neg_view_cowork'].fillna(value="Maybe", inplace=True)

sub = df[['mh_coverage_flag', 'mh_employer_discussion', 'mh_resources_provided',
       'mh_neg_view_cowork', 'mh_family_hist', 'age', 'sex', 'comp_no_empl', 'mh_diagnos_proffesional']]

sub.dropna(inplace=True)

y_vals = sub['mh_diagnos_proffesional']
x_vals = sub[['age', 'sex', 'num_emply', 'mh_family_hist', 'mh_resources_provided', 'mh_coverage_flag', 'mh_employer_discussion', 'mh_neg_view_work']

# LOAD LR Model and MAKE PIPELINE 
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

ct = make_column_transformer(
    (StandardScaler(), ["age"]),
    (OneHotEncoder(), ['mh_coverage_flag', 'mh_employer_discussion', 'mh_resources_provided', 'mh_neg_view_cowork', 'mh_family_hist', 'sex', 'comp_no_empl']),
    remainder="drop"  # all other columns in X will be dropped.
)
ct

# FIT MODEL
from sklearn.pipeline import make_pipeline

pipeline = make_pipeline(
    ct,
    LogisticRegression()
)

pipeline.fit(X=x_vals, y=y_vals)


# SAVE MODEL AS PKL FILE 
filename = 'ml_model/music_books.pkl'
pickle.dump(pipeline, open(filename, 'wb'))

