-----
popcenter-distance
-----


The US Census computes population centers based on census data. This data is
available by state as well as by county, and a few other options that probably
only make sense to census workers. This project is to make it easy to compute
the geographic distance between population centers. The US Census data lists
population centers in lat/long coordinates.

There are many algorithms for converting (several of which can be read about
at [Movable Type Scripts](http://www.movable-type.co.uk/scripts/latlong.html)).
Some treat the earth as flat, which, over small distances is decently accurate 
and fast. Some treat the earth as a true sphere, which is more accurate than
flat over long distances (e.g.
[Haversine](https://en.wikipedia.org/wiki/Haversine_formula)). Some adjust for
the fact that the earth is an oblate spheroid, using an approximation for
the radius at the equator as well as the poles 
([as described in this SO answer](https://stackoverflow.com/a/37870363/2364215)).
While it is my aim to implement several algorithms, the only one implemented so
far is the oblate spheroid one, which I am attributing to Keerthana
Gopalakrishnan, as did the poster of this
[SO answer](https://stackoverflow.com/a/49916544/2364215) to the question
[Calculate distance between two latitude-longitude points? (Haversine formula)](https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula)


Other resources for possible algorithms to implement:

* https://github.com/mapado/haversine/blob/master/haversine/haversine.py
* http://www.movable-type.co.uk/scripts/latlong.html
* https://en.wikipedia.org/wiki/Vincenty%27s_formulae
* https://en.wikipedia.org/wiki/Geographical_distance
* https://cs.nyu.edu/visual/home/proj/tiger/gisfaq.html

Data Sources:

* Census Data Mean Population Center by State:
    http://www2.census.gov/geo/docs/reference/cenpop2010/CenPop2010_Mean_ST.txt
* Census Data Mean Population Center by County:
    https://www2.census.gov/geo/docs/reference/cenpop2010/county/CenPop2010_Mean_CO.txt

Other Future Work
-------
* With the census data only changing once every 10 years, the distances could be
computed into a lookup table, and that table made available in projects.
* Smart switching could be implemented, based on whether speed or accuracy is
desired, or if the distance is determined to be long, and thus a more accurate
model would be desired.
