#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Test the GenImgProjTransformer capabilities.
# Author:   Frank Warmerdam <warmerdam@pobox.com>
#
###############################################################################
# Copyright (c) 2008, Frank Warmerdam <warmerdam@pobox.com>
# Copyright (c) 2008-2013, Even Rouault <even dot rouault at mines-paris dot org>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import sys

sys.path.append( '../pymod' )

import gdaltest
from osgeo import gdal
from osgeo import osr

###############################################################################
# Test simple Geotransform based transformer.

def transformer_1():

    ds = gdal.Open('data/byte.tif')
    tr = gdal.Transformer( ds, None, [] )

    (success,pnt) = tr.TransformPoint( 0, 20, 10 )

    if not success \
       or abs(pnt[0]- 441920) > 0.00000001 \
       or abs(pnt[1]-3750720) > 0.00000001 \
       or pnt[2] != 0.0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20) > 0.00000001 \
       or abs(pnt[1]-10) > 0.00000001 \
       or pnt[2] != 0.0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.' )
        return 'fail'

    return 'success' 

###############################################################################
# Test GCP based transformer with polynomials.

def transformer_2():

    ds = gdal.Open('data/gcps.vrt')
    tr = gdal.Transformer( ds, None, [ 'METHOD=GCP_POLYNOMIAL' ] )

    (success,pnt) = tr.TransformPoint( 0, 20, 10 )

    if not success \
       or abs(pnt[0]-441920) > 0.001 \
       or abs(pnt[1]-3750720) > 0.001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20) > 0.001 \
       or abs(pnt[1]-10) > 0.001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.' )
        return 'fail'

    return 'success' 

###############################################################################
# Test GCP based transformer with thin plate splines.

def transformer_3():

    ds = gdal.Open('data/gcps.vrt')
    tr = gdal.Transformer( ds, None, [ 'METHOD=GCP_TPS' ] )

    (success,pnt) = tr.TransformPoint( 0, 20, 10 )

    if not success \
       or abs(pnt[0]-441920) > 0.001 \
       or abs(pnt[1]-3750720) > 0.001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20) > 0.001 \
       or abs(pnt[1]-10) > 0.001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.' )
        return 'fail'

    return 'success' 

###############################################################################
# Test geolocation based transformer.

def transformer_4():

    ds = gdal.Open('data/sstgeo.vrt')
    tr = gdal.Transformer( ds, None, [ 'METHOD=GEOLOC_ARRAY' ] )

    (success,pnt) = tr.TransformPoint( 0, 20, 10 )

    if not success \
       or abs(pnt[0]+81.961341857910156) > 0.000001 \
       or abs(pnt[1]-29.612689971923828) > 0.000001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-19.554539744554866) > 0.001 \
       or abs(pnt[1]-9.1910760024906537) > 0.001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.' )
        return 'fail'

    return 'success' 

###############################################################################
# Test RPC based transformer.

