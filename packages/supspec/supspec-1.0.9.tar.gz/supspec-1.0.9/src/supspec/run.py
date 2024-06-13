#run the code
import sys
from supspec.support_functions.support_functions import *
from supspec.support_functions.import_data import *
from supspec.support_functions.mcmc_fitting import *
from supspec.support_functions.plot import *
from tqdm import tqdm
import warnings 
warnings.filterwarnings('ignore')


def universe(Q_V = 'Q', data_dir = 'data/', user_extension = ''):

    #print("please put all your data files in a folder called 'data'")
    extensions = ['.txt', '.data', '.out']
    if len(user_extension) > 0:
        extensions.append(user_extension)

    print("data_dir: "+str(data_dir))
    filenames = []
    for file in os.listdir(data_dir):
        for extension in extensions:
            if extension in str(file):
                filenames.append(file)

    #Example Oxygen line
    true_wavelength = 7775
    lowerbound = 7500
    upperbound = 7860

    true_wavelength = float(input('what is the true wavelength?'))
    lowerbound = float(input('what is the lowerbound?'))
    upperbound = float(input('what is the upperbound?'))

    wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds = import_data(filenames, lowerbound, upperbound, true_wavelength, Q_V = Q_V, data_dir = data_dir)

    nwalkers = 20
    if Q_V.upper() != 'Q':
        answer = input("How many walkers do you want (20) ? ")
        if is_integer(answer): 
            nwalkers = int(answer)
            answer2 = input("The current number of walkers is " + str(nwalkers) + "\nPress return to confirm: ")
            while len(answer2) > 0:
                nwalkers = int(input("How many walkers do you want (" +str(nwalkers)+ ") ? "))
                answer2 = input("The current number of walkers is " +str(nwalkers) + "\nPress return to confirm: ")


    n_iterations =5000
    if Q_V.upper() != 'Q':
        answer = input("How many interations do you want (5000) ? ")
        if is_integer(answer): 
            n_iterations = int(answer)
            answer2 = input("The current number of iterations is " + str(n_iterations) + "\nPress return to confirm: ")
            while len(answer2) > 0:
                n_iterations = int(input("How many iterations do you want (" +str(n_iterations)+ ")  ? "))
                answer2 = input("The current number of iterations is " + str(n_iterations) + "\nPress return to confirm: ")
        
    #finding fitted normalized values for fitted function
    mu_s, sigma_s, c_s, d_s, err_s = fitting(true_wavelength, wavelengths_normalizeds, fluxes_normalizeds, nwalkers, loss_function, n_iterations, filenames, Q_V = Q_V)


    #getting fitted parameters in denormalized (physical) units, and plot fitted function over real spectrum
    real_mu_s_s, real_sigma_s_s, real_c_s_s = plot_and_denormalize(mu_s, sigma_s, c_s, d_s, err_s, filenames, true_wavelength, wavelengths_normalizeds, fluxes_normalizeds, wavelengths_windows, fluxes_windows, lowerbound, upperbound, Q_V = Q_V)


    write_velocities(filenames, true_wavelength, real_mu_s_s, real_sigma_s_s, Q_V = Q_V)

    rerun = 'n'
    if Q_V.upper() != 'Q':
        rerun = input("Should I rerun the fit? (n)")
    return rerun


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument('-d', "--directory", dest='directory', default='data/', type=str,help='Directory that holds spectroscopy data')
    parser.add_argument('-e', "--extensions", dest='extensions', default='', type=str,help='File extension of spectroscopy provided')

    args = parser.parse_args()

    data_dir = args.directory
    if args.verbose == 1:
        Q_V = 'V'
    else:
        Q_V = 'Q'

    user_extension = ''
    if len(args.extensions)> 0 :
        user_extension = args.extensions

    rerun = 'y'
    while rerun != 'n' and len(rerun) > 0:
        rerun = universe(Q_V = Q_V, data_dir = data_dir, user_extension = user_extension)




if __name__ == "__main__":
    main()
