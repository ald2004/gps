# GPS输入: ['$GNGGA', '102350.000', '3100.75202', 'N', '12100.37996', 'E', '1', '22', '0.6', '31.3', 'M', '0.0', 'M', '', '*49\r\n']
# /usr/bin/python3
# -*- coding: utf-8 -*

import os,sys,uuid,glob,fire,math

def wgs_gcj(lat, lon):
    pi = 3.1415926535897932384626
    a = 6378245.0
    ee = 0.00669342162296594323

    def transform_lat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
        return ret

    def transform_lon(x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
        return ret

    d_lat = transform_lat(lon - 105.0, lat - 35.0)
    d_lon = transform_lon(lon - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * pi
    magic = math.sin(rad_lat)
    magic = 1 - ee * magic * magic
    sqrt_magic = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * pi)
    d_lon = (d_lon * 180.0) / (a / sqrt_magic * math.cos(rad_lat) * pi)
    mg_lat = lat + d_lat
    mg_lon = lon + d_lon
    return mg_lat, mg_lon

# info = ['$GNGGA', '102350.000', '3100.75202', 'N', '12100.37996', 'E', '1', '22', '0.6', '31.3', 'M', '0.0', 'M', '', '*49\r\n']
# info = ['$GNGGA', '', '', '', '', '', '0', '00', '25.5', '', '', '', '', '', '*64\n']
def parse(info):
    latitude_wgs84 = int(float(info[2]) / 100) + (float(info[2]) / 100 - int(float(info[2]) / 100)) * 100 / 60
    longitude_wgs84 = int(float(info[4]) / 100) + (float(info[4]) / 100 - int(float(info[4]) / 100)) * 100 / 60
    latitude_gcj02, longitude_gcj02 = wgs_gcj(latitude_wgs84, longitude_wgs84)
    print("纬度：", latitude_gcj02, "经度：", longitude_gcj02)
    print(f"{str(longitude_gcj02)}, {str(latitude_gcj02)}")
    print("卫星数：", info[7])
def testgps():
    with open('session.log','r') as fid:
        for line in fid.readlines():
            # print(line[1:6])
            if(line[1:6]=="GNGGA"):
                # parse(line.split(","))
                print(line.split(","))
if __name__ =="__main__":
    fire.Fire()

