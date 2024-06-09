import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from apsimNGpy.experiment.variable import BoundedVariable

a_true = 3
b_true = 6
sigma_true = 2
n = 100  # Length of data series

# For the independent variable, x, we will choose n values equally spaced
# between 0 and 10
x = np.linspace(0, 10, n)

# Calculate the dependent (observed) values, y
y = a_true * x + b_true + np.random.normal(loc=0, scale=sigma_true, size=n)


# Define quasi maximum loss function
#####################################################################
def NSE(params, obs, simulator_func):
    """ Nash-Sutcliffe efficiency.
    """
    # Run simulation
    sim = simulator_func(*params)

    # NS
    num = np.sum((sim - obs) ** 2)
    denom = np.sum((obs - obs.mean()) ** 2)
    ns = 1 - (num / denom)

    return [ns, sim]


# set the threshold and the sample size
ns_min = 0.7
n_samp = 4000

# priors
a_min, a_max = -10, 10
b_min, b_max = -10, 10
sigma_min, sigma_max = 0, 10

# sample from the prior using monte carlo
a_s = np.random.uniform(low=a_min, high=a_max, size=n_samp)
b_s = np.random.uniform(low=b_min, high=b_max, size=n_samp)


# For each of the parameter sets drawn above, we run the model and calculate the Nash-Sutcliffe efficiency.
# If it's above the behavioural threshold we'll store that parameter set and the associated model output, otherwise we'll discard both.

def _eval_observed(params, obs):
    """ Evaluate the observed it should be in the same year and same length"""

def run_glue(a_s, b_s, n_samp, ns_min):
    """ Run GLUE analysis.
        Uses nash_sutcliffe() to estimate performance and returns
        dataframes containing all "behavioural" parameter sets and
        associated model output.
    """
    # Store output
    out_params = []
    out_sims = []

    # Loop over param sets
    for idx in range(n_samp):
        params = [a_s[idx], b_s[idx]]

        # Calculate Nash-Sutcliffe
        ns, sim = NSE(params, x, y)

        # Store if "behavioural"
        if ns >= ns_min:
            params.append(ns)
            out_params.append(params)
            out_sims.append(sim)

    # Build df
    params_df = pd.DataFrame(data=out_params,
                             columns=['a', 'b', 'ns'])

    assert len(params_df) > 0, 'No behavioural parameter sets found.'

    # Number of behavioural sets
    print('Found %s behavioural sets out of %s runs.' % (len(params_df), n_samp))

    # DF of behavioural simulations
    sims_df = pd.DataFrame(data=out_sims)

    return params_df, sims_df





# time to estimate the confidence itnerval

def weighted_quantiles(values, quantiles, sample_weight=None):
    """ Modified from
        http://stackoverflow.com/questions/21844024/weighted-percentile-using-numpy
        NOTE: quantiles should be in [0, 1]
        values array with data
        quantiles array with desired quantiles
        sample_weight array of weights (the same length as `values`)
        Returns array with computed quantiles.
    """
    # Convert to arrays
    values = np.array(values)
    quantiles = np.array(quantiles)

    # Assign equal weights if necessary
    if sample_weight is None:
        sample_weight = np.ones(len(values))

    # Otherwise use specified weights
    sample_weight = np.array(sample_weight)

    # Check quantiles specified OK
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), 'quantiles should be in [0, 1]'

    # Sort
    sorter = np.argsort(values)
    values = values[sorter]
    sample_weight = sample_weight[sorter]

    # Compute weighted quantiles
    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    weighted_quantiles /= np.sum(sample_weight)

    return np.interp(quantiles, weighted_quantiles, values)


def plot_glue(params_df, sims_df):
    """ Plot median simulation and confidence intervals for GLUE.
    """
    # Get weighted quantiles for each point in x from behavioural simulations
    weights = params_df['ns']
    quants = [0.025, 0.5, 0.975]

    # List to store output
    out = []

    # Loop over points in x
    for col in sims_df.columns:
        values = sims_df[col]
        out.append(weighted_quantiles(values, quants, sample_weight=weights))

    # Build df
    glue_df = pd.DataFrame(data=out, columns=['2.5%', '50%', '97.5%'])

    # Plot predicted
    plt.fill_between(x, glue_df['2.5%'], glue_df['97.5%'], color='r', alpha=0.3)
    plt.plot(x, glue_df['50%'], 'r-', label='Estimated')
    plt.title('GLUE')

    # Plot true line
    plt.plot(x, y, 'bo')
    plt.plot(x, a_true * x + b_true, 'b--', label='True')

    plt.legend(loc='best')

    plt.show()

    return glue_df





def glue_coverage(glue_df):
    """ Prints coverage from GLUE analysis.
    """
    # Add observations to df
    glue_df['obs'] = y

    # Are obs within CI?
    glue_df['In_CI'] = ((glue_df['2.5%'] < glue_df['obs']) &
                        (glue_df['97.5%'] > glue_df['obs']))

    # Coverage
    cov = 100. * glue_df['In_CI'].sum() / len(glue_df)

    print('Coverage: %.1f%%' % cov)

x =None
if __name__ == '__main__' and x:
    params_df, sims_df = run_glue(a_s, b_s, n_samp, ns_min)
    glue_df = plot_glue(params_df, sims_df)
    glue_coverage(glue_df)

    # The Nash-Sutlcliffe score can take any value from −∞ to 1, with 0 implying
    # the model output is no better than taking the mean of the observations. What happens if we relax the behavioural threshold by setting it to 0?
    ns_min = 0

    params_df, sims_df = run_glue(a_s, b_s, n_samp, ns_min)

    glue_df = plot_glue(params_df, sims_df)

    glue_coverage(glue_df)

    # changing it to 0.9 reduced the coverage
    ns_min = 0.9

    params_df, sims_df = run_glue(a_s, b_s, n_samp, ns_min)

    glue_df = plot_glue(params_df, sims_df)

    glue_coverage(glue_df)

    # if we set it to one, we are most likely not going to get anything, assertion error will ocure because designed it that way
    ns_min = 1
    try:
        params_df, sims_df = run_glue(a_s, b_s, n_samp, ns_min)

        glue_df = plot_glue(params_df, sims_df)

        glue_coverage(glue_df)
    except AssertionError as e:
        print(e)
        print('Please check your you behavioral value threshold')
