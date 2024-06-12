import os
import logging
import numpy as np
import rasterio
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from rasterio.io import DatasetReader
from rasterio.transform import guard_transform
from collections import OrderedDict
from folium.plugins import Draw, Geocoder, Fullscreen
from folium.plugins import LocateControl, MousePosition, MeasureControl
from folium.raster_layers import ImageOverlay


logger = logging.getLogger(__name__)

# func to check matplotlib
def check_plt():
    try:
        import matplotlib.pyplot as plt
        return plt
    except (ImportError, RuntimeError): 
        error_message = (
            "Unable to import matplotlib.\n"
            "matplotlib is required for plotting functions."
        )
        raise ImportError(error_message)


# func to plot raster image (single band)
def plot_raster(input_data, with_bounds=True, contour=False, contour_label_kws=None,
         ax=None, title=None, transform=None, adjust=False, cmap=None, figsize=None, gamma=None, **kwargs):

    # check matplotlib package
    plt = check_plt()

    # If figsize is not provided, set a defualt
    if figsize is None:
        figsize=(15, 10) 

    # Create a figure with the specified figsize
    fig,ax = plt.subplots(figsize=figsize)

    # Check if the input_data is a tuple
    if isinstance(input_data, tuple):
        # Read data from the specified band index of the dataset
        arr = input_data[0].read(input_data[1])
    
        # Check if the array has multiple dimensions (potentially an image)
        if len(arr.shape) >= 3:
            arr = reshape_as_image(arr)
    
        # Adjust extent if with_bounds is True
        if with_bounds:
            kwargs['extent'] = plotting_extent(input_data[0])
    
    # Check if the input_data is a DatasetReader object
    elif isinstance(input_data, DatasetReader):
        # Adjust extent if with_bounds is True
        if with_bounds:
            kwargs['extent'] = plotting_extent(input_data)
    
        # Check the number of raster bands in the dataset
        if input_data.count == 1:

            # Read a single band with masking
            arry = input_data.read(1, masked=True)
            arr = np.nan_to_num(arry) # fill nan

            
        else:
            try:
                # Create a colorinterp lookup table for band reordering
                source_colorinterp = OrderedDict(zip(input_data.colorinterp, input_data.indexes))
                colorinterp = rasterio.enums.ColorInterp
    
                # Collect indexes of RGB channels in the specified order
                rgb_indexes = [
                    source_colorinterp[ci]
                    for ci in (colorinterp.red, colorinterp.green, colorinterp.blue)
                ]
    
                # Read RGB channels and reshape to image format
                arry = input_data.read(rgb_indexes, masked=True)
                arr = np.nan_to_num(arry) # fill nan
                arr = reshape_as_image(arr)
                
    
            # Handle KeyError (e.g., if RGB channels are not defined)
            except KeyError:
                # Read a single band with masking
                arry = input_data.read(1, masked=True)
                arr = np.nan_to_num(arry) # fill nan
                
    # Handle input_data as a numpy array
    else:
        # Squeeze the numpy array to remove single-dimensional entries
        input_data = np.ma.squeeze(input_data)
    
        # Check if the array has multiple dimensions (potentially an image)
        if len(input_data.shape) >= 3:
            arr = reshape_as_image(input_data)
        else:
            arr = input_data
    
        # Adjust extent if both transform and with_bounds are specified
        if transform and with_bounds:
            kwargs['extent'] = plotting_extent(arr, transform)

    # If cmap is not provided, set it to the default colormap you want
    if cmap is None:
        cmap = 'gist_earth' 

    # Adjust pixel values for proper RGB plotting
    if adjust and arr.ndim >= 3:
        # Adjust each band by the min/max so it will plot as RGB.
        arr = reshape_as_raster(arr).astype("float64")

        for ii, band in enumerate(arr):
            arr[ii] = adjust_band(band)

        arr = reshape_as_image(arr)

    # Check gamma
    if gamma is None:
        gamma = 0.5
    
    # Enhance brightness using PowerNorm
    norm = mcolors.PowerNorm(gamma=gamma)
    arr = norm(arr)

    # Initialize a flag for showing the plot
    show = False

    # If ax is not provided, create a new Axes object
    if not ax:
        show = True
        ax = plt.gca()

    # Plot as contours if contour flag is True
    if contour:
        if 'cmap' not in kwargs:
            kwargs['colors'] = kwargs.get('colors', 'red')

        kwargs['linewidths'] = kwargs.get('linewidths', 1.5)
        kwargs['alpha'] = kwargs.get('alpha', 0.8)

        C = ax.contour(arr, origin='upper', **kwargs)

        # Set contour label properties
        if contour_label_kws is None:
            contour_label_kws = dict(fontsize=8, inline=True)

        if contour_label_kws:
            ax.clabel(C, **contour_label_kws)
    else:
        # Plot as image
        ax.imshow(arr, cmap=cmap, **kwargs)
        plt.colorbar(ax.imshow(arr, cmap=cmap, **kwargs), ax=ax)
        
    # Set the plot title if provided
    if title:
        ax.set_title(title, fontweight='bold')

    # Show the plot if required
    if show:
        plt.show()

    # Return the Axes object
    return ax


