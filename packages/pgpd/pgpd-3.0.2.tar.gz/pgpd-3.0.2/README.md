<img src="https://github.com/0phoff/pygeos-pd/blob/master/docs/source/_static/logo.svg?raw=true" alt="Logo" width="100%">  

[![Version][version-badge]][release-url]
[![CI][ci-badge]][ci-url]
[![Documentation][doc-badge]][documentation-url]
<a href="https://ko-fi.com/D1D31LPHE"><img alt="Ko-Fi" src="https://www.ko-fi.com/img/githubbutton_sm.svg" height="20"></a>  

Small wrapper to use Shapely functions from pandas.  
The main use case is if you want to have geometries in your dataframe,
but you do not care about CRS at all and thus do not need all the extra features from GeoPandas.

## Install
This package is available on PyPi for installation.

```bash
pip install pgpd
```


## Example
Let's get started by first creating a dataframe with Shapely data.  
Note that we need to explicitly set the type of the Shapely columns to __"geos"__!

```python
>>> import pandas as pd
>>> import shapely
>>> import pgpd

>>> # Create a DataFrame
>>> df = pd.DataFrame({
...   'a': list('abcde'),
...   'poly': shapely.box(range(5), 0, range(10,15), 10),
...   'pt': shapely.points(range(5), range(10,15))
... })
>>> df = df.astype({'poly':'geos', 'pt':'geos'})
>>> df
   a                                      poly            pt
0  a  POLYGON ((10 0, 10 10, 0 10, 0 0, 10 0))  POINT (0 10)
1  b  POLYGON ((11 0, 11 10, 1 10, 1 0, 11 0))  POINT (1 11)
2  c  POLYGON ((12 0, 12 10, 2 10, 2 0, 12 0))  POINT (2 12)
3  d  POLYGON ((13 0, 13 10, 3 10, 3 0, 13 0))  POINT (3 13)
4  e  POLYGON ((14 0, 14 10, 4 10, 4 0, 14 0))  POINT (4 14)
```

### Series
We can access shapely functionality through the "geos" accessor namespace.  

```python
>>> df.poly.geos.length()
0    40.0
1    40.0
2    40.0
3    40.0
4    40.0
Name: length, dtype: float64

>>> df.pt.geos.total_bounds()
xmin     0.0
ymin    10.0
xmax     4.0
ymax    14.0
Name: total_bounds, dtype: float64

>>> df.poly.geos.clip_by_rect(0, 0, 5, 10)
0    POLYGON ((0 0, 0 10, 5 10, 5 0, 0 0))
1    POLYGON ((1 0, 1 10, 5 10, 5 0, 1 0))
2    POLYGON ((2 0, 2 10, 5 10, 5 0, 2 0))
3    POLYGON ((3 0, 3 10, 5 10, 5 0, 3 0))
4    POLYGON ((4 0, 4 10, 5 10, 5 0, 4 0))
Name: clip_by_rect, dtype: geos
```

Some functions return more values per row, so we convert them to DataFrames:

```python
>>> df.poly.geos.bounds()
   xmin  ymin  xmax  ymax
0   0.0   0.0  10.0  10.0
1   1.0   0.0  11.0  10.0
2   2.0   0.0  12.0  10.0
3   3.0   0.0  13.0  10.0
4   4.0   0.0  14.0  10.0
```

There are some functions that return a variable number of items per original object.
For these functions, the index of the returned Series/DataFrame will point to the original object index.

```python
>>> points = pd.Series(
...   shapely.multipoints(
...     [[0,0], [1,1], [2,2], [0,1],[2,3], [10,20],[30,40],[40,50],[50,60]],
...     indices=[0,0,0,1,1,2,2,2,2],
...   ),
...   dtype='geos',
... )
>>> points
0                 MULTIPOINT (0 0, 1 1, 2 2)
1                      MULTIPOINT (0 1, 2 3)
2    MULTIPOINT (10 20, 30 40, 40 50, 50 60)
dtype: geos

>>> points.geos.get_parts()
0      POINT (0 0)
0      POINT (1 1)
0      POINT (2 2)
1      POINT (0 1)
1      POINT (2 3)
2    POINT (10 20)
2    POINT (30 40)
2    POINT (40 50)
2    POINT (50 60)
Name: get_parts, dtype: geos

>>> points.geos.get_coordinates_2d()
      x     y   z
0   0.0   0.0 NaN
0   1.0   1.0 NaN
0   2.0   2.0 NaN
1   0.0   1.0 NaN
1   2.0   3.0 NaN
2  10.0  20.0 NaN
2  30.0  40.0 NaN
2  40.0  50.0 NaN
2  50.0  60.0 NaN
```

Finally, Shapely also has some binary functions, which work on 2 different sets of geometries.  
These functions are also made available on Series, but work slightly differently.
We added a `manner` argument, which can be one of 3 different values: _keep_, _align_, _expand_.
This argument dictates how the 2 sets of geometries are transformed before running the binary function:

- _keep_: Function is run on the input as is.
- _align_: Align both sets with each other, according to their index (only works when `other` is a Series).
- _expand_: Expand both sets to a 2D array and compare each geometry of set A with each geometry of set B (returns a 2D array of dimension _<len(A), len(B)>_).

