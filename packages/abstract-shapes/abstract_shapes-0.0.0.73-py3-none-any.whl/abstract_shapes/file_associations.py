from abstract_pandas import *
def clean_list(list_obj):
    while '' in list_obj:
        list_obj.remove('')
    return list_obj
def get_cardinal_keys():
    return {'direction':["north","south","easty","west"],'from':['center',"boundary"],"rangeInclusive":["inclusive","range"]}
def get_column_js():
    return {'zipcodes':['ZIP_CODE'],'cities':['CITY'],'counties':["countyName","COUNTY_NAM","NAME"]}
def get_designation_js():
    return {'cities':['city','cities','citie'],'counties':['counties','countie','county','countys','counties'],'zipcodes':['zips','zipcodes','zip-codes','zip_codes','zip codes','zipcode','zip','zip-code','zip_code','zip code']}
def if_eq_or_in(string,compString,exact=False,case=False,reverse=True):
    if not case:
        string=str(string).lower()
        compString = str(compString).lower()
    if string == compString:
        return True
    if not exact:
        if string in compString:
            return True
    if reverse:
        if compString in string:
            return True
    return False
def is_str_in_list_versa(list_obj,string):
    string_lower = str(string).lower()
    list_lower = [str(obj).lower() for obj in list_obj]
    for obj in list_lower:
        if obj in string_lower or string_lower in obj:
            return True
    return False
def get_closest_designation(designation):
    if isinstance(designation,gpd.GeoDataFrame):
        columns = get_df(designation,nrows=0)
        for designation_type,values in get_designation_js().items():
            for column in columns:
                for value in values:
                    response = if_eq_or_in(column,value,exact=True,case=False,reverse=False)
                    if response:
                        return designation_type
    designation_lower = str(designation).lower()
    designation_js = get_designation_js()
    for key,values in designation_js.items():
        values.append(key.lower())
        if designation_lower in values:
            return key
    for key,values in designation_js.items():
        values.append(key.lower())
        if is_str_in_list_versa(values,designation_lower):
            return key
def get_any_row(df,value,column=None):
    value = str(value).lower()
    headers =  get_df(df,nrows=0)
    for header in headers:
        values = [val for val in enumerate(df[header].tolist()) if if_eq_or_in(value,val[1])]
        if values:
            return df.iloc[values[0][0]]
def get_any_geom(df,value,column=None):
    value = str(value).lower()
    headers =  get_df(df,nrows=0)
    for header in headers:
        values = [val for val in enumerate(df[header].tolist()) if  if_eq_or_in(value,val[1])]
        if values:
            return df.at[values[0][0],'geometry']
def get_any_header(df,value,column=None):
    value = str(value).lower()
    headers =  get_df(df,nrows=0)
    for header in headers:
        values = [val for val in enumerate(df[header].tolist()) if if_eq_or_in(value,val[1])]
        if values:
            return header
def get_city_or_county(point):
    geo_data= []
    for point_itter in ['A','B']:
        for location_type in ['city','county']:
            curr_itter = f"{location_type}{point_itter}"
            value = point.get(curr_itter)
            if value:
                logging.info(f"{curr_itter} {value}")
                return get_closest_designation(location_type),value
    return geo_data
