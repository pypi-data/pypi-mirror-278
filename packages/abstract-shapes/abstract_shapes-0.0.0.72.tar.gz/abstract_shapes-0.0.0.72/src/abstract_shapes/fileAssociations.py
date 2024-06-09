def get_column_js():
    return {'zipcodes':['ZIP_CODE'],'cities':['CITY'],'counties':["countyName","COUNTY_NAM","NAME"]}
def get_designation_js():
    return {'cities':['city','cities','citie'],'counties':['counties','countie','county','countys','counties'],'zipcodes':['zips','zipcodes','zip-codes','zip_codes','zip codes','zipcode','zip','zip-code','zip_code','zip code']}
def get_column_name(designation,file_type='shp'):
    designation = get_closest_designation(designation)
    column_keys = get_column_js().get(designation)
    geo_df = shape_mgr.get_contents(designation,file_type)
    column_name = [name for name in geo_df.columns.tolist() if name in column_keys]
    if column_name and isinstance(column_name,list) and len(column_name)>0:
        return column_name[0]
    return column_keys_js[designation][0]
def get_column_list(designation,file_type='shp'):
    column_name = get_column_name(designation,file_type)
    geo_df = shape_mgr.get_contents(designation,file_type)
    if geo_df is not None:
        return geo_df[column_name].tolist()
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