# func to returns the extent of the data in a format suitable for use.
def plotting_extent(source, transform=None):
    """
     Returns an extent in the format needed
     for :func:`matplotlib.pyplot.imshow` (left, right, bottom, top)
     instead of rasterio's bounds (left, bottom, right, top)

    """
    if hasattr(source, 'bounds'):
        # If the source has 'bounds' attribute (like a rasterio dataset), use those bounds
        extent = (source.bounds.left, source.bounds.right,
                  source.bounds.bottom, source.bounds.top)
    elif not transform:
        # If the source is an array, but no transform is provided, raise an error
        raise ValueError("transform is required if source is an array")
    else:
        # If the source is an array, calculate extent using the provided transform
        transform = guard_transform(transform)
        rows, cols = source.shape[0:2]
        left, top = transform * (0, 0)
        right, bottom = transform * (cols, rows)
        extent = (left, right, bottom, top)

    return extent

def reshape_as_image(arr):
    """
    swapping the axes order from (bands, rows, columns)
    to (rows, columns, bands)

    """
    # swap the axes order from (bands, rows, columns) to (rows, columns, bands)
    im = np.ma.transpose(arr, [1, 2, 0])
    return im


def reshape_as_raster(arr):
    """
    Returns the array in a raster order
    by swapping the axes order from (rows, columns, bands)
    to (bands, rows, columns)

    """
    # swap the axes order from (rows, columns, bands) to (bands, rows, columns)
    im = np.transpose(arr, [2, 0, 1])
    return im

# func to plot histogram
def plot_hist(source, bins=10, masked=True, title='Histogram', ax=None, label=None, **kwargs):
    """
    Display a histogram of raster data using matplotlib.

    """
    # check matplotlib available
    plt = check_plt()


    # Read data from the provided source
    if isinstance(source, DatasetReader):
        arr = source.read(masked=masked)
    elif isinstance(source, (tuple, rasterio.Band)):
        arr = source[0].read(source[1], masked=masked)
    else:
        arr = source
    # Determine the range of values for the histogram plot
    rang = np.nanmin(arr), np.nanmax(arr)

    # Reshape the data if necessary
    if len(arr.shape) == 2:
        arr = np.expand_dims(arr.flatten(), 0).T
        colors = ['gold']
    else:
        arr = arr.reshape(arr.shape[0], -1).T
        colors = ['red', 'green', 'blue', 'violet', 'gold', 'saddlebrown']

    # Add more colors if needed
    if arr.shape[-1] > len(colors):
        n = arr.shape[-1] - len(colors)
        colors.extend(np.ndarray.tolist(plt.get_cmap('Accent')(np.linspace(0, 1, n))))
    else:
        colors = colors[:arr.shape[-1]]

    # Handle labels for legend
    if label:
        labels = label
    # else, create default labels
    else:
        # If a rasterio.Band() is given make sure the proper index is displayed
        # in the legend.
        if isinstance(source, (tuple, rasterio.Band)):
            labels = [str(source[1])]
        else:
            labels = (str(i + 1) for i in range(len(arr)))

    # Determine if an Axes object is provided or needs to be created
    if ax:
        show = False
    else:
        show = True
        ax = plt.gca()

    fig = ax.get_figure()

    # Plot the histograms
    ax.hist(arr,
            bins=bins,
            color=colors,
            label=labels,
            range=rang,
            **kwargs)

    ax.legend(loc="upper right")
    ax.set_title(title, fontweight='bold')
    ax.grid(True)
    ax.set_xlabel('DN')
    ax.set_ylabel('Frequency')

    # Show the plot if required
    if show:
        plt.show()


