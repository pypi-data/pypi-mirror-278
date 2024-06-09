# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plot_map']

package_data = \
{'': ['*']}

install_requires = \
['Cartopy>=0.21.1,<0.22.0',
 'matplotlib>=3.5.2,<4.0.0',
 'scipy>=1.8.1,<2.0.0',
 'shapely>=2.0.1,<3.0.0',
 'xcsv-plot>=0,<1']

entry_points = \
{'console_scripts': ['xcsv_plot_map = xcsv.plot_map.__main__:main']}

setup_kwargs = {
    'name': 'xcsv-plot-map',
    'version': '0.4.2',
    'description': 'Subpackage to plot and locate on a map, data from extended CSV (XCSV) files',
    'long_description': "# xcsv-plot-map\n\nxcsv-plot-map is a subpackage of [xcsv](https://github.com/paul-breen/xcsv).  It's main purpose is to provide a simple CLI for plotting extended CSV (XCSV) files, and locating the data on a map, given an extended header section with geographical coordinates.  These will typically detail where the data were acquired.  It inherits from the [xcsv-plot](https://pypi.org/project/xcsv-plot) subpackage of xcsv.\n\n## Install\n\nThe package can be installed from PyPI:\n\n```bash\n$ pip install xcsv-plot-map\n```\n\n## Notes on installing Cartopy\n\nxcsv-plot-map has a dependency on Cartopy.  In turn, Cartopy requires the Proj library.  If you find that you can't install Cartopy because the version of the Proj library on your system is too old, then you can build a local version of the Proj library.  This should be a fairly straightforward build.  You may then find that the Cartopy package installs OK, but that you get the following segfault at runtime when trying to use xcsv-plot-map:\n\n```bash\nfree(): invalid size\nAborted (core dumped)\n```\n\nThis is a known issue.  A suggested fix for this is to reinstall the Python `shapely` package.  First remove it:\n\n```bash\n$ pip uninstall shapely\n```\n\nand then reinstall it with specific `pip` options:\n\n```bash\n$ pip install --no-binary :all: shapely\n```\n\nThis may take a while, but should resolve the segfault issue and everything should work.\n\n## Using the package\n\nAn XCSV file with an [ACDD-compliant](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) extended header section, including geographical coordinates in `longitude` and `latitude` header items, and well-annotated column-headers, already provides much of the text needed to make an informative plot and map, so we can just plot the XCSV file directly from the command line.  This is the purpose of the `xcsv-plot-map` subpackage.  For example:\n\n```bash\n$ python3 -m xcsv.plot_map -x 0 -y 1 example.csv\n```\n\nNote here that we're calling `xcsv-plot-map` as a *module main*.  As a convenience, this invocation is wrapped as a console script when installing the package, hence the following invocation is equivalent:\n\n```bash\n$ xcsv_plot_map -x 0 -y 1 example.csv\n```\n\nIn addition to using the CLI, the package can be used as a Python library.  The main class is `Plot`.  This is inherited from the `xcsv-plot.Plot` class, with some overridden methods.  The class provides methods to plot a given list of datasets (XCSV objects), and locate them on a map:\n\n```python\nimport xcsv\nimport xcsv.plot_map as xpm\n\nfilenames = ['example1.csv','example2.csv','example3.csv']\ndatasets = []\n\nfor filename in filenames:\n    with xcsv.File(filename) as f:\n        datasets.append(f.read())\n\nplotter = xpm.Plot()\nplotter.plot_datasets(datasets, xidx=0, yidx=1)\n```\n\n## Command line usage\n\nCalling the script with the `--help` option will show the following usage:\n\n```bash\n$ python -m xcsv.plot_map --help\nusage: xcsv_plot_map [-h] [-x XIDX | -X XCOL] [-y YIDX | -Y YCOL]\n                     [--x-label XLABEL] [--y-label YLABEL] [--invert-x-axis]\n                     [--invert-y-axis] [--title TITLE] [--caption CAPTION]\n                     [--label-key LABEL_KEY] [-s FIGSIZE FIGSIZE]\n                     [-p PROJECTION] [-m] [-b BG_IMG_PATH] [-o OUT_FILE]\n                     [-P PLOT_OPTS] [-S] [-V]\n                     in_file [in_file ...]\n\nplot the given XCSV files and locate the data on a map\n\npositional arguments:\n  in_file               input XCSV file(s)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -x XIDX, --x-idx XIDX\n                        column index (zero-based) containing values for the\n                        x-axis\n  -X XCOL, --x-column XCOL\n                        column label containing values for the x-axis\n  -y YIDX, --y-idx YIDX\n                        column index (zero-based) containing values for the\n                        y-axis\n  -Y YCOL, --y-column YCOL\n                        column label containing values for the y-axis\n  --x-label XLABEL      text to be used for the plot x-axis label\n  --y-label YLABEL      text to be used for the plot y-axis label\n  --invert-x-axis       invert the x-axis\n  --invert-y-axis       invert the y-axis\n  --title TITLE         text to be used for the plot title\n  --caption CAPTION     text to be used for the plot caption\n  --label-key LABEL_KEY\n                        key of the header item in the extended header section\n                        whose value will be used for the plot legend label\n  -s FIGSIZE FIGSIZE, --figsize FIGSIZE FIGSIZE\n                        size of the figure (width height)\n  -p PROJECTION, --map-projection PROJECTION\n                        projection to use for displaying the site coordinates\n                        on the map (one of the CRS classes provided by\n                        Cartopy)\n  -m, --plot-on-map     instead of a plot alongside a site map, show just a\n                        map and plot the coordinate data directly on the map\n  -b BG_IMG_PATH, --background-image BG_IMG_PATH\n                        path to an image to show in the background of the plot\n  -o OUT_FILE, --out-file OUT_FILE\n                        output plot file\n  -P PLOT_OPTS, --plot-options PLOT_OPTS\n                        options for the plot, specified as a simple JSON\n                        object\n  -S, --scatter-plot    set plot options (see -P) to produce a scatter plot\n  -V, --version         show program's version number and exit\n\nExamples\n\nGiven an XCSV file with an ACDD-compliant extended header section, including geographical coordinates in longitude and latitude, and a single column (at column 0) of data values:\n\n# id: 1\n# title: The title\n# latitude: -73.86 (degree_north)\n# longitude: -65.46 (degree_east)\ndepth (m)\n0.575\n1.125\n2.225\n\nThen the following invocation will plot the only column on the y-axis, with the x-axis the indices of the data points, and will locate the coordinates on a map:\n\npython3 -m xcsv.plot_map input.csv\n\nIf the file also contains a suitable variable for the x-axis:\n\n# id: 1\n# title: The title\n# latitude: -73.86 (degree_north)\n# longitude: -65.46 (degree_east)\ntime (year) [a],depth (m)\n2012,0.575\n2011,1.125\n2010,2.225\n\nthen the columns to be used for the x- and y-axes can be specified thus:\n\npython3 -m xcsv.plot_map -x 0 -y 1 input.csv\n```\n\n",
    'author': 'Paul Breen',
    'author_email': 'pbree@bas.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/paul-breen/xcsv-plot-map',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