def transformer_5():

    ds = gdal.Open('data/rpc.vrt')
    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC' ] )

    (success,pnt) = tr.TransformPoint( 0, 20.5, 10.5 )

    if not success \
       or abs(pnt[0]-125.64830100509131) > 0.000001 \
       or abs(pnt[1]-39.869433991997553) > 0.000001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20.5) > 0.001 \
       or abs(pnt[1]-10.5) > 0.001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.' )
        return 'fail'

    # Try with a different height.

    (success,pnt) = tr.TransformPoint( 0, 20.5, 10.5, 30 )

    if not success \
       or abs(pnt[0]-125.64828521533849) > 0.000001 \
       or abs(pnt[1]-39.869345204440144) > 0.000001 \
       or pnt[2] != 30:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.(2)' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20.5) > 0.001 \
       or abs(pnt[1]-10.5) > 0.001 \
       or pnt[2] != 30:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.(2)' )
        return 'fail'

    # Test RPC_HEIGHT option
    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT=30' ] )

    (success,pnt) = tr.TransformPoint( 0, 20.5, 10.5 )

    if not success \
       or abs(pnt[0]-125.64828521533849) > 0.000001 \
       or abs(pnt[1]-39.869345204440144) > 0.000001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.(3)' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20.5) > 0.001 \
       or abs(pnt[1]-10.5) > 0.001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.(3)' )
        return 'fail'

    # Test RPC_DEM and RPC_HEIGHT_SCALE options

    # (long,lat)=(125.64828521533849 39.869345204440144) -> (Easting,Northing)=(213324.662167036 4418634.47813677) in EPSG:32652
    ds_dem = gdal.GetDriverByName('GTiff').Create('/vsimem/dem.tif', 100, 100, 1)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(32652)
    ds_dem.SetProjection(sr.ExportToWkt())
    ds_dem.SetGeoTransform([213300,200,0,4418700,0,-200])
    ds_dem.GetRasterBand(1).Fill(15)
    ds_dem = None

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT_SCALE=2', 'RPC_DEM=/vsimem/dem.tif' ] )

    (success,pnt) = tr.TransformPoint( 0, 20.5, 10.5, 0 )

    if not success \
       or abs(pnt[0]-125.64828521533849) > 0.000001 \
       or abs(pnt[1]-39.869345204440144) > 0.000001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.(4)' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20.5) > 0.001 \
       or abs(pnt[1]-10.5) > 0.001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.(4)' )
        return 'fail'

    tr = None

    # Test RPC_DEMINTERPOLATION=cubic

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT_SCALE=2', 'RPC_DEM=/vsimem/dem.tif', 'RPC_DEMINTERPOLATION=cubic' ] )

    (success,pnt) = tr.TransformPoint( 0, 20.5, 10.5, 0 )

    if not success \
       or abs(pnt[0]-125.64828521533849) > 0.000001 \
       or abs(pnt[1]-39.869345204440144) > 0.000001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.(5)' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20.5) > 0.001 \
       or abs(pnt[1]-10.5) > 0.001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.(5)' )
        return 'fail'

    tr = None

    # Test RPC_DEMINTERPOLATION=near

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT_SCALE=2', 'RPC_DEM=/vsimem/dem.tif', 'RPC_DEMINTERPOLATION=near' ] )

    (success,pnt) = tr.TransformPoint( 0, 20.5, 10.5, 0 )

    if not success \
       or abs(pnt[0]-125.64828521503811) > 0.000001 \
       or abs(pnt[1]-39.869345204874911) > 0.000001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.(6)' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )

    if not success \
       or abs(pnt[0]-20.5) > 0.001 \
       or abs(pnt[1]-10.5) > 0.001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.(6)' )
        return 'fail'

    tr = None

    # Test outside DEM extent : default behaviour --> error
    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT_SCALE=2', 'RPC_DEM=/vsimem/dem.tif' ] )

    (success,pnt) = tr.TransformPoint( 0, 40000, 0, 0 )
    if success != 0:
        gdaltest.post_reason( 'fail' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, 125, 40, 0 )
    if success != 0:
        gdaltest.post_reason( 'fail' )
        return 'fail'

    tr = None

    # Test outside DEM extent with RPC_DEM_MISSING_VALUE=0
    ds_dem = gdal.GetDriverByName('GTiff').Create('/vsimem/dem.tif', 100, 100, 1)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(32652)
    ds_dem.SetProjection(sr.ExportToWkt())
    ds_dem.SetGeoTransform([213300,1,0,4418700,0,-1])
    ds_dem.GetRasterBand(1).Fill(15)
    ds_dem = None
    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT_SCALE=2', 'RPC_DEM=/vsimem/dem.tif', 'RPC_DEM_MISSING_VALUE=0' ] )

    (success,pnt) = tr.TransformPoint( 0, -99.5, 0.5, 0 )
    if not success \
       or abs(pnt[0]-125.64746155942839) > 0.000001 \
       or abs(pnt[1]-39.869506789921168) > 0.000001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    (success,pnt) = tr.TransformPoint( 1, pnt[0], pnt[1], pnt[2] )
    if not success \
       or abs(pnt[0]--99.5) > 0.001 \
       or abs(pnt[1]-0.5) > 0.001 :
        print(success, pnt)
        gdaltest.post_reason( 'got wrong reverse transform result.' )
        return 'fail'

    tr = None

    gdal.Unlink('/vsimem/dem.tif')

    return 'success' 


