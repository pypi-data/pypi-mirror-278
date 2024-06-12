from setuptools import setup, find_packages

DESC ='Godream (Geo-dream) is a library that contain  geospatial tools for RS&GIS analyse in python language. This appears to be a Python library specifically developed to assist in the analysis of geospatial data, with a focus on remote sensing and GIS applications. Such a library would likely provide functions and tools to manipulate, process, and visualize geospatial data, making it easier for users to perform complex analyses in these domains.' 

setup(
    name='Godream',
    packages=['Godream'],
    version='0.1.2',
    license='MIT',
    author_email='dreamusaha@gmail.com',
    description= 'This is a library that contain geospatial tools in python for Remote sensing and GIS applications. This project is part of Open data of Gistda project. ',
    long_description= DESC,
    author='Pathakorn Usaha',
    url= 'https://github.com/DreamPTK/Godream',
    download_url= 'https://github.com/DreamPTK/Godream/archive/refs/tags/v0.0.1.zip',
    keywords= ['geography','geospatial','GIS', 'RS', 'Geospatial analysis'],
    install_requires= ["dask", "dask_ml", "xarray", 'joblib', 'datacube', 'rasterio', 'rioxarray', 
                       'geopandas',' jsons', 'numpy', 'matplotlib', 'scikit-learn','folium','flusstools', 'shapely' ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3.9',
        ],
    )

