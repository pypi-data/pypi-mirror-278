import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from Godream.convertool import xarray_ds
from Godream.classification import predict_xray


# Model for rice classification from SAR VH(19 bands, crs 4326)
# by Random foreset classification
def riceBySar(raster_stack = True, output_tiff = True, figsize = None, num_estimator = None ):
    '''
    raster_stack: the stacking of SAR images path (this model use specifically 19 image)
    
    output_tiff: classified output path
    
    figsize: set figure size of image to plot. The defualt is figsize = (12, 6).
    
    num_estimator: the number of trees in RF classifier. The defult is 500. 
    
    '''
    # read raster file
    raster = rasterio.open(raster_stack)
    
    # check num of bands stacked
    numband = raster.count
    
    if numband < 19:
        raise ValueError ('this model need 19 bands stacked')
    elif numband > 19:
        raise ValueError ('this model need 19 bands stacked')
    else:
        pass
    
    # check CRS
    ref_crs = 'EPSG:4326'
    da = raster.crs
    
    if da != ref_crs:
        raise ValueError ('the CRS of raster should be EPSG:4326')
    
    # create xarray ds 
    print('Creating Xarray dataset')
    
    # input ds
    ds_input = xarray_ds(tiff_path=raster_stack)
    
    print('Finish to create Xarray dataset')
    
    
    # read training set
    gdf =gpd.read_file('data\SAR_VH_1721.geojson')
    
    # training data preparation
    columns_to_convert = ['classtype','T1','T2','T3','T4','T5','T6','T7','T8','T9',
                      'T10','T11','T12','T13','T14','T15','T16','T17','T18','T19']  

    # select column to use
    model_input1 = gdf[columns_to_convert]
    
    # convert to np array
    model_input2 = model_input1[columns_to_convert].to_numpy()
    
    model_input2[:, 0] = np.where(model_input2[:, 0] == 1, 1, 0)
    
    # Split into training and testing data
    model_train, model_test = model_selection.train_test_split(model_input2, 
                                                               stratify = model_input2[:, 0], 
                                                               train_size=0.7, 
                                                               random_state=0)
    print("Train shape:", model_train.shape)
    print("Test shape:", model_test.shape)
    
    # Select the variables we want to use to train our model
    model_variables = columns_to_convert[1:]

    # Extract relevant indices from the processed shapefile
    model_col_indices = [
    columns_to_convert.index(var_name) for var_name in model_variables ]
    
    # set number of estimator
    if num_estimator is None:
        num_estimator = 500
    
    print('num of estimator: ', num_estimator)
    
    # initial the model
    rf_model = RandomForestClassifier(n_estimators= num_estimator, random_state=42)
    
    # Train model
    rf_model.fit(model_train[:, model_col_indices], model_train[:, 0])
    
    # validate acc of model
    predictions = rf_model.predict(model_test[:, model_col_indices])
    
    acc = accuracy_score(predictions, model_test[:, 0])

    print ('the accuracy of model :', acc )
    
    # Predict using the trained model
    predicted = predict_xray(rf_model, ds_input, clean=True)
    
    print('predicting finish!!!')
    
    # export to geotiff
    predicted.Predictions.rio.to_raster(output_tiff,  # tiff file
                                    driver='GTiff', 
                                    dtype='float64', 
                                    crs = ds_input.geobox.crs,
                                    )
    print('exported result to your output path')
    
    print('Note that: the output will be upside down, You can flip it in ArcMap software.')
    
    # set figure size for plot output image
    if figsize is None:
        figsize = (12, 6)
    
    # Set up plot result
    fig, axes = plt.subplots(1, 1, figsize = figsize)  # Set up one subplot

    # Plot classified image
    predicted.Predictions.plot(ax=axes, 
                               cmap='Greens', 
                               add_labels=False, 
                               add_colorbar=False)
    
    # Reverse the Y-axis to match your desired orientation
    axes.invert_yaxis()

    # Add a plot title
    axes.set_title('Classified Data')

    # Display the plot
    plt.show()
    
    
# Model to classify rice cultivated area from Optical image
def riceByOptical(raster_img = True, output_tiff = True, figsize = None, num_estimator = None ):
    '''
    raster_img: the raster images path. This model need specific 4 bands 
                that comprise red_band, green_band, blue_band and nir_band, 
                respectively.
    
    output_tiff: classified output path
    
    figsize: set figure size of image to plot. The defualt is figsize = (12, 6).
    
    num_estimator: the number of trees in RF classifier. The defult is 500. 
    
    '''
    
    # read raster file
    raster = rasterio.open(raster_img)
    
    # check num of bands stacked
    numband = raster.count
    
    print("Note: Raster images should have 4 bands that compose of red, green, blue and nir respectively. ")
    
    # check CRS
    ref_crs = 'EPSG:4326'
    da = raster.crs
    
    if da != ref_crs:
        raise ValueError ('the CRS of raster should be EPSG:4326')
    
    # create xarray ds 
    print('Creating Xarray dataset')
    
    # input ds
    ds_input = xarray_ds(tiff_path=raster_img, rice_model = True)
    
    print('Finish to create Xarray dataset')
    
    # read training set
    gdf =gpd.read_file('data/trainset_index.geojson')
    
    # training data preparation
    columns_to_convert = ['class', 'band_1', 'band_2', 'band_3', 'band_4', 'ndvi', 'ndwi', 'gndvi']  

    # select column to use
    model_input1 = gdf[columns_to_convert]
    
    # convert to np array
    model_input2 = model_input1[columns_to_convert].to_numpy()
    
    model_input2[:, 0] = np.where(model_input2[:, 0] == 111, 1, 0)
    
    # Split into training and testing data
    model_train, model_test = model_selection.train_test_split(model_input2, 
                                                               stratify = model_input2[:, 0], 
                                                               train_size=0.7, 
                                                               random_state=0)
    print("Train shape:", model_train.shape)
    print("Test shape:", model_test.shape)
    
    # Select the variables we want to use to train our model
    model_variables = columns_to_convert[1:]

    # Extract relevant indices from the processed shapefile
    model_col_indices = [
    columns_to_convert.index(var_name) for var_name in model_variables ]
    
    # set number of estimator
    if num_estimator is None:
        num_estimator = 500
    
    print('num of estimator: ', num_estimator)
    
    print("Call Random Forest Classifier")
    
    # initial the model
    rf_model = RandomForestClassifier(n_estimators= num_estimator, random_state=42)
    
    # Train model
    rf_model.fit(model_train[:, model_col_indices], model_train[:, 0])
    
    # validate acc of model
    predictions = rf_model.predict(model_test[:, model_col_indices])
    
    print("train model")
    
    acc = accuracy_score(predictions, model_test[:, 0])

    print ('the accuracy of model :', acc )
    
    # Predict using the trained model
    predicted = predict_xray(rf_model, ds_input, clean=True)
    
    print('predicting finish!!!')
    
    # export to geotiff
    predicted.Predictions.rio.to_raster(output_tiff,  # tiff file
                                    driver='GTiff', 
                                    dtype='float64', 
                                    crs = ds_input.geobox.crs,
                                    )
    print('exported result to your output path')
     
    # set figure size for plot output image
    if figsize is None:
        figsize = (12, 6)
    
    # Set up plot result
    fig, axes = plt.subplots(1, 1, figsize = figsize)  # Set up one subplot

    # Plot classified image
    predicted.Predictions.plot(ax=axes, 
                               cmap='Greens', 
                               add_labels=False, 
                               add_colorbar=False)
    


    # Add a plot title
    axes.set_title('Classified Data')

    # Display the plot
    plt.show()