###############################################################################
# Test RPC convergence bug (bug # 5395)

def transformer_6():

    ds = gdal.Open('data/rpc_5395.vrt')
    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC' ] )

    (success,pnt) = tr.TransformPoint( 0, 0.5, 0.5 )

    if not success \
       or abs(pnt[0]-28.26163232) > 0.0001 \
       or abs(pnt[1]--27.79853245) > 0.0001 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    return 'success'

###############################################################################
# Test Transformer.TransformPoints

def transformer_7():

    ds = gdal.Open('data/byte.tif')
    tr = gdal.Transformer( ds, None, [] )

    (pnt, success) = tr.TransformPoints( 0, [(20, 10)] )

    if success[0] == 0 \
       or abs(pnt[0][0]- 441920) > 0.00000001 \
       or abs(pnt[0][1]-3750720) > 0.00000001 \
       or pnt[0][2] != 0.0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong forward transform result.' )
        return 'fail'

    return 'success' 

###############################################################################
# Test handling of nodata in RPC DEM (#5680)

def transformer_8():

    ds = gdal.Open('data/rpc.vrt')

    # (long,lat)=(125.64828521533849 39.869345204440144) -> (Easting,Northing)=(213324.662167036 4418634.47813677) in EPSG:32652
    ds_dem = gdal.GetDriverByName('GTiff').Create('/vsimem/dem.tif', 100, 100, 1, gdal.GDT_Int16)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(32652)
    ds_dem.SetProjection(sr.ExportToWkt())
    ds_dem.SetGeoTransform([213300,1,0,4418700,0,-1])
    ds_dem.GetRasterBand(1).SetNoDataValue(-32768)
    ds_dem.GetRasterBand(1).Fill(-32768)
    ds_dem = None

    for method in [ 'near', 'bilinear', 'cubic' ]:
        tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_DEM=/vsimem/dem.tif', 'RPC_DEMINTERPOLATION=%s' % method ] )

        (success,pnt) = tr.TransformPoint( 0, 20, 10, 0 )

        if success:
            print(success, pnt)
            gdaltest.post_reason( 'got wrong forward transform result.' )
            return 'fail'

        (success,pnt) = tr.TransformPoint( 1, 125.64828521533849, 39.869345204440144, 0 )

        if success:
            print(success, pnt)
            gdaltest.post_reason( 'got wrong reverse transform result.' )
            return 'fail'


    gdal.Unlink('/vsimem/dem.tif')

    return 'success' 

###############################################################################
# Test RPC DEM line optimization

def transformer_9():

    ds = gdal.Open('data/rpc.vrt')

    # (long,lat)=(125.64828521533849 39.869345204440144) -> (Easting,Northing)=(213324.662167036 4418634.47813677) in EPSG:32652
    ds_dem = gdal.GetDriverByName('GTiff').Create('/vsimem/dem.tif', 100, 100, 1, gdal.GDT_Byte)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)
    ds_dem.SetProjection(sr.ExportToWkt())
    ds_dem.SetGeoTransform([125.647968621436,1.2111052640051412e-05,0,39.869926216038,0,-8.6569068979969188e-06])
    import random
    random.seed(0)
    data = ''.join([ chr(40 + int(10 * random.random()) ) for i in range(100*100) ])
    ds_dem.GetRasterBand(1).WriteRaster(0, 0, 100, 100, data)
    ds_dem = None

    for method in [ 'near', 'bilinear', 'cubic' ]:
        tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_DEM=/vsimem/dem.tif', 'RPC_DEMINTERPOLATION=%s' % method ] )

        points = []
        for i in range(10):
            points.append((125.64828521533849, 39.869345204440144))
        (pnt, success) = tr.TransformPoints( 1, points )
        if not success[0]:
            gdaltest.post_reason( 'failure' )
            print(method)
            return 'fail'
        pnt_optimized = pnt[0]

        (success,pnt) = tr.TransformPoint( 1, 125.64828521533849, 39.869345204440144, 0 )
        if not success:
            gdaltest.post_reason( 'failure' )
            print(method)
            return 'fail'

        if pnt != pnt_optimized:
            gdaltest.post_reason( 'failure' )
            print(method)
            print(pnt)
            print(pnt_optimized)
            return 'fail'


    gdal.Unlink('/vsimem/dem.tif')

    return 'success'

