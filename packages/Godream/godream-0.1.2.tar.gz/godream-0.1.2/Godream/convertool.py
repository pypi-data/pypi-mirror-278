import os
import rasterio
import rioxarray
import geopandas as gpd
import xarray as xr
import json
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from flusstools.geotools import open_raster, get_srs, float2int



# function to convert file format
def convert_format(input_path, output_path, output_format= None ):
    
    # Read in the  file using geopandas
    gdf = gpd.read_file(input_path)
    
    CRS_input = gdf.crs
    
    if output_format is None:
        raise IndexError('Need output_format, it can be ESRI Shapefile or GeoJSON ')
    else: 
        # Write out the GeoDataFrame to a SHP file with the specified CRS and encoding
        gdf.to_file(output_path, driver = output_format, crs= CRS_input, encoding='utf-8')


# function to convert CRS of shp and geojson file  / raster file(tif)     
def convert_crs(input_path, output_path, new_crs):
    
    # init
    is_Raster = False
    is_Vector = False
    
    # Check if the operation involves Raster-Vector (RV) or Vector-Vector (VV) clipping
    if input_path.lower().endswith('.tif') :
        is_Raster = True
    elif (input_path.lower().endswith('.shp') or input_path.lower().endswith('.geojson')):
        is_Vector = True
    
    
    # if input is vector
    if is_Vector is True:
    
        # check defined crs
        if new_crs is None:
            raise IndexError( 'No crs, The crs should define.' )

        if input_path.lower().endswith('geojson'):

            # Read in the GeoJSON file using geopandas
            gdf = gpd.read_file(input_path)

            # Convert the geometry to the desired CRS
            gdf = gdf.to_crs(new_crs)

            # Write out the GeoDataFrame to a  file with the specified CRS and encoding
            gdf.to_file(output_path, driver='GeoJSON', crs=new_crs, encoding='utf-8')

        elif input_path.lower().endswith('shp'):

            # Read in the shp file using geopandas
            gdf = gpd.read_file(input_path)

            # Convert the geometry to the desired CRS
            gdf = gdf.to_crs(new_crs)

            # Write out the GeoDataFrame to a  file with the specified CRS and encoding
            gdf.to_file(output_path, driver='ESRI Shapefile', crs=new_crs, encoding='utf-8')

        else:
            raise IndexError('Input file format should be ESRI Shapefile or GeoJSON. ')
    
    if is_Raster is True:
        
        # Open the source raster dataset
        with rasterio.open(input_path,'r') as src:
            # Define the new CRS
            new_crs = rasterio.crs.CRS.from_epsg(new_crs)

            # Calculate the transformation parameters
            transform, width, height = calculate_default_transform(
                src.crs, new_crs, src.width, src.height, *src.bounds
            )
            
            # Create a new dataset for the reprojected image
            with rasterio.open(
                output_path, 'w',
                driver='GTiff',
                count=src.count,
                crs=new_crs,
                transform=transform,
                width=width,
                height=height,
                dtype=src.dtypes[0]
            ) as reprojected:
                # Reproject the source dataset to the new CRS
                for i in range(1, src.count+1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(reprojected, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=new_crs,
                        resampling=Resampling.bilinear
                )
    
# fuction to create xarray from raster       
def xarray_ds(tiff_path, rice_model = None):
    with rasterio.open(tiff_path) as src:
        
        # Get spatial information
        transform = src.transform
        crs = src.crs
        
        # count bands
        num_band = src.count
    
        # Initialize a dictionary to store DataArrays
        data_dict = {}
        
        # Create the coordinates for the x and y dimensions
        left, bottom, right, top = src.bounds
        x = np.linspace(left, right, src.width)
        y = np.linspace(top, bottom, src.height)
        

        # Read each band and create a DataArray for it
        for i in range(num_band):
            band_i = src.read(i + 1)  # Add 1 to the band index to match 1-based indexing
            ds_i = xr.DataArray(band_i, dims=('y', 'x'), 
                                coords={"y": y, "x": x})

            # Assign DataArray to a variable based on band index
            band_name = f'band_{i + 1}' 
            data_dict[band_name] = ds_i.astype(float)


        if rice_model is True:    
        # Calculate new bands
            ndvi_band = (data_dict['band_4'] - data_dict['band_1']) / (data_dict['band_4'] + data_dict['band_1'])
            ndwi_band = (data_dict['band_2'] - data_dict['band_4']) / (data_dict['band_4'] + data_dict['band_2'])
            gndvi_band = (data_dict['band_4'] - data_dict['band_2']) / (data_dict['band_4'] + data_dict['band_2'])

                        
            data_dict['NDVI'] = ndvi_band.astype(float)
            data_dict['NDWI'] = ndwi_band.astype(float)
            data_dict['GNDVI'] = gndvi_band.astype(float)
            
            # # Create an xarray Dataset with all the bands
            # dataset = xr.Dataset({'ndvi': ndvi_band, 'ndwi': ndwi_band, 'gndvi': gndvi_band}).astype(float)

        else:
            pass
            # # Create an xarray Dataset with all the bands
            # dataset = xr.Dataset(data_dict).astype(float)
 

        # Create an xarray Dataset with all the bands
        dataset = xr.Dataset(data_dict).astype(float)

        # Add global attributes if needed
        dataset.attrs['crs'] = str(crs)
        dataset.attrs['transform'] = transform

    return dataset

# the function to create new column in geojson file
# to add classtye table for training data
def geojson_add_Newcol(geojson_file_path):
    with open(geojson_file_path, 'r') as f:
        geojson_data = json.load(f)

    # Count the number of rows in the GeoJSON data
    
    num_rows = len(geojson_data['features'])
    print('num of rows: ',num_rows)
  
    # Prompt the user for the new column name and value
    new_column_name = input("Enter the name of the new column: ")
    # new_column_value = int(input("Enter the value for the new column: "))
    
    # Try to get an integer input for the new column value
    while True:
        new_column_value = input("Enter the value for the new column: ")
        try:
            new_column_value = int(new_column_value)
            break
        except ValueError:
            print("Invalid input: Please enter an integer value.")
    
    # Add the new column to each feature in the GeoJSON data
    for feature in geojson_data['features']:
        feature['properties'][new_column_name] = new_column_value

    # Write the updated GeoJSON data back to the file
    with open(geojson_file_path, 'w') as f:
        json.dump(geojson_data, f)

    # Return the number of rows in the GeoJSON data before the new column was added
    return num_rows

    

# func to convert raster image to polygon
def raster2polygon(file_name, out_shp_fn, band_number=1, field_name="values"):
    """
    Convert a raster to polygon
    :param file_name: STR of target file name, including directory; must end on ".tif"
    :param out_shp_fn: STR of a shapefile name (with directory e.g., "C:/temp/poly.shp")
    :param band_number: INT of the raster band number to open (default: 1)
    :param field_name: STR of the field where raster pixel values will be stored (default: "values")
    :return: None
    """
    # if len(out_shp_fn) < 13:
    #     pass
    # else:
    #     raise ValueError('Shapefile name may not have more than 13 characters')
        
    # ensure that the input raster contains integer values only and open the input raster
    file_name = float2int(file_name)
    raster, raster_band = open_raster(file_name, band_number=band_number)

    # create new shapefile with the create_shp function
    new_shp = create_shp(out_shp_fn, layer_name="raster_data", layer_type="polygon")
    dst_layer = new_shp.GetLayer()

    # create new field to define values
    new_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
    dst_layer.CreateField(new_field)

    # Polygonize(band, hMaskBand[optional]=None, destination lyr, field ID, papszOptions=[], callback=None)
    gdal.Polygonize(raster_band, None, dst_layer, 0, [], callback=None)

    # create projection file
    srs = get_srs(raster)
    make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))
    print("Success: Wrote %s" % str(out_shp_fn)) 
    
 
 # function extension for converting raster image to polygon   
