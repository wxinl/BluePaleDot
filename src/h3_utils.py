import os, sys

import warnings
warnings.filterwarnings('ignore')

from matplotlib import pyplot as plt

import pandas as pd
import geopandas as gpd
import numpy as np
import sklearn

import h3
import h3pandas


from shapely import geometry
from shapely.geometry import Polygon



from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString
import itertools

from operator import itemgetter
def hex_generator(gdf, r):
    """
    input: boundary file, list of resolution
    output: hexagons of desired resolution geodataframes
    """
    print('Starting...')
    gdf_proj = gdf.copy()
    gdf_proj['geometry'] = gdf_proj.to_crs(3857).buffer(5000)
    gdf_proj = gdf_proj.to_crs(4326)
    print('Done')

    ## generate hex
    print('Generating hex at level', r)
    hexagons = list(set([i for j in gdf_proj.h3.polyfill(r)['h3_polyfill'].to_list() for i in j]))
    hex_geoms = [hex2poly(hexagon) for hexagon in hexagons]
    hex_gdf = gpd.GeoDataFrame(data={'hex'+str(r): hexagons, 'geometry':hex_geoms}, crs=4326)
    print('Done')
    
    ## refine to boundary
    # select ones that are within the boundary

    result_gdf = refine_sjoin(gdf, hex_gdf, unique_id='hex'+str(r))

    # within_hex = gpd.sjoin(hex_gdf, gdf, op='within')
    # # overlap the rest with the boundary to get hexagons on boundary
    # not_within = hex_gdf[~hex_gdf['hex'+str(r)].isin(within_hex['hex'+str(r)])]
    # intersect_boundary_hex = gpd.sjoin(not_within, gdf)
    # # within + overlap hexagons => hexagons covering the whole region refined to region boundary
    # result_gdf = hex_gdf[(hex_gdf['hex'+str(r)].isin(within_hex['hex'+str(r)]))|(hex_gdf['hex'+str(r)].isin(intersect_boundary_hex['hex'+str(r)]))]
    # print('Hex',str(r),'layer created.')

    return result_gdf

def refine_sjoin(boundary, gdf, unique_id):
    within_bounds = gpd.sjoin(gdf, boundary, op='within')
    not_within = gdf[~gdf[unique_id].isin(within_bounds[unique_id])]

    # overlap the rest with the boundary
    boundary_intersect = gpd.sjoin(not_within, boundary)

    # within + overlap hexagons => hexagons covering the whole region refined to region boundary
    result_gdf = gdf[(gdf[unique_id].isin(within_bounds[unique_id]))|(gdf[unique_id].isin(boundary_intersect[unique_id]))]
    return result_gdf

def hex_of_point(point, res):
    '''
    input: point geometry, resolution
    output: hexagons
    '''
    return h3.geo_to_h3(point.y,point.x,res)


def hex2poly(x):
    '''
    input: hex
    output: polygon geometry
    '''
    geom_boundary_coords = h3.h3_to_geo_boundary(x,geo_json = True)
    geom_shp = geometry.Polygon(geom_boundary_coords)
    
    return geom_shp

def get_bbox(shp):
    xmin, ymin, xmax, ymax = shp.total_bounds
    boundary = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])
    geoJson = {'type': 'Polygon',
     'coordinates': [[[ymin, xmin], [ymax, xmin], [ymax, xmax], [ymin, xmax]]] }
    # boundary = gpd.GeoSeries([boundary]).__geo_interface__
    return boundary, geoJson