###############################################################################
# Test RPC DEM transform from geoid height to ellipsoidal height

def transformer_10():

    sr = osr.SpatialReference()
    sr.ImportFromProj4('+proj=longlat +datum=WGS84 +geoidgrids=./tmp/fake.gtx +vunits=m +foo=bar +no_defs')
    if sr.ExportToProj4().find('foo=bar') >= 0:
        print('Missing proj.4')
        return 'skip'
    if sr.ExportToProj4().find('geoidgrids') < 0:
        print('Missing geoidgrids in %s. Outdated proj.4 version' % sr.ExportToProj4())
        return 'skip'

    # Create fake vertical shift grid
    out_ds = gdal.GetDriverByName('GTX').Create('tmp/fake.gtx',10,10,1,gdal.GDT_Float32)
    out_ds.SetGeoTransform([-180,36,0,90,0,-18])
    sr = osr.SpatialReference()
    sr.SetWellKnownGeogCS('WGS84')
    out_ds.SetProjection( sr.ExportToWkt() )
    out_ds.GetRasterBand(1).Fill(100)
    out_ds = None


    # Create a fake DEM
    ds_dem = gdal.GetDriverByName('GTiff').Create('/vsimem/dem.tif', 100, 100, 1, gdal.GDT_Byte)
    ds_dem.SetGeoTransform([125.647968621436,1.2111052640051412e-05,0,39.869926216038,0,-8.6569068979969188e-06])
    import random
    random.seed(0)
    data = ''.join([ chr(40 + int(10 * random.random()) ) for i in range(100*100) ])
    ds_dem.GetRasterBand(1).WriteRaster(0, 0, 100, 100, data)
    ds_dem = None

    ds_dem = gdal.Open('/vsimem/dem.tif')
    vrt_dem = gdal.GetDriverByName('VRT').CreateCopy('/vsimem/dem.vrt', ds_dem)
    ds_dem = None

    vrt_dem.SetProjection("""COMPD_CS["WGS 84 + my_height",
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]],
    VERT_CS["my_height",
        VERT_DATUM["my_height",0,
            EXTENSION["PROJ4_GRIDS","./tmp/fake.gtx"]],
        UNIT["metre",1,
            AUTHORITY["EPSG","9001"]],
        AXIS["Up",UP]]]""")
    vrt_dem = None

    ds = gdal.Open('data/rpc.vrt')

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_DEM=/vsimem/dem.vrt' ] )
    (success,pnt) = tr.TransformPoint( 1, 125.64828521533849, 39.869345204440144, 0 )

    if not success \
       or abs(pnt[0]-27.31476045569616) > 1e-5 \
       or abs(pnt[1]--53.328814757762302) > 1e-5 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong result.' )
        return 'fail'

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_DEM=/vsimem/dem.vrt', 'RPC_DEM_APPLY_VDATUM_SHIFT=FALSE' ] )
    (success,pnt) = tr.TransformPoint( 1, 125.64828521533849, 39.869345204440144, 0 )

    if not success \
       or abs(pnt[0]-21.445626206892484) > 1e-5 \
       or abs(pnt[1]-1.6460100520871492) > 1e-5 \
       or pnt[2] != 0:
        print(success, pnt)
        gdaltest.post_reason( 'got wrong result.' )
        return 'fail'

    gdal.GetDriverByName('GTX').Delete('tmp/fake.gtx')

    return 'success'

###############################################################################
# Test failed inverse RPC transform (#6162)

