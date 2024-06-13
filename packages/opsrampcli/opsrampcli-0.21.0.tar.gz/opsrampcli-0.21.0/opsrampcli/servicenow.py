import requests
import pandas as pd
from datetime import datetime
import pytz



def get_resources_df(job):
    SERVICENOW_DISPLAY_VALUE = 'display_value'
    FIELD_NAME_MAPPING = 'fieldname_mapping'
    FIELD_VALUE_MAPPING = 'fieldvalue_mapping'
    FIELD_VALUE_REGEX = 'regex'
    FIELD_VALUE_REPLACE = 'replace'
    FIELD_STATIC_VALUE = 'static_fieldvalue'

    url = f"{job['source']['servicenow']['instance_url']}/api/now/table/{job['source']['servicenow']['table']}"
    auth = requests.auth.HTTPBasicAuth(job['source']['servicenow']['auth']['username'], job['source']['servicenow']['auth']['password'])
    qstrings = {}
    for k, v in job['source']['servicenow']['query_parameters'].items():
        qstrings[f'sysparm_{k}'] = v
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.get(url=url, auth=auth, params=qstrings, headers=headers)
    try:
        responsedict = response.json()
    except Exception as e:
        raise Exception('Failed to retrieve records from ServiceNow datasource.')
    records = responsedict.get('result', [])
    processed_recs = []
    for record in records:
        newrec = {}
        for key,value in record.items():
            if isinstance(value, dict) and SERVICENOW_DISPLAY_VALUE in value:
                newrec[key] = value[SERVICENOW_DISPLAY_VALUE]
            else:
                newrec[key] = value
        processed_recs.append(newrec)

    df = pd.DataFrame(processed_recs)

    if FIELD_NAME_MAPPING in job and isinstance(job[FIELD_NAME_MAPPING], dict):
        for old, new in job[FIELD_NAME_MAPPING].items():
            if old in df.columns:
                df.rename(columns={old: new}, inplace=True)
    

    if FIELD_VALUE_MAPPING in job and isinstance(job[FIELD_VALUE_MAPPING], dict):
        for fieldname, mappings in job[FIELD_NAME_MAPPING].items():
            if fieldname in df.columns and isinstance(mappings, list):
                for mapping in mappings:
                    if isinstance(mapping, dict) and FIELD_VALUE_REGEX in mapping and FIELD_VALUE_REPLACE in mapping:
                        df[fieldname] = df[fieldname].str.replace(mapping[FIELD_VALUE_REGEX], mapping[FIELD_VALUE_REPLACE], regex=True)
    
    if FIELD_STATIC_VALUE in job and isinstance(job[FIELD_STATIC_VALUE], dict):
        for field, value in job[FIELD_STATIC_VALUE].items():
            if value == 'TIMESTAMPLOCAL()':
                value = str(datetime.now())
            elif value == 'TIMESTAMPUTC()':
                value = str(datetime.now().astimezone(pytz.utc))        
            df[field] = value


    if 'exceptions' in job:
        for fieldname, values_to_exclude in job['exceptions'].items():
            df = df[~df[fieldname].isin(values_to_exclude)]

    return df