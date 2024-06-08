from setuptools import setup, find_packages

setup(
    name='5dee',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'GeoPandas',
        'Shapely',
        'Fiona',
        'Spatialpandas',
        'pySAL',
        'GDAL',
        'Rasterio',
        'Datashader',
        'Xarray-Spatial',
        'H3',
        'NetworkX',
        'PyProj',
        'folium',
        'PaddleSpatial',
        'rerun'
    ],
    url='https://github.com/8gratitude8/5dee',
    author='GRATITUD3.ETH',
    author_email='gratitude@5-dee.com',
    description='A package to install all necessary dependencies for spatial compute and remote agtech'
)