```python
>>> # KEEP: Just runs the `contains` function on the "poly" column data and the given Point
>>> df.poly.geos.contains(shapely.from_wkt("Point (11 5)"), manner='keep')
0    False
1    False
2     True
3     True
4     True
Name: contains, dtype: bool

>>> # ALIGN: We only pass 3 points, but tell the function to align the data according to the index
>>> df.poly.geos.distance(df.pt[1:4], manner='align')
0    NaN
1    1.0
2    2.0
3    3.0
4    NaN
Name: distance, dtype: float64

>>> # EXPAND: Compare each polygon with each point (returns numpy.ndarray <5,3> in this case)
>>> df.poly.geos.distance(df.pt[1:4], manner='expand')
array([[1.        , 2.        , 3.        ],
       [1.        , 2.        , 3.        ],
       [1.41421356, 2.        , 3.        ],
       [2.23606798, 2.23606798, 3.        ],
       [3.16227766, 2.82842712, 3.16227766]])
```

One last difference is that you can omit the `other` set of geometries.
The method will then automatically choose the _expand_ mode and use the `self` data twice.

```python
>>> # Compute all possible intersection areas of the geometries in the "poly" column
>>> shapely.area(df.poly.geos.intersection())
array([[100.,  90.,  80.,  70.,  60.],
       [ 90., 100.,  90.,  80.,  70.],
       [ 80.,  90., 100.,  90.,  80.],
       [ 70.,  80.,  90., 100.,  90.],
       [ 60.,  70.,  80.,  90., 100.]])
```


### DataFrame
While all Shapely functions are available on Series, some are made available on the DataFrame as well.  
The functions that are available on DataFrames are those that have a 1-to-1 mapping (create one output for each geometry in the column),
or those that have a fixed number of outputs for the entire geos column.

```python
>>> # Fixed number of outputs (ic. xmin,ymin,xmax,ymax)
>>> df.geos.total_bounds()
      poly    pt
xmin   0.0   0.0
ymin   0.0  10.0
xmax  14.0   4.0
ymax  10.0  14.0

>>> # For every Shapely function that has a 1-to-1 relation,
>>> # the DataFrame variant allows inplace modification
>>> df.geos.transform(lambda coord: coord*2, inplace=True)
>>> df
   a                                      poly            pt
0  a  POLYGON ((20 0, 20 20, 0 20, 0 0, 20 0))  POINT (0 20)
1  b  POLYGON ((22 0, 22 20, 2 20, 2 0, 22 0))  POINT (2 22)
2  c  POLYGON ((24 0, 24 20, 4 20, 4 0, 24 0))  POINT (4 24)
3  d  POLYGON ((26 0, 26 20, 6 20, 6 0, 26 0))  POINT (6 26)
4  e  POLYGON ((28 0, 28 20, 8 20, 8 0, 28 0))  POINT (8 28)
```


## GeoPandas
The main use case for this library is not to depend on GeoPandas and all of its dependencies.
However -if you need to- this library provides methods to convert from and to GeoPandas.

### Series
```python
>>> gs = df.pt.geos.to_geopandas(crs='WGS84')
>>> gs
0    POINT (0.00000 20.00000)
1    POINT (2.00000 22.00000)
2    POINT (4.00000 24.00000)
3    POINT (6.00000 26.00000)
4    POINT (8.00000 28.00000)
Name: pt, dtype: geometry

>>> s2 = gs.geos.to_geos()
>>> s2
0    POINT (0 20)
1    POINT (2 22)
2    POINT (4 24)
3    POINT (6 26)
4    POINT (8 28)
Name: pt, dtype: geos
```

### DataFrame
GeoPandas only allows for one `geometry` column, so any other column is left as our own `geos`dtype.

```python
>>> gdf = df.geos.to_geopandas(geometry='poly', crs='WGS84')
>>> gdf
   a                                               poly            pt
0  a  POLYGON ((20.00000 0.00000, 20.00000 20.00000,...  POINT (0 20)
1  b  POLYGON ((22.00000 0.00000, 22.00000 20.00000,...  POINT (2 22)
2  c  POLYGON ((24.00000 0.00000, 24.00000 20.00000,...  POINT (4 24)
3  d  POLYGON ((26.00000 0.00000, 26.00000 20.00000,...  POINT (6 26)
4  e  POLYGON ((28.00000 0.00000, 28.00000 20.00000,...  POINT (8 28)
>>> gdf.dtypes
a         object
poly    geometry
pt          geos
dtype: object

>>> df2 = gdf.geos.to_geos()
>>> df2
   a                                      poly            pt
0  a  POLYGON ((20 0, 20 20, 0 20, 0 0, 20 0))  POINT (0 20)
1  b  POLYGON ((22 0, 22 20, 2 20, 2 0, 22 0))  POINT (2 22)
2  c  POLYGON ((24 0, 24 20, 4 20, 4 0, 24 0))  POINT (4 24)
3  d  POLYGON ((26 0, 26 20, 6 20, 6 0, 26 0))  POINT (6 26)
4  e  POLYGON ((28 0, 28 20, 8 20, 8 0, 28 0))  POINT (8 28)
>>> df2.dtypes
a       object
poly      geos
pt        geos
dtype: object
```


[version-badge]: https://img.shields.io/pypi/v/pgpd?label=version
[ci-badge]: https://github.com/0phoff/pgpd/actions/workflows/ci.yml/badge.svg?branch=master
[doc-badge]: https://img.shields.io/badge/-Documentation-9B59B6.svg
[release-url]: https://github.com/0phoff/pgpd/releases
[ci-url]: https://github.com/0phoff/pgpd/actions/workflows/ci.yml
[documentation-url]: https://0phoff.github.io/pgpd
