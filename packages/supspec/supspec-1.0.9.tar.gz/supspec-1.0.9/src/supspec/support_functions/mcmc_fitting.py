from supspec.support_functions.support_functions import *

def normal_dist (x, mu, sigma, c, D):
    A = (1/(sigma*(2*np.pi)**0.5))
    B = -1*(x-mu)**2/(2*sigma**2)
    y = -1*D*A*np.exp(B)+c

    return y


def loss_function(inp, x, y_true):
    mu, sigma, c, D, err = inp

    if err < 0 or err > 5 or c < 0 or mu < -2 or mu > 2 or sigma > 8 or sigma < 0 or D < 0 or D > 100:
        return -np.inf

    y_fitted=normal_dist(x = x, mu=mu, sigma=sigma, c=c, D = D)
    
    return np.sum(-1.0*(y_true-y_fitted)**2.0)/err-np.exp(err)
  
  

def create_initial_guesses(nwalkers):
    
    c_reasonable=0.5

    mu_reasonable = 0.1
    sigma_reasonable = 3

    D_reasonable = 1.0

    err_reasonable=0.01
    
    initial_guesses = []
    for walker in range(nwalkers):
        mu_guess = mu_reasonable * (1+0.1*np.random.random())
        sigma_guess = sigma_reasonable * (1+0.1*np.random.random())
        c_guess = c_reasonable * (1+1*np.random.random())
        D_guess = D_reasonable * (1+0.1*np.random.random())
        err_guess = err_reasonable * (1+0.1*np.random.random())

        initial_guesses.append([mu_guess, sigma_guess,c_guess, D_guess, err_guess])
    return initial_guesses


def fitting(true_wavelength, W_new, F_new, nwalkers, loss_function, n_iterations, filenames, Q_V = 'Q'):
  
    mu_s = {}
    sigma_s = {}
    c_s = {}
    D_s = {}
    err_s = {}
    
    for filename in filenames:
        initial_guesses=(create_initial_guesses(nwalkers))
        sampler = emcee.EnsembleSampler(nwalkers = nwalkers, ndim = 5, log_prob_fn = loss_function, kwargs = {"y_true":F_new[filename], "x": W_new[filename]})
        sampler.run_mcmc(initial_guesses, n_iterations, progress = True)

        samples=sampler.get_chain()
        
        mu_found=samples[:,:,0]
        sigma_found=samples[:,:,1]
        c_found=samples[:,:,2]
        D_found=samples[:,:,3]
        err_found=samples[:,:,4]
                   
        mu_s[filename] = mu_found
        sigma_s[filename] = sigma_found
        c_s[filename] = c_found
        D_s[filename] = D_found
        err_s[filename] = err_found

      
    return mu_s, sigma_s, c_s, D_s, err_s 