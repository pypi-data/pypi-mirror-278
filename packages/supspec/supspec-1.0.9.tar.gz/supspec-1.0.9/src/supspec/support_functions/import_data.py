#enter filename, rest wavelength
from supspec.support_functions.support_functions import *
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import math
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams['interactive'] == True

def user_input():
    lowerbound = float(input("lowerbound: "))
    upperbound = float(input("upperbound: "))
    return lowerbound, upperbound
    
def import_data (filenames, x1, x2, true_wavelength, Q_V = 'Q', data_dir = 'data'):
    wavelengths_windows = {}
    fluxes_windows = {}
    wavelengths_normalizeds = {}
    fluxes_normalizeds = {}
    for filename in filenames:
        data_loaded = np.loadtxt(data_dir + "/" + filename)
        wavelengths = data_loaded[:,0]
        fluxes = data_loaded[:,1]
        
        if not os.path.isdir('Results_'+str(true_wavelength) ):
            os.mkdir('Results_'+str(true_wavelength))
        if not os.path.isdir('Results_'+str(true_wavelength)+'/Spectrum_'+filename[:filename.index('.txt')]):
            os.mkdir('Results_'+str(true_wavelength)+'/Spectrum_'+filename[:filename.index('.txt')])
        
        W = 15
        H = 8

        fig, ax = plt.subplots(1, 2, figsize = (W, H))
               
        ax1 = ax[0]
        ax2 = ax[1]

        ax1 = make_axis(ax1)
        ax2 = make_axis(ax2)
        fig.suptitle("Spectrum ("+filename[:filename.index('.txt')]+")", fontsize = 35, weight = 'bold')
        ax1.set_title("Original Spectrum", fontsize = 20, pad =10)
        ax2.set_title("Window", fontsize = 20, pad =10)
        fig.supxlabel(r'Wavelength ($\AA$)', fontsize = 25)
        fig.supylabel(r"Flux", fontsize = 25)
        
        
        colors = get_colors(3, 'chill')
        idx = np.where ((wavelengths > x1) & (wavelengths < x2))
        wavelengths_window = wavelengths[idx]
        fluxes_window = fluxes[idx]      
        


        f_to_keep = []
        w_to_keep = []
        for i in range(len(fluxes_window)):
            y_smoothed=savgol_filter(fluxes_window, 30, 2)
            sig=np.std(y_smoothed - fluxes_window)
            n=3
            
            orig_flux = fluxes_window[i]
            smooth_y = y_smoothed[i]
            diff = abs(orig_flux - smooth_y)
            
            if diff < n*sig:
           
                f_to_keep.append(fluxes_window[i])
                w_to_keep.append(wavelengths_window[i])

       
        ax1.plot(wavelengths, fluxes, linewidth = 2, color = colors[0], alpha = 0.4)
        ax1.plot(wavelengths[idx], fluxes[idx], linewidth = 4, color = colors[0], alpha = 1.0)
        ax1.vlines([x1, x2], min(fluxes), max(fluxes), linewidth = 2, color = colors[1])                     
        ax2.plot(w_to_keep, f_to_keep, linewidth = 3, color = colors[0])
        
        plt.savefig('Results_'+str(true_wavelength)+'/Spectrum_'+ filename[:filename.index('.txt')] +'/Spectrum_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        
        
        if Q_V.upper() != 'Q':
            plt.show(block=False)
            plt.pause(1)
            answer = input("Working on file " +filename+ ": Do you like the window? y/n (y): ") 
            while answer.lower() == "n": 
                lowerbound, upperbound = user_input()
                idx = np.where ((wavelengths > lowerbound) & (wavelengths < upperbound))
                wavelengths_window = wavelengths[idx]
                fluxes_window = fluxes[idx]
                
                
                f_to_keep.clear()
                w_to_keep.clear()
                for i in range(len(fluxes_window)):
                    y_smoothed=savgol_filter(fluxes_window, 30, 2)
                    sig=np.std(y_smoothed - fluxes_window)
                    n=3
                    orig_flux = fluxes_window[i]
                    smooth_y = y_smoothed[i]
                    diff = abs(orig_flux - smooth_y)
                    if diff < n*sig:
                        f_to_keep.append(fluxes_window[i])
                        w_to_keep.append(wavelengths_window[i])
                ax2.cla()
                ax2.plot(w_to_keep, f_to_keep, linewidth = 3, color = colors[0])
                
                ax1.cla()
                ax1.plot(wavelengths, fluxes, "b-", linewidth = 2, color = colors[0], alpha = 0.4)
                ax1.plot(wavelengths[idx], fluxes[idx], "b-", linewidth = 4, color = colors[0], alpha = 1.0)
                ax1.vlines([x1, x2], min(fluxes), max(fluxes), linewidth = 2, color = colors[1])    
                ax1.vlines([lowerbound, upperbound], min(fluxes), max(fluxes), linewidth = 2, color = colors[2])
                
                plt.pause(1)
                
                ax1.cla()
                ax1.plot(wavelengths, fluxes, "b-", linewidth = 2, color = colors[0], alpha = 0.4)
                ax1.plot(wavelengths[idx], fluxes[idx], "b-", linewidth = 4, color = colors[0], alpha = 1.0)
                ax1.vlines([lowerbound, upperbound], min(fluxes), max(fluxes), linewidth = 2, color = colors[2])
                
                plt.savefig('Results_'+str(true_wavelength)+'/Spectrum_'+ filename[:filename.index('.txt')] +'/Spectrum_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
                answer = input("Working on file " +filename+ ": Do you like the new window? y/n (y): ")
        plt.close()
        
        wavelengths_normalized = (w_to_keep - np.mean(w_to_keep))/np.std(w_to_keep)
        fluxes_normalized = (f_to_keep- np.mean(f_to_keep))/np.std(f_to_keep)
        wavelengths_windows[filename] = w_to_keep
        fluxes_windows[filename] = f_to_keep
        wavelengths_normalizeds[filename] = wavelengths_normalized
        fluxes_normalizeds[filename] = fluxes_normalized  
            
    return wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds


