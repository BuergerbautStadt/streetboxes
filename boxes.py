import json
import requests
import xml.etree.ElementTree as ET
import time

from pprint import pprint

def bbox_from_polygon(polygon):
  minLat, maxLat, minLon, maxLon = 90, 0, 180, 0

  # this margin is used to enlarge the bounding box in order to actually
  # catch the streets around the area in question
  margin = 0.001

  for point in polygon[0]:

    if point[0] < minLat:
      minLat = point[0] - margin

    if point[0] > maxLat:
      maxLat = point[0] + margin

    if point[1] < minLon:
      minLon = point[1] - margin

    if point[1] > maxLon:
      maxLon = point[1] + margin

  bbox = { "box": [minLat, minLon, maxLat, maxLon], "center": [(minLat + maxLat) / 2, (minLon + maxLon) / 2] }

  return bbox

def extract_ways(box):
  url = "http://api.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % tuple(box["box"])
  r = requests.get(url)

  ways = []
  
  data = ET.fromstring(r.text)

  it = data.getiterator("way")
  for el in data.getiterator("way"):
    highwayCheck = el.find(".//tag[@k='highway']")
    if highwayCheck is None:
      continue

    name = el.find(".//tag[@k='name']")

    if (name is not None) and (name.get("v") not in ways):
      ways.append(name.get("v"))          

  return ways

def process_feature(feature):
  geometry = feature["geometry"]

  geoinfo = {}
  geoinfo["id"] = feature["properties"]["spatial_alias"]

  bboxes = []

  if geometry["type"] == "MultiPolygon":
    for polygon in geometry["coordinates"]:
      bbox = bbox_from_polygon(polygon)
      bboxes.append(bbox)

  else:
    bbox = bbox_from_polygon(geometry["coordinates"])
    bboxes.append(bbox)

  geoinfo["ways"] = []

  for box in bboxes:
    geoinfo["ways"].append(extract_ways(box))

  print("processed \"%s\" - (%d of %d)" % (geoinfo["id"], len(geoinfos), len(json_data["features"])))

  return geoinfo

# Process all features in 'plan.geojson' for now

fd = open('plan.geojson')
json_data = json.load(fd)
fd.close()

geoinfos = []

i = 2
for feature in json_data["features"]:
  geoinfos.append(process_feature(feature))
  #time.sleep(4)
  i -= 1
  if i == 0:
    break

fd = open('geoinfos.json', 'w')
json.dump(geoinfos, fd, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
fd.close()
