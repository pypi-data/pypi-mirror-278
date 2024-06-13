import numpy as np
import os
import sys
import argparse
import emcee
import corner
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
matplotlib.rcParams['interactive'] == True
#import PyQt6
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


sKy_colors = {'light blue':'#63B8FF', 'blue':'#4876FF', 'very dark blue':'#27408B', 
'blue grey':'#C6E2FF', 'dim cyan':'#98F5FF', 'cyan':'#00FFFF','red':'#FF4040', 
'mute red':'#EE6363', 'dark mute red':'#CD5555', 'dark red':'#CD2626', 'green':'#00FF7F', 
'honest green':'#008B45', 'dark green':'#008B45', 'grey':'#8B8989', 'dark grey':'#666666', 
'orange':'#FF9912', 'purple':'#8E388E', 'magenta':'#FF00FF', 'purple pink':'#FF83FA', 
'dark purple pink':'#BF3EFF', 'bright brown':'#8B5A00', 'dull brown':'#8B4726', 'mute brown':'#BC8F8F'}

color_schemes = {
"elsa":[sKy_colors["blue"], sKy_colors["blue grey"], 
sKy_colors["dark purple pink"], sKy_colors["cyan"], sKy_colors["light blue"], 
sKy_colors["magenta"], sKy_colors["grey"]],

"simplex":[sKy_colors['orange'], sKy_colors['grey'], sKy_colors['mute brown'], sKy_colors['blue grey']],

"autumn": [sKy_colors['grey'], sKy_colors['mute red'], sKy_colors['orange'], sKy_colors['dark red']],

"2145": [sKy_colors['dark purple pink'], sKy_colors['light blue'], sKy_colors['purple pink'],  sKy_colors['blue'],
 sKy_colors['magenta'],  sKy_colors['very dark blue']],

"ocean": [sKy_colors['cyan'], sKy_colors['blue grey'], 
sKy_colors['light blue'], sKy_colors['blue'], sKy_colors['very dark blue']],

"red_blue": [sKy_colors['dark red'], sKy_colors['mute red'], 
sKy_colors['orange'], sKy_colors['very dark blue'], sKy_colors['blue'], sKy_colors['light blue']],

"rainforest_flower":[sKy_colors['honest green'], sKy_colors['grey'], 
sKy_colors['purple'], sKy_colors['magenta'], sKy_colors['purple pink'], sKy_colors['dark purple pink']],

"childhood":[sKy_colors['dark purple pink'], sKy_colors['orange'], sKy_colors['magenta'], 
 sKy_colors['green'], sKy_colors['blue'], sKy_colors['red'], sKy_colors['cyan']],

"chill": [sKy_colors['light blue'], sKy_colors['blue grey'], sKy_colors['mute red'], 
sKy_colors['grey'], sKy_colors['purple pink'], 
sKy_colors['mute brown']],

"icecream": ['black', 'pink', sKy_colors['grey'],  sKy_colors['purple pink']]

}

def get_colors(i, scheme = None):
    return sKy_color_list(i, scheme)

def sKy_color_list(i, scheme = None):
    '''inputs: i-integer number of colors to generate, scheme-name of color scheme to choose colors from
       outputs: color_list-list of colors generated from sKy_colors dictionary with length i
       This function generates a list of i colors that can be used in a color map. It doesn't 
       do anything super intelligent. It just picks i random colors from the dictionary. Scheme allows you to 
       specify if you want the colors to come from a color scheme that exists. It will pick the first i colors 
       from the specified color scheme, if the scheme exists. If i is larger than the number of colors in
       the scheme, more colors will be chosen from the rest of the set of colors
    '''

    import random
    tor = None
    if scheme is None or scheme not in color_schemes.keys():
        idx_list = np.asarray(random.sample(range(len(sKy_colors.keys())), i))
        tor = [sKy_colors_list[i] for i in idx_list]
    else:

        tor = [color_schemes[scheme][j] for j in range(min([i, len(color_schemes[scheme])]))]
        if len(tor) < i:
            idx_list = np.asarray(random.sample(range(len(sKy_colors.keys())), i-len(tor)))
            for k in idx_list:
                tor.append(sKy_colors_list[k])

    return tor

def get_pretty_plot():
    W = 12
    H = 8
    fig, ax = plt.subplots(figsize=(W, H))

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    plt.tick_params(
        which='major',
        bottom='on',
        top='on',
        left='on',
        right='on',
        direction='in',
        length=25)
    plt.tick_params(
        which='minor',
        bottom='on',
        top='on',
        left='on',
        right='on',
        direction='in',
        length=10)
    #matplotlib.rcParams["font.family"] = 'serif'
    #matplotlib.rc('axes', unicode_minus=False)
    #matplotlib.rcParams['mathtext.fontset'] = 'custom'
    #matplotlib.rcParams['mathtext.rm'] = 'serif'
    #matplotlib.rcParams['mathtext.it'] = 'serif'
    #matplotlib.rcParams['mathtext.bf'] = 'serif'
    plt.xticks(fontsize=1.5*W)
    plt.yticks(fontsize=1.5*W)
    weight = 'normal'
    

    return plt

def make_axis(ax):
  ax.xaxis.set_minor_locator(AutoMinorLocator())
  ax.yaxis.set_minor_locator(AutoMinorLocator())

  ax.tick_params(
    which='major',
    bottom='on',
    top='on',
    left='on',
    right='on',
    direction='in',
    labelsize = 25,
    length=25)
  ax.tick_params(
      which='minor',
      bottom='on',
      top='on',
      left='on',
      right='on',
      direction='in',
      labelsize = 15,
      length=10)

  return ax
  
import random

def write_to_file(file_loc, data_out, separator = ' ', headers=None, append=False):
    '''inputs: file_loc-location to which to write to, data_to_write-this is a 2d array that will be written to a file
       outputs: none
       This function writes a 2d array to a file'''
       
    if not append:
        out = open(file_loc ,'w')
    else:
        out = open(file_loc ,'a+')
    
    if type(data_out) is str:
        out.write(data_out)
        
    else:
        for i  in range(len(data_out)):
            if isinstance(data_out[i], float) or type(data_out[i]) is str:
                out.write(str(data_out[i])+separator)
            else:
                for j in range(len(data_out[i])):
                    out.write(str(data_out[i][j])+separator)
                
            out.write("\n")
    out.close()