def adjust_band(band, kind=None):
    """
    Adjust a band to be between 0 and 1.

    """
    # Minimum pixel value
    img_min = np.float64(np.nanmin(band))
    # Maximum pixel value
    img_max = np.float64(np.nanmax(band))

    # Adjust pixel values
    px=(band - img_min) / (img_max - img_min)
    return px




# func to create interactive map from lat/lon
def show_map(lat=None, lon=None, with_draw_tools=True,zoom=None):
    """Create a map using Folium."""
    
    # Set default latitude and longitude values
    if lat is None:
        lat = 13.726 # Bangkok latitude
    if lon is None:
        lon = 100.514  # Bangkok longitude
    
     # set default zoom level
    if zoom is None:
        zoom = 6
             
    # Create a map using Folium defualt: crs='EPSG3857'
    m = folium.Map(location=[lat, lon],zoom_start=zoom, tiles = None )

    # # lat/lon popup
    # m.add_child(folium.LatLngPopup())
    
    # add geocoder plugin
    geocoder = Geocoder(position='topleft', collapsed=True, show=True)
    geocoder.add_to(m)
    
    # # add masker location
    # folium.Marker([lat, lon], 
    #               icon=folium.Icon(color="red", icon="flag")).add_to(m)
    
    # add fullscreen plugin
    Fullscreen().add_to(m) 
    
    LocateControl().add_to(m)
    
    # measurement
    MeasureControl(position="bottomright").add_to(m)
    
    
    MousePosition(  position="bottomleft",
                    separator=" | ",
                    prefix="&copy; GODream | Lat/Lon:",
                    num_digits=4,
                ).add_to(m)
    
  
    # add tile layer map
    folium.TileLayer('https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', name='Terrain', attr='Google').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', name='Hybrid', attr='Google').add_to(m)
    folium.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', name='OpenStreetMap', attr='OpenStreetMap').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/sphere_hybrid/EPSG3857/{z}/{x}/{y}.jpeg?key=42B90819583344A789DA424BE70CDB61', name='Gistda Hybrid', attr='sphere.gistda').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/thailand_images/EPSG3857/{z}/{x}/{y}.jpeg?key=test2022', name='Gistda Satellite', attr='sphere.gistda').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=m@221097413,traffic&x={x}&y={y}&z={z}', name='Traffic', attr='Google').add_to(m)


    # add WMS
    folium.WmsTileLayer(
    url="https://basemap.sphere.gistda.or.th/service?key=test2022",
    name="Gistda streets",
    fmt="image/png",
    layers='sphere_streets',
    attr=u"gistda",
    transparent=True,
    overlay=False,
    control=True,
    
    ).add_to(m)
    
    folium.WmsTileLayer(
    url="http://ows.terrestris.de/osm/service?",
    name="Hillshade",
    fmt="image/png",
    layers='SRTM30-Colored-Hillshade',
    attr=u"OSM",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
    
    folium.WmsTileLayer(
    url="http://ows.mundialis.de/services/service?",
    name="Topology",
    fmt="image/png",
    layers='TOPO-WMS,OSM-Overlay-WMS',
    attr=u"OSM",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
    
    folium.WmsTileLayer(
    url="http://ows.terrestris.de/osm/service?",
    name="OSM",
    fmt="image/jpeg",
    layers='OSM-WMS',
    attr=u"OSM",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
    
    
    folium.WmsTileLayer(
    url="https://ms.longdo.com/mapproxy/service",
    name="Topology_longdo",
    fmt="image/png",
    layers='bluemarble_terrain',
    attr=u"gistda",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
        
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google').add_to(m)

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Add drawing tools to create the polygon
    if with_draw_tools:
        
        draw = Draw(
            export=True,
            filename='drawn_polygons.geojson',
            draw_options={
                'polygon': {'allowIntersection': True},
                'rectangle': {'allowIntersection': True},
                'circle':  {'allowIntersection': True},
                'marker':  {'allowIntersection': True},
                'polyline':  {'allowIntersection': True},
            },
            edit_options={
                'featureGroup': None,
            },
        )

        draw.add_to(m)

    return m
        
        
#func to create overlay interactive map 
def overlay_map(vector_file=None, raster_file=None, with_draw_tools=True,zoom=None , opacity = None):
    """Create a map using Folium."""
    if zoom is None:
        zoom = 11

    if opacity is None:
        opacity = 1
    
    if vector_file is None:
        
        # Open the raster file for reading
        with rasterio.open(raster_file[0]) as src:
            
            # check crs
            ref= src.crs
            defult_crs = "EPSG:4326"
            second_crs = "EPSG:3857"
            if ref == defult_crs:
                pass
            elif ref == second_crs:
                pass
            else:
                raise ImportError("Need crs in EPSG:4326 or 3857")
            
            
            # Get the bounds 
            bound = src.bounds
            
            # Transform the bounds to latitude and longitude
            lat_min, lat_max = bound.bottom, bound.top
            lon_min, lon_max = bound.left, bound.right

        # Calculate the center of the bounds
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
            
        # Create a map using Folium defualt: crs='EPSG3857'
        m = folium.Map(location=[center_lat, center_lon],zoom_start=zoom, tiles = None )

    else:
        # Create a Folium map centered on the first polygon of the first file
        polygons = gpd.read_file(vector_file[0])
        center_lon, center_lat = polygons['geometry'][0].centroid.coords[0]

        # Create a map using Folium defualt: crs='EPSG3857'
        m = folium.Map(location=[center_lat, center_lon],zoom_start=zoom, tiles = None )

        # Define a list of colors to use for each file (only 18 layers)
        colors = ['lime','blue', 'red', 'yellow','#40E0D0', 'orange', 'CA33FF','Aqua','Fuchsia',
             'darkblue','darkgreen', 'cyan', 'chartreuse','crimson', 'magenta', 'indigo','tomato','teal']

        # Read each GeoJSON file and create a GeoDataFrame
        gdfs = [gpd.read_file(file) for file in vector_file]
    
        # Add each GeoDataFrame as a separate layer with a different color
        for i, gdf in enumerate(gdfs):
            filename = os.path.splitext(os.path.basename(vector_file[i]))[0]
            folium.GeoJson(gdf,
                    name=  filename,
                    style_function=lambda x, color=colors[i]: {'color': color, 'fillOpacity': 0.2},
                    tooltip=gdf.columns.tolist()).add_to(m)

###################### Raster part ######################################

    # Read the raster image using rasterio
    if raster_file:
        
        for x in raster_file:
            with rasterio.open(x) as src:
                
                # Extract the base name of the input file (without extension)
                input_file_name = os.path.splitext(os.path.basename(x))[0]
                
                if src.count >= 3:
                    
                    # read bands
                    band_1 = src.read(1)
                    band_2 = src.read(2)
                    band_3 = src.read(3)

                    # fill nan with zero
                    band1 = np.nan_to_num(band_1, nan = 0 )
                    band2 = np.nan_to_num(band_2, nan = 0 )
                    band3 = np.nan_to_num(band_3, nan = 0 )

                    bounds = src.bounds

                    # norm value to (0-1)
                    red_n = normalize(band3)
                    green_n = normalize(band2)
                    blue_n = normalize(band1)

                    # Stack the bands to create the RGB image
                    rgb_image= np.dstack((red_n, green_n, blue_n))
                        
                else:
                    # read first band
                    band = src.read(1, masked=True)
                    
                    # If NaN values are present, replace them with a default value (e.g., 0)
                    band = np.nan_to_num(band, nan=0)
                    # band = np.ma.filled(band, fill_value=0)

                    # Create a grayscale image using the specified band
                    rgb_image = np.dstack([band] * 3)
                    
                    bounds = src.bounds

                # Create an ImageOverlay using Folium
                overlay = ImageOverlay(image= rgb_image, 
                                       bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                                       colormap=lambda x: (0.1, 0.2, 0.5, x),
                                       name= input_file_name,
                                       alt="GODream",
                                       interactive=True,
                                       cross_origin=False,
                                       opacity=opacity,
                                       )
                overlay.add_to(m)
                
                
    #########################################################################
            
    # lat/lon popup
    # m.add_child(folium.LatLngPopup())

    # add geocoder plugin
    geocoder = Geocoder(position='topleft', collapsed=True, show=True)
    geocoder.add_to(m)
 
    # add tile layer map
    folium.TileLayer('https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', name='Terrain', attr='Google').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', name='Hybrid', attr='Google').add_to(m)
    folium.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', name='OpenStreetMap', attr='OpenStreetMap').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/sphere_hybrid/EPSG3857/{z}/{x}/{y}.jpeg?key=42B90819583344A789DA424BE70CDB61', name='Gistda Hybrid', attr='sphere.gistda').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/thailand_images/EPSG3857/{z}/{x}/{y}.jpeg?key=test2022', name='Gistda Satellite', attr='sphere.gistda').add_to(m)

    # add WMS
    folium.WmsTileLayer(
    url="https://basemap.sphere.gistda.or.th/service?key=test2022",
    name="Gistda streets",
    fmt="image/png",
    layers='sphere_streets',
    attr="gistda",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
    
    folium.WmsTileLayer(
    url="http://ows.terrestris.de/osm/service?",
    name="Hillshade",
    fmt="image/png",
    layers='SRTM30-Colored-Hillshade',
    attr="OSM",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
    
    folium.WmsTileLayer(
    url="http://ows.mundialis.de/services/service?",
    name="Topology",
    fmt="image/png",
    layers='TOPO-WMS,OSM-Overlay-WMS',
    attr="OSM",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)
    
    folium.WmsTileLayer(
    url="http://ows.terrestris.de/osm/service?",
    name="OSM_terrestris",
    fmt="image/png",
    layers='OSM-WMS',
    attr="OSM",
    transparent=True,
    overlay=False,
    control=True,
    ).add_to(m)

    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google').add_to(m) 
    
    # add fullscreen plugin
    Fullscreen().add_to(m) 
    
    # measurement
    MeasureControl(position="bottomright").add_to(m)

    # LocateControl
    LocateControl().add_to(m)
    
    MousePosition(  position="bottomleft",
                    separator=" | ",
                    prefix="&copy; GODream | Lat/Lon:",
                    num_digits=4,
                    ).add_to(m)
    
    
    # Add layer control to the map
    folium.LayerControl().add_to(m)
    
    # Add drawing tools to create the polygon
    if with_draw_tools:
        
        draw = Draw(
            export=True,
            filename='drawn_polygons.geojson',
            draw_options={
                'polygon': {'allowIntersection': True},
                'rectangle': {'allowIntersection': True},
                'circle':  {'allowIntersection': True},
                'marker':  {'allowIntersection': True},
                'polyline':  {'allowIntersection': True},
            },
            edit_options={
                'featureGroup': None,
            },
        )

        draw.add_to(m)

    return m

# function for plot_multibands 
def normalize(band):
    band_min, band_max = (band.min(), band.max())
    return ((band-band_min)/((band_max - band_min)))

def brighten(band):
    alpha=0.13
    beta=0
    return np.clip(alpha*band+beta, 0,255)

# function to plot raster in multi-bands raster
def plot_multibands(raster_file, bands = None,  brightness = None):
    
     # set bands
     if bands is None:
            bands = [3,2,1]
     else:
         pass
         
     # set bright default
     if brightness is None:
         brightness = 0.85
     else:
         pass

     with rasterio.open(raster_file) as ds:

        # check num of bands
        num_bands= ds.count
        er_message = ("Image file need at least 3 bands to plot multi-bands")
        if num_bands<3:
            raise IndexError(er_message)
        else: pass


        a = bands[0]
        b = bands[1]
        c = bands[2]

        print('band:',a,'|','band:',b,'|','band:',c)

        # read band 
        band1 = ds.read(a)
        band2 = ds.read(b)
        band3 = ds.read(c)
        
        # fill nan with zero
        band1 = np.nan_to_num(band1)
        band2 = np.nan_to_num(band2)
        band3 = np.nan_to_num(band3)
         
        # norm value to (0-1)
        red_n = normalize(band1)
        green_n = normalize(band2)
        blue_n = normalize(band3)
    
        # rgb stack
        rgb_composite_n= np.dstack((red_n, green_n, blue_n))

        # plot img
        plt.imshow(rgb_composite_n,  alpha=brightness )

    