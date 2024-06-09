from .file_associations import *
from .direction import *
from abstract_pandas.abstractLandManager import *
import logging
import os,json
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
# Setup logging
def get_latitude_longitude(point_js):
    point_js['latitude']=False
    if str(point_js.get('direction')).lower() in ['north','south','true']:
        point_js['latitude']=True
    return point_js
logging.basicConfig(level=logging.INFO)
def get_cardinal_keys():
    return {'direction':["north","south","easty","west"],'from':['center',"boundary"],"rangeInclusive":["inclusive","range"]}
def get_column_js():
    return {'zipcodes':['ZIP_CODE'],'cities':['CITY'],'counties':["countyName","COUNTY_NAM","NAME"]}
def get_designation_js():
    return {'cities':['city','cities','citie'],'counties':['counties','countie','county','countys','counties'],'zipcodes':['zips','zipcodes','zip-codes','zip_codes','zip codes','zipcode','zip','zip-code','zip_code','zip code']}
def closest_designation(desig):
     desig = desig.lower()
     for designation in ['zipcodes','cities','counties']:
         if desig in get_designation_js()[designation]:
             return designation
     if 'cit' in desig:
         return 'cities'
     if 'count' in desig:
         return 'counties'
     if 'zip' in desig:
         return 'zipcodes'
     return get_closest_designation(desig)

def determine_category(directory):
    compare_js = {'cit': "cities", 'stat': "states", 'count': "counties", 'zip': "zipcodes"}
    for key, value in compare_js.items():
        if key in directory.lower():
            return value
    return "others"
def find_shapefiles(root_dir):
    shape_extensions = {'.shp', '.shx', '.dbf', '.prj', '.cpg', '.xml', '.geojson'}
    categorized_files = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if os.path.splitext(file)[1].lower() in shape_extensions:
                category = determine_category(dirpath)
                if category not in categorized_files:
                    categorized_files[category] = []
                categorized_files[category].append(os.path.join(dirpath, file))
    dirs_js = {}
    for key,values in categorized_files.items():
        for value in values:
            dirs_js[key] = os.path.dirname(value)
    
    return dirs_js
class shapeManager(metaclass=SingletonMeta):
    def __init__(self, directory=None,epsg=4326):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.shapes_repository = {}
            self.dataDir = directory
            self.directories = find_shapefiles(self.dataDir)
            self.land_mgr = landManager(self.directories)
            self.epsg = epsg
    def get_contents(self, dir_name, file_type, epsg=4326, update=None):
            logging.info(f"Fetching contents for directory: {dir_name}, file type: {file_type}")
            # Retrieve cached contents if available
            if dir_name not in self.shapes_repository:
                self.shapes_repository[dir_name]={}
            if file_type not in self.shapes_repository[dir_name]:
                contents = self.land_mgr.get_contents(dir_name=dir_name, file_type=file_type, update=update)
                dir_name,columns,column_name = self.get_col_name(dir_name,contents)
                self.shapes_repository[dir_name][file_type]={'contents':contents,"columns":columns,"column_name":column_name}
            return self.shapes_repository[dir_name][file_type]['contents']

    def get_col_name(self,designation,contents):
        designation = closest_designation(designation)
        columns = get_df(contents,nrows=0)
        column_name = [name for name in columns if name in get_column_js().get(get_closest_designation(designation))] or None
        if column_name and isinstance(column_name, list) and len(column_name) > 0:
            logging.info(f"Found column name: {column_name[0]}")
            column_name =column_name[0]
        return designation,columns,column_name
    def get_geo_data_dir(self, subDir=None):
        dataDir = self.dataDir
        if subDir:
            dataDir = os.path.join(self.dataDir, subDir)
        logging.info(f"Geo data directory: {dataDir}")
        return dataDir

    def get_directories(self):
        directories = {'zipcodes': "", 'cities': "", 'counties': ""}
        for designation in directories:
            directories[designation] = self.get_geo_data_dir(subDir=designation)
            logging.info(f"Set directory for {designation}: {directories[designation]}")
        return directories
    def get_polygon(self, designation, value):
        logging.info(f"Fetching polygon for designation: {designation}, value: {value}")
        designation = closest_designation(designation)
        geo_df = self.get_contents(designation, 'shp')
        column_name = self.get_column_name(designation, file_type='shp')
        polygon = self.land_mgr.get_polygon(geo_df, column_name, value)
        logging.info(f"Polygon fetched for designation: {designation}, value: {value}")
        return polygon

    def get_column_name(self, designation, file_type='shp'):
        logging.info(f"Fetching column name for designation: {designation}, file type: {file_type}")
        designation = closest_designation(designation)
        self.get_contents(designation, file_type)
        logging.info(f"Using default column name for designation: {designation}")
        return self.shapes_repository[designation][file_type]['column_name']

    def get_column_list(self,designation,file_type='shp'):
        designation = closest_designation(designation)
        geo_df = self.get_contents(designation,file_type)
        column_name = self.get_column_name(designation,file_type=file_type)
        if geo_df is not None:
            column_list = geo_df[column_name].tolist()
            logging.info(f"Returning column list for designation: {designation}, file type: {file_type}")
            return column_list

    def get_derived_geom(self, point_js):
        designation, value = get_city_or_county(point_js)
        df_a = self.get_contents(designation, 'shp')
        geom = None
        row = get_any_row(df_a,value)
        if row is not None:
            row = row.to_dict()
            geom = row.get('geometry')
            logging.info(f"Derived geometry for {value}")
        geom = geom or self.get_polygon(designation, value)
        if point_js.get('from') == 'center':
            geom = geom.centroid

        point_js['geom'] = geom
        return point_js

    def derive_cardinal_vars(self, point_js):
        logging.info(f"Deriving cardinal variables for point: {point_js}")
        point_js = self.get_derived_geom(point_js)
        point_js = get_latitude_longitude(point_js)
        point_js['rangeInclusive'] = str(point_js.get('rangeInclusive')).lower() == 'false'
        return point_js
