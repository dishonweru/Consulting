# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 08:29:49 2018

@author: dishon-lendable
"""

import json, urllib2, base64
from pandas.io.json import json_normalize
import pandas as pd

'''with open('clients.json') as f:
    data = json.load(f)'''

#Create Connection to Webservice endpoint
request = urllib2.Request('https://odyssey.openmf.org/fineract-provider/api/v1/clients?tenantIdentifier=odyssey')
base64string = base64.encodestring('%s:%s' % ('dishon', 'douglasdc3')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)
response_str = result.read().decode('utf-8')
json_obj = json.loads(response_str)

df = pd.DataFrame(json_obj)   

normalized_df = json_normalize(df['pageItems'])
normalized_df['id'] = normalized_df['id'].astype(str)

'''column is a string of the column's name.
for each value of the column's element (which might be a list),
duplicate the rest of columns at the corresponding row with the (each) value.
'''

def flattenColumn(input, column):    
    column_flat = pd.DataFrame([[i, c_flattened] for i, y in input[column].apply(list).iteritems() for c_flattened in y], columns=['I', column])
    column_flat = column_flat.set_index('I')
    return input.drop(column, 1).merge(column_flat, left_index=True, right_index=True)
    
normalized_df['iter_control'] = 's'
new_df = flattenColumn(normalized_df, 'iter_control')
new_df.to_csv('clients.csv',sep=',',encoding='utf-8')
        