def transformer_11():

    ds = gdal.GetDriverByName('MEM').Create('', 6600, 4400)
    rpc = [
        'HEIGHT_OFF=1113.66579196784',
        'HEIGHT_SCALE=12.5010114250099',
        'LAT_OFF=38.8489906468112',
        'LAT_SCALE=-0.106514418771489',
        'LINE_DEN_COEFF=1 -0.000147949809772754 -0.000395269640841174 -1.15825619524758e-05 -0.001613476071797 5.20818134468044e-05 -2.87546958936308e-05 0.00139252754800089 0.00103224907048726 -5.0328770407996e-06 8.03722313022155e-06 0.000236052289425919 0.000208478107633822 -8.11629138727222e-06 0.000168941442517399 0.000392113144410504 3.13299811375497e-06 -1.50306451132806e-07 -1.96870155855449e-06 6.84425679628047e-07',
        'LINE_NUM_COEFF=0.00175958077249233 1.38380980570961 -1.10937056344449 -2.64222540811728e-05 0.00242330787142254 0.000193743606261641 -0.000149740797138056 0.000348558508286103 -8.44646294793856e-05 3.10853483444725e-05 6.94899990982205e-05 -0.00348125387930033 -0.00481553689971959 -7.80038440894703e-06 0.00410332555882184 0.00269594666059233 5.94355882183947e-06 -6.12499223746471e-05 -2.16490482825638e-05 -1.95059491792213e-06',
        'LINE_OFF=2199.80872158044',
        'LINE_SCALE=2202.03966104116',
        'LONG_OFF=77.3374268058015',
        'LONG_SCALE=0.139483831686384',
        'SAMP_DEN_COEFF=1 0.000220381598198686 -5.9113079248377e-05 -0.000123013508187712 -2.69270454504924e-05 3.85090208529735e-05 -5.05359221990966e-05 0.000207017095461956 0.000441092857548974 1.47302072491805e-05 9.4840973108768e-06 -0.000810344094204395 -0.000690502911945615 -1.07959445293954e-05 0.000801157109076503 0.000462754838815978 9.13256389877791e-06 7.49571761868177e-06 -5.00612460432453e-06 -2.25925949180435e-06',
        'SAMP_NUM_COEFF=-0.00209214639511201 -0.759096012299728 -0.903450038473527 5.43928095403867e-05 -0.000717672934172181 -0.000168790405106395 -0.00015564609496447 0.0013261576802665 -0.000398331147368139 -3.84712681506314e-05 2.70041394522796e-05 0.00254362585790201 0.00332988183285888 3.36326833370395e-05 0.00445687297094153 0.00290078876854111 3.59552237739047e-05 7.16492495304347e-05 -5.6782194494005e-05 2.32051448455541e-06',
        'SAMP_OFF=3300.39818049514',
        'SAMP_SCALE=3302.50400920438'
    ]
    ds.SetMetadata(rpc, 'RPC')

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT=4000' ] )
    (success,pnt) = tr.TransformPoint( 0, 0, 0, 0 )
    if success:
        print(pnt)
        return 'fail'

    # But this one should succeed
    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_HEIGHT=1150' ] )
    (success,pnt) = tr.TransformPoint( 0, 0, 0, 0 )
    if not success or abs(pnt[0] - 77.350939956024618) > 1e-7 or abs(pnt[1] - 38.739703990877814) > 1e-7:
        print(pnt)
        return 'fail'

    return 'success'

###############################################################################
# Test degenerate cases of TPS transformer