def create_shp(shp_file_dir, overwrite=True, *args, **kwargs):
    """
    :param shp_file_dir: STR of the (relative shapefile directory (ends on ".shp")
    :param overwrite: [optional] BOOL - if True, existing files are overwritten
    :kwarg layer_name: [optional] STR of the layer_name - if None: no layer will be created (max. 13 chars)
    :kwarg layer_type: [optional] STR ("point, "line", or "polygon") of the layer_name - if None: no layer will be created
    :output: returns an ogr shapefile layer
    """
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")

    # check if output file exists if yes delete it
    if os.path.exists(shp_file_dir) and overwrite:
        shp_driver.DeleteDataSource(shp_file_dir)

    # create and return new shapefile object
    new_shp = shp_driver.CreateDataSource(shp_file_dir)

    # create layer if layer_name and layer_type are provided
    if kwargs.get("layer_name") and kwargs.get("layer_type"):
        # create dictionary of ogr.SHP-TYPES
        geometry_dict = {"point": ogr.wkbPoint,
                         "line": ogr.wkbMultiLineString,
                         "polygon": ogr.wkbMultiPolygon}
        # create layer
        try:
            new_shp.CreateLayer(str(kwargs.get("layer_name")),
                                geom_type=geometry_dict[str(kwargs.get("layer_type").lower())])
        except KeyError:
            print("Error: Invalid layer_type provided (must be 'point', 'line', or 'polygon').")
        except TypeError:
            print("Error: layer_name and layer_type must be string.")
        except AttributeError:
            print("Error: Cannot access layer - opened in other program?")
    return new_shp
    
# function to create projection file of a shapfile
def make_prj(shp_file_name, epsg):
    """
    Returns:
        None: Creates a projection file (``.prj``) in the same directory and
        with the same name of ``shp_file_name``.
    """
    shp_dir = shp_file_name.split(shp_file_name.split("/")[-1].split("\\")[-1])
    shp_name = shp_file_name.split(".shp")[0].split("/")[-1].split("\\")[-1]
    with open(shp_dir[0] + shp_name + ".prj", "w+") as prj:
        prj.write(get_wkt(epsg))
        
        
        
def get_wkt(epsg, wkt_format="esriwkt"):
    """Gets WKT-formatted projection information for an epsg code using the ``osr`` library.

    Args:
        epsg (int): epsg Authority code
        wkt_format (str): of wkt format (default is esriwkt for shapefile projections)

    Returns:
        str: WKT (if error: returns default corresponding to ``epsg=4326``).
    """
    default = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'
    spatial_ref = osr.SpatialReference()
    try:
        spatial_ref.ImportFromEPSG(epsg)
    except TypeError:
        logging.error(
            "epsg must be integer. Returning default WKT(epsg=4326).")
        return default
    except Exception:
        logging.error(
            "epsg number does not exist. Returning default WKT(epsg=4326).")
        return default
    if wkt_format == "esriwkt":
        spatial_ref.MorphToESRI()
    return spatial_ref.ExportToPrettyWkt()

    

    
    
        
        
        
    
    
    
         




 