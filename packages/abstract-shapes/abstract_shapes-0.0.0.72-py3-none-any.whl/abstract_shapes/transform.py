from osgeo import ogr, osr
from shapely import wkb,Polygon,MultiPolygon
def get_obj_crs(epsg=None,proj_string=None,obj=osr):
    obj_crs = obj.SpatialReference()
    if epsg:
        obj_crs.ImportFromEPSG(epsg)
    else:
        obj_crs.ImportFromWkt(str(proj_string))
    return obj_crs
def setup_transformation(source_epsg=None, target_epsg=None,source_proj_string=None,target_proj_string=None):
    source_crs = get_obj_crs(epsg=source_epsg,proj_string=source_proj_string)
    target_crs = get_obj_crs(epsg=target_epsg,proj_string=target_proj_string)
    return osr.CoordinateTransformation(source_crs,target_crs)
def transform_ogr_geometry(ogr_geom, transform):
    """
    Transform a single ogr.Geometry and return it as a Shapely geometry.
    """
    # Clone the original geometry to avoid modifying it directly
    transformed_ogr_geom = ogr_geom.Clone()
    # Apply the transformation
    transformed_ogr_geom.Transform(transform)
    # Export to WKB
    wkb_data = transformed_ogr_geom.ExportToWkb()
    wkb_data=bytes(wkb_data)
    # Check if wkb_data is a bytes object
    if not isinstance(wkb_data, bytes):
        raise TypeError(f"Expected WKB data to be bytes, got {type(wkb_data).__name__}")

    # Convert the WKB data to a Shapely geometry
    new_shapely_geom = wkb.loads(wkb_data)
    return new_shapely_geom

def transform_geometry(geom, transform):
    """
    Apply a coordinate transformation to any Shapely geometry and return a new geometry.
    """
    # Convert Shapely geometry to ogr.Geometry if necessary
    if isinstance(geom, (Polygon, MultiPolygon)):
        ogr_geom = ogr.CreateGeometryFromWkb(geom.wkb)
    else:
        raise TypeError("Unsupported geometry type")
    
    if isinstance(geom, MultiPolygon):
        # Handle MultiPolygon by transforming each constituent polygon
        transformed_polygons = [transform_ogr_geometry(ogr.CreateGeometryFromWkb(poly.wkb), transform) for poly in geom.geoms]
        return MultiPolygon(transformed_polygons)
    else:
        # Handle single Polygon
        return transform_ogr_geometry(ogr_geom, transform)
def update_geom(gdf,index,transform):
    existing_geom = gdf.at[index, 'geometry']
    return transform_geometry(existing_geom, transform)
    
def update_geometry_in_gdf(gdf, index=None, source_epsg=None, target_epsg=None,source_proj_string=None,target_proj_string=None):
    """
    Update the geometry in a GeoDataFrame at a specific index if the transformed geometry is different.
    """
    # Create transformation
    transform = setup_transformation(source_epsg=source_epsg, target_epsg=target_epsg,source_proj_string=source_proj_string,target_proj_string=target_proj_string)
    # Get the existing geometry and transform it

    if index== None:
        for index in range(len(gdf)):
            new_geom = update_geom(gdf,index,transform)
            if new_geom:
                gdf.at[index, 'geometry'] = new_geom
        return gdf
    else:
        # Check if the new geometry is different from the existing geometry
        if not existing_geom.equals(new_geom):
            gdf.at[index, 'geometry'] = new_geom
            print(f"Updated row {index} with new geometry.")
        else:
            print(f"No update needed for row {index}.")
        return gdf