def transformer_12():

    ds = gdal.Open("""
    <VRTDataset rasterXSize="20" rasterYSize="20">
  <GCPList Projection="PROJCS[&quot;NAD27 / UTM zone 11N&quot;,GEOGCS[&quot;NAD27&quot;,DATUM[&quot;North_American_Datum_1927&quot;,SPHEROID[&quot;Clarke 1866&quot;,6378206.4,294.9786982139006,AUTHORITY[&quot;EPSG&quot;,&quot;7008&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6267&quot;]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;degree&quot;,0.0174532925199433],AUTHORITY[&quot;EPSG&quot;,&quot;4267&quot;]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,-117],PARAMETER[&quot;scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;26711&quot;]]">
    <GCP Id="" Pixel="0" Line="0" X="0" Y="0"/>
    <GCP Id="" Pixel="20" Line="0" X="20" Y="0"/>
    <GCP Id="" Pixel="0" Line="20" X="0" Y="20"/>
    <GCP Id="" Pixel="20" Line="20" X="20" Y="20"/>
    <GCP Id="" Pixel="0" Line="0" X="0" Y="0"/> <!-- duplicate entry -->
  </GCPList>
  <VRTRasterBand dataType="Byte" band="1">
    <ColorInterp>Gray</ColorInterp>
    <SimpleSource>
      <SourceFilename relativeToVRT="1">data/byte.tif</SourceFilename>
    </SimpleSource>
  </VRTRasterBand>
</VRTDataset>""")

    tr = gdal.Transformer( ds, None, [ 'METHOD=GCP_TPS' ] )
    if tr is None:
        gdaltest.post_reason('fail')
        return 'fail'

    ds = gdal.Open("""
    <VRTDataset rasterXSize="20" rasterYSize="20">
  <GCPList Projection="PROJCS[&quot;NAD27 / UTM zone 11N&quot;,GEOGCS[&quot;NAD27&quot;,DATUM[&quot;North_American_Datum_1927&quot;,SPHEROID[&quot;Clarke 1866&quot;,6378206.4,294.9786982139006,AUTHORITY[&quot;EPSG&quot;,&quot;7008&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6267&quot;]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;degree&quot;,0.0174532925199433],AUTHORITY[&quot;EPSG&quot;,&quot;4267&quot;]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,-117],PARAMETER[&quot;scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;26711&quot;]]">
    <GCP Id="" Pixel="0" Line="0" X="0" Y="0"/>
    <GCP Id="" Pixel="20" Line="0" X="20" Y="0"/>
    <GCP Id="" Pixel="0" Line="20" X="0" Y="20"/>
    <GCP Id="" Pixel="20" Line="20" X="20" Y="20"/>
    <GCP Id="" Pixel="0" Line="0" X="10" Y="10"/> <!-- same pixel,line -->
  </GCPList>
  <VRTRasterBand dataType="Byte" band="1">
    <ColorInterp>Gray</ColorInterp>
    <SimpleSource>
      <SourceFilename relativeToVRT="1">data/byte.tif</SourceFilename>
    </SimpleSource>
  </VRTRasterBand>
</VRTDataset>""")

    gdal.ErrorReset()
    with gdaltest.error_handler():
        tr = gdal.Transformer( ds, None, [ 'METHOD=GCP_TPS' ] )
    if gdal.GetLastErrorMsg() == '':
        gdaltest.post_reason('fail')
        return 'fail'

    ds = gdal.Open("""
    <VRTDataset rasterXSize="20" rasterYSize="20">
  <GCPList Projection="PROJCS[&quot;NAD27 / UTM zone 11N&quot;,GEOGCS[&quot;NAD27&quot;,DATUM[&quot;North_American_Datum_1927&quot;,SPHEROID[&quot;Clarke 1866&quot;,6378206.4,294.9786982139006,AUTHORITY[&quot;EPSG&quot;,&quot;7008&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6267&quot;]],PRIMEM[&quot;Greenwich&quot;,0],UNIT[&quot;degree&quot;,0.0174532925199433],AUTHORITY[&quot;EPSG&quot;,&quot;4267&quot;]],PROJECTION[&quot;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,-117],PARAMETER[&quot;scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;26711&quot;]]">
    <GCP Id="" Pixel="0" Line="0" X="0" Y="0"/>
    <GCP Id="" Pixel="20" Line="0" X="20" Y="0"/>
    <GCP Id="" Pixel="0" Line="20" X="0" Y="20"/>
    <GCP Id="" Pixel="20" Line="20" X="20" Y="20"/>
    <GCP Id="" Pixel="10" Line="10" X="20" Y="20"/> <!-- same X,Y -->
  </GCPList>
  <VRTRasterBand dataType="Byte" band="1">
    <ColorInterp>Gray</ColorInterp>
    <SimpleSource>
      <SourceFilename relativeToVRT="1">data/byte.tif</SourceFilename>
    </SimpleSource>
  </VRTRasterBand>
</VRTDataset>""")

    gdal.ErrorReset()
    with gdaltest.error_handler():
        tr = gdal.Transformer( ds, None, [ 'METHOD=GCP_TPS' ] )
    if gdal.GetLastErrorMsg() == '':
        gdaltest.post_reason('fail')
        return 'fail'

    return 'success'

