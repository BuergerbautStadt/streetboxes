# streetboxes

`boxes.py` demonstrates how to extract street names from geojson shapes. To catch all corresponding streets, the area of each bounding box is slightly increased and then [openstreetmap's](http://openstreetmap.org) data is queried and checked for the `k=highway` tag. 
