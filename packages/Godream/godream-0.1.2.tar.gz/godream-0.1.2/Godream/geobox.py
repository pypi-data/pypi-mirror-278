import os
import json
import geojson
import rasterio
import geopandas as gpd
from osgeo import gdal 




# the merge tool combines datasets that are the same datatype into one   
def merge(files, output_file):
    # Initialize an empty list of features
    features = []

    # Loop through all the input files and add their features to the list
    for file in files:
        with open(file) as f:
            data = json.load(f)
            features += data['features']

    # Create a new GeoJSON object
    new_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Write the new GeoJSON file
    with open(output_file, 'w') as f:
        geojson.dump(new_data, f)
        
        
# function for intersect
def intersect(file_paths, output_file):
    
    # Read each GeoJSON file and create a GeoDataFrame
    gdfs = [gpd.read_file(fp) for fp in file_paths]
    
    # perform intersect on each pair of geodataframe
    result = gdfs[0]
    for gdf in gdfs[1:]:
        result = result.intersection(gdf)
        
    #save result to output file
    result.to_file(output_file)
    
    
# function for union
def union(file_paths, output_file):
    
    # read each files and create a geodataframe
    gdfs = [gpd.read_file(fp) for fp in file_paths]
    
    # perfrom Union on each pair of Geodataframe
    result = gdfs[0]
    for gdf in gdfs[1:]:
        result = result.union(gdf)
    # save to output file
    result.to_file(output_file)
    
    
# func for Erase/Difference    
def erase(file, erase_file, output_file):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    gdfe = gpd.read_file(erase_file)
    
    # perform func
    result = gdf.overlay(gdfe, how = 'difference')
    
    # savs to output
    result.to_file(output_file)
    

#func for clip (can both Vector and raster)
def clip(input_path, clip_path, output_path):
    
    # init
    is_RV = False
    is_VV = False
    
    # Check if the operation involves Raster-Vector (RV) or Vector-Vector (VV) clipping
    if input_path.lower().endswith('.tif') and (clip_path.lower().endswith('.shp') or clip_path.lower().endswith('.geojson')):
        is_RV = True
    elif (input_path.lower().endswith('.shp') or input_path.lower().endswith('.geojson')) and (clip_path.lower().endswith('.shp') or clip_path.lower().endswith('.geojson')):
        is_VV = True
    
           
    if is_VV is True:
        # read input and clip file
        gdf = gpd.read_file(input_path)
        gdfc = gpd.read_file(clip_path)

        # clip function
        result = gpd.clip(gdf, gdfc)

        # save to output
        result.to_file(output_path)
    
    if is_RV is True:
        gdal.Warp(output_path, 
                  input_path, 
                  cutlineDSName=clip_path, 
                  cropToCutline=True)
        
    
#func for Symmetrical difference
def smc_difference(file, diff_file, output_file):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    gdfd = gpd.read_file(diff_file)
    
    # perform function
    result = gdf.overlay(gdfd, how = 'symmetric_difference')
    
    #save to output
    result.to_file(output_file)
    

# func for dissolve    
def dissolve(file, output, dissolve_by):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    
    # perform func
    result = gdf.dissolve(by=dissolve_by)
       
    #save to output
    result.to_file(output)
    
    
# func for buffer ie. buffer = 0.005 (500 meter)
def buffer(file, output, buffer_num):
    
    # read input and erase file
    gdf = gpd.read_file(file)
       
    # perform func
    result = gdf.buffer(buffer_num)
            
    #save to output
    result.to_file(output)
    
# function to find the center of polygon  
def find_centroid(file, output):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    
    # perform func
    result = gdf.centroid
    
        #save to output
    result.to_file(output)
    
 # function for band stacking
# def stack_bands(band_paths, output_path): 
#     """
#     Stack multiple input raster bands into a single output raster file.

#     Parameters:
#         band_paths (list of str): List of input raster band file paths to be stacked.
#         output_path (str): Output raster file path.
#     """
#     num_bands = len(band_paths)
    
#     # Open the first band to get geospatial information
#     first_band = gdal.Open(band_paths[0])

#     # Get band dimensions and data type
#     x_size = first_band.RasterXSize
#     y_size = first_band.RasterYSize
#     data_type = first_band.GetRasterBand(1).DataType

#     # Create the output dataset
#     driver = gdal.GetDriverByName("GTiff")  # You can change the output format here
#     output_dataset = driver.Create(output_path, x_size, y_size, num_bands, data_type)

#     # Set the projection and geotransform
#     output_dataset.SetProjection(first_band.GetProjection())
#     output_dataset.SetGeoTransform(first_band.GetGeoTransform())

#     # Loop through input bands and copy data to the output dataset
#     for i, band_path in enumerate(band_paths, start=1):
#         band = gdal.Open(band_path)
#         band_data = band.GetRasterBand(1).ReadAsArray()
#         output_dataset.GetRasterBand(i).WriteArray(band_data)

#     # Close the output dataset
#     output_dataset = None
    

def stack_bands(band_paths, output_path): # work
    """
    Stack multiple input raster bands into a single output raster file.

    Parameters:
        band_paths (list of str): List of input raster band file paths to be stacked.
        output_path (str): Output raster file path.
    """
    num_bands = len(band_paths)
    
    # Open the first band to get geospatial information
    first_band = gdal.Open(band_paths[0])

    # Get band dimensions and data type
    x_size = first_band.RasterXSize
    y_size = first_band.RasterYSize
    data_type = first_band.GetRasterBand(1).DataType

    # Create the output dataset
    driver = gdal.GetDriverByName("GTiff")  # You can change the output format here
    output_dataset = driver.Create(output_path, x_size, y_size, num_bands, data_type)

    # Set the projection and geotransform
    output_dataset.SetProjection(first_band.GetProjection())
    output_dataset.SetGeoTransform(first_band.GetGeoTransform())

    # Loop through input bands and copy data to the output dataset
    for i, band_path in enumerate(band_paths, start=1):
        band = gdal.Open(band_path)
        band_data = band.GetRasterBand(1).ReadAsArray()
        output_dataset.GetRasterBand(i).WriteArray(band_data)

    # Close the output dataset
    output_dataset = None
    
    
# function to extract data by points
def extract_by_point( raster, points, output_vector = None):
    '''
    raster: raster data in geotiff file.
    points: points (vector data) in geojson or shapefile.
    
    '''
    # Read the vector mask (e.g., shapefile)
    gdf = gpd.read_file(points)
    
    # Open the raster file
    with rasterio.open(raster) as src:
        # Loop through each point in the GeoDataFrame
        for idx, point in gdf.iterrows():
            # Extract pixel values at the coordinates of the point
            row, col = src.index(point['geometry'].x, point['geometry'].y)
            pixel_values = src.read(indexes=list(range(1, src.count + 1)), window=((row, row+1), (col, col+1)))

            # Assign the pixel values to new columns in the GeoDataFrame
            for band_num, values in enumerate(pixel_values, start=1):
                gdf.at[idx, f'band_{band_num}'] = values[0] 
                
    # Write out the GeoDataFrame to a  file with the specified CRS and encoding
    gdf.to_file(output_vector, driver='GeoJSON', encoding='utf-8')
                
    return gdf
                



def merge_df(files, output_file):
    # Initialize an empty list of features
    features = []

    # Loop through all the input files and add their features to the list
    for file in files:
        with open(file) as f:
            data = json.load(f)
            features += data['features']

    # Create a new GeoJSON object
    new_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Write the new GeoJSON file
    with open(output_file, 'w') as f:
        geojson.dump(new_data, f)
                  
    
    