###############################################################################
# Test inverse RPC transform at DEM edge (#6377)

def transformer_13():

    ds = gdal.GetDriverByName('MEM').Create('', 6600, 4400)
    rpc = [
        "HEIGHT_OFF=79.895358112544",
        "HEIGHT_SCALE=71.8479951519956",
        "LAT_OFF=39.1839631741725",
        "LAT_SCALE=-0.0993355184710674",
        "LINE_DEN_COEFF=1 8.18889582174233e-05 -0.000585027621468826 0.00141894885228522 -0.000585589558894143 2.26848970721562e-05 0.0004556101949561 -0.000807782279739336 -0.00042471862816941 -0.000569244978738162 1.48442578097541e-05 4.05131290592846e-05 2.84884306250279e-05 -5.18205692205965e-06 -6.313878273056e-07 1.53979251356426e-05 -7.18376115203249e-06 -6.17331013601745e-05 -7.21314704472095e-05 4.12297300238455e-06",
        "LINE_NUM_COEFF=-0.00742236358913794 -1.34432796989641 1.14742235955483 -0.00419813954264328 -0.00234215180175534 -0.00624463816085957 0.00678228413157904 0.0020362389986917 -0.00187712244349171 -8.03499198655765e-08 -0.00058862905508099 -0.00738644673656152 -0.00769111767189179 0.00076485216017804 0.00714033152180546 0.00597946564795612 -0.000632882594479344 -0.000167672086277102 0.00055226160003967 1.01784884515205e-06",
        "LINE_OFF=2199.71134437189",
        "LINE_SCALE=2197.27163235171",
        "LONG_OFF=-108.129788954851",
        "LONG_SCALE=0.135395601856691",
        "SAMP_DEN_COEFF=1 -0.000817668457487893 -0.00151956231901818 0.00117149108953055 0.000514723430775277 0.000357856819755055 0.000655430235824068 -0.00100177312999255 -0.000488725013873637 -0.000500795084518271 -3.31511569640467e-06 4.60608554396048e-05 4.71371559254521e-05 -3.47487113243818e-06 1.0984752288197e-05 1.6421626141648e-05 -6.2866141729034e-06 -6.32966599886646e-05 -7.06552514786235e-05 3.89288575686084e-06",
        "SAMP_NUM_COEFF=0.00547379112608157 0.807100297014362 0.845388298829057 0.01082483811889 -0.00320368761068744 0.00357867636379949 0.00459377712275926 -0.00324853865239341 -0.00218177030092682 2.99823054607907e-05 0.000946829367823539 0.00428577519330827 0.0045745876325088 -0.000396201144848935 0.00488772258958395 0.00435309486883759 -0.000402737234433541 0.000402935809278189 0.000642374929382851 -5.26793321752838e-06",
        "SAMP_OFF=3299.3111821927",
        "SAMP_SCALE=3297.19448149873"
    ]
    ds.SetMetadata(rpc, 'RPC')

    tr = gdal.Transformer( ds, None, [ 'METHOD=RPC', 'RPC_DEM=data/transformer_13_dem.tif' ] )
    (success,pnt) = tr.TransformPoint( 0, 6600, 24 )
    if not success or abs(pnt[0] - -108.00066006090175) > 1e-7 or abs(pnt[1] - 39.157694114659051) > 1e-7:
        print(pnt)
        return 'fail'


    return 'success'

gdaltest_list = [
    transformer_1,
    transformer_2,
    transformer_3,
    transformer_4,
    transformer_5,
    transformer_6,
    transformer_7,
    transformer_8,
    transformer_9,
    transformer_10,
    transformer_11,
    transformer_12,
    transformer_13
    ]

disabled_gdaltest_list = [
    transformer_9
]


if __name__ == '__main__':

    gdaltest.setup_run( 'transformer' )

    gdaltest.run_tests( gdaltest_list )

    gdaltest.summarize()

