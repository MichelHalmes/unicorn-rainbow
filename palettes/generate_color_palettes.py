import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import colorsys

NB_VALUES = 255
COLOR_MAPS = [
    # ('gist_earth', None),
    # ('terrain', None),
    ('ocean', None),
    # ('gist_stern', None),
    ('brg', None),
    # ('CMRmap', None),
    # ('cubehelix', None),
    ('gnuplot', (7, 0)),
    # ('gnuplot2', None),
    # ('gist_ncar', None),
    ('nipy_spectral', (10, 10)),
    ('jet', None),
    # ('rainbow', None),
    ('gist_rainbow', None),
    ('hsv', None),
    # ('flag', None),
    # ('prism', None),
]


color_palettes = {}

for cmap_name, truncate in COLOR_MAPS:
    cmap = plt.get_cmap(cmap_name)
    norm = mpl.colors.Normalize(vmin=0, vmax=NB_VALUES-1)
    scalarMap = cm.ScalarMappable(norm=norm, cmap=cmap)
    def val_to_rgb(val):
        rgb = scalarMap.to_rgba(val)
        return [int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])]
    palette = map(val_to_rgb, range(NB_VALUES))
    if truncate:
        palette = palette[truncate[0]: -(truncate[1]+1)]
    color_palettes[cmap_name] = palette

def mich_rainbow(deg):
    rgb = colorsys.hsv_to_rgb((1.*deg/NB_VALUES)**2, 1, 1)
    return tuple(int(255*c/sum(rgb)) for c in rgb)
color_palettes['mich_rainbow'] = map(mich_rainbow, range(NB_VALUES))

print color_palettes['nipy_spectral']


with open('./palettes/color_palettes.json', 'w') as fp:
    json.dump(color_palettes, fp)
