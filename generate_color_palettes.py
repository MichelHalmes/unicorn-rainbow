import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import json

NB_VALUES = 360
COLOR_MAPS = [  'gist_earth', 'terrain', 'ocean', 'gist_stern',
                'brg', 'CMRmap', 'cubehelix',
                'gnuplot', 'gnuplot2', 'gist_ncar',
                'nipy_spectral', 'jet', 'rainbow',
                'gist_rainbow', 'hsv', 'flag', 'prism']


color_palettes = {}

for cmap_name in COLOR_MAPS:
    cmap = plt.get_cmap(cmap_name)
    norm = mpl.colors.Normalize(vmin=0, vmax=NB_VALUES-1)
    scalarMap = cm.ScalarMappable(norm=norm, cmap=cmap)
    def val_to_rgb(val):
        rgb = scalarMap.to_rgba(val)
        return [int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])]

    palette = map(val_to_rgb, range(NB_VALUES))
    color_palettes[cmap_name] = palette


with open('color_palettes.json', 'w') as fp:
    json.dump(color_palettes, fp)
