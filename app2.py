# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 20:16:12 2019

@author: vinic
"""

import folium 
import pandas as pd


data = pd.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"
    
    
def style(x):
    if x['properties']['POP2005'] < 10000000:
        return "green"
    elif 10000000 <= x['properties']['POP2005'] < 20000000:
        return "orange"
    else:
        return "red"

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

fgv = folium.FeatureGroup(name="Volcanos")
fgp = folium.FeatureGroup(name="Population")
map = folium.Map(location = [lat[0],lon[0]], zoom_start=7)


for lt, ln, el, name in zip(lat, lon, elev, name): 
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location = [lt, ln], popup = folium.Popup(iframe), radius=6, fill_color=color_producer(el), fill = True,
                                     color = 'grey', fill_opacity=0.7))
    
    
fgp.add_child(folium.GeoJson(data = open("world.json", 'r', encoding='utf-8-sig').read(), 
                            style_function = lambda  x: {"fillColor": style(x)}))
    

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())


map.save("firstMap.html")
