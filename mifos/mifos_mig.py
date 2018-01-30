# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 08:29:49 2018

@author: dishon-lendable
"""

import json
from pandas.io.json import json_normalize
import pandas as pd

with open('clients.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)   

normalized_df = json_normalize(df['pageItems'])

'''column is a string of the column's name.
for each value of the column's element (which might be a list),
duplicate the rest of columns at the corresponding row with the (each) value.
'''

def flattenColumn(input, column):
    column_flat = pd.DataFrame([[i, c_flattened] for i, y in input[column].apply(list).iteritems() for c_flattened in y], columns=['I', column])
    column_flat = column_flat.set_index('I')
    return input.drop(column, 1).merge(column_flat, left_index=True, right_index=True)
    
new_df = flattenColumn(normalized_df, 'id')
new_df.to_csv('out.csv',sep=',',encoding='utf-8')
        