# Bug cause

Unaware of the ****kwargs** argument, I introduced a bug into my program by passing a list instead of a dictionary while instantiating **NearEarthObject** and **OrbitPath** objects in the **database.py** script.

# Code snippet before fixing the bug
```
# List version of the row
attributes_list = list(row.items())
NEO = NearEarthObject(**attributes_list)
orbit = OrbitPath(**attributes_list)
```

# Bug solution

* Read [this]() article about ****kwargs** and ***args**. 
* Converted the list into dict before passing it to the **NearEarthObject** and **OrbitPath** objects.  

# Code snippet after fixing the bug
```
# List version of the row
attributes_list = list(row.items())
# Dict version of the row
attributes_dict = dict(attributes_list)
NEO = NearEarthObject(**attributes_dict)
orbit = OrbitPath(**attributes_dict)
```
