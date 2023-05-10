import pandas as pd
def preprocess(df,region):
    df=df[df['Season']=='Summer']
    df=df.drop_duplicates()
    df=df.merge(region,on='NOC',how='left')
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df