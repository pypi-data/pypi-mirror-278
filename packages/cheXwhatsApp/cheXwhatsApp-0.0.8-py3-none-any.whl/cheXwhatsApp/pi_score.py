import os
import pandas  as pd
import numpy as np 

# Calculate the PI score
def pip_score(df1, df2):
    pip_df = pd.DataFrame()
    # from np1 remove the rows where image_name is not present in np2
    df1 = df1[df1['image_names'].isin(df2['image_names'])]
    pip_df['image_names'] = df1['image_names']

    # if any value in dataframe np1 is greater than 0.5 make it 1 else 0, without converting to numpy
    np1 = df1.iloc[0:, 1:]
    np1 = np.where(np1 >= 0.5 , 1, 0)

    np2 = df2.iloc[0:, 1:]
    np2 = np.where(np2 >= 0.5 , 1, 0)

    np3 = np.where(np1 == np2 , 0, 1)
    # convert np3 to a 1 d array by converting each row to 0 if all elements are 0 else 1
    np3 = np.where(np3.sum(axis = 1) > 0, 1, 0)

    # map these to images in pip_df
    pip_df['pip_score'] = np3
        
    return pip_df

