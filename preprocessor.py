import pandas as pd


def preprocess(df, region_df):
    # Filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # Dropping duplicated
    df = df.drop_duplicates()
    # if we used inplace = True, it would return None data type, and the other operations wouldn't work
    # one hot encoding the medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    print(df)
    return df
