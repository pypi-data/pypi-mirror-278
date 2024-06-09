from .abstractShapeManager import *
def get_min_latitude_of_geom(geometry):
    """Return the minimum latitude of a geometry which can be Polygon or MultiPolygon."""
    if isinstance(geometry, Polygon):
        min_lat = min(point[1] for point in geometry.exterior.coords)
    elif isinstance(geometry, MultiPolygon):
        min_lat = min(point[1] for polygon in geometry.geoms for point in polygon.exterior.coords)
    else:
        raise TypeError("Unsupported geometry type")
    return min_lat
def get_max_latitude_of_geom(geometry):
    """Return the minimum latitude of a geometry which can be Polygon or MultiPolygon."""
    if isinstance(geometry, Polygon):
        min_lat = max(point[1] for point in geometry.exterior.coords)
    elif isinstance(geometry, MultiPolygon):
        min_lat = max(point[1] for polygon in geometry.geoms for point in polygon.exterior.coords)
    else:
        raise TypeError("Unsupported geometry type")
    return min_lat
# Function to check if a geometry's latitude lies within specified bounds, supporting both Polygon and MultiPolygon
def is_within_bounds(geometry, lower_bound, upper_bound):
    def extract_latitudes(polygon):
        """Extract latitudes from a polygon's exterior coordinates."""
        return [coord[1] for coord in polygon.exterior.coords]

    latitudes = []
    if isinstance(geometry, Polygon):
        latitudes = extract_latitudes(geometry)
    elif isinstance(geometry, MultiPolygon):
        for polygon in geometry.geoms:
            latitudes.extend(extract_latitudes(polygon))
    else:
        raise TypeError("Unsupported geometry type")
    # Check if any latitude falls within the specified bounds
    return any(lower_bound <= lat <= upper_bound for lat in latitudes)
def get_latitude_longitude(point_js):
        point_js['latitude']=False
        if str(point_js.get('direction')).lower() in ['north','south','true']:
            point_js['latitude']=True
        return point_js
def is_key_found(json_obj,key):
    if key in list(json_obj.keys()):
        return True
def search_for_cardinal_keys(point_object):
    derived_js = {}
    for each_js in [get_designation_js(),get_cardinal_keys()]:
        for key,values in each_js.items():
            for value in values:
                for card_key,value in point_object.keys.items():
                    result = if_eq_or_in(key,value,exact=False,case=False,reverse=True)
                    if result:
                        derived_js[key] = value
                    if key in derived_js:
                        break
                if is_key_found(derived_js,key):
                    break
    return derived_js
    
