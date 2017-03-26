import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import colorsys

NB_VALUES = 255
COLOR_MAPS = [
    # ('gist_earth', 1),
    # ('terrain', 1),
    ('ocean', 1),
    # ('gist_stern', 1),
    ('brg', 1),
    # ('CMRmap', 1),
    # ('cubehelix', 1),
    ('gnuplot', 1),
    # ('gnuplot2', 1),
    # ('gist_ncar', 1),
    ('nipy_spectral', .99),
    ('jet', 1),
    # ('rainbow', 1),
    ('gist_rainbow', 1),
    ('hsv', 1),
    # ('flag', 1),
    # ('prism', 1),
]


color_palettes = {}

for cmap_name, scale in COLOR_MAPS:
    cmap = plt.get_cmap(cmap_name)
    norm = mpl.colors.Normalize(vmin=0, vmax=NB_VALUES-1)
    scalarMap = cm.ScalarMappable(norm=norm, cmap=cmap)
    def val_to_rgb(val):
        rgb = scalarMap.to_rgba(val*scale)
        return [int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])]
    color_palettes[cmap_name] = map(val_to_rgb, range(NB_VALUES))

def mich_rainbow(deg):
    rgb = colorsys.hsv_to_rgb((deg/360.0)**2, 1, 1)
    return tuple(int(255*c/sum(rgb)) for c in rgb)
color_palettes['mich_rainbow'] = map(mich_rainbow, range(NB_VALUES))

with open('./palettes/color_palettes.json', 'w') as fp:
    json.dump(color_palettes, fp)
