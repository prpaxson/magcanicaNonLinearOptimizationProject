import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from lmfit import create_params, Parameters

def randomize_parameters():
    """
    Create LMFIT model parameters initialized randomly between [0,1)

    Returns:
    p -- Model parameters loaded with random values
    """
    p = Parameters()
    # Each value can be constrained if needed
    p.add("rAmp", value=np.random.random())
    p.add("thetaAmp", value=np.random.random())
    p.add("thetaFreq", value=np.random.random())
    p.add("thetaPhase", value=np.random.random())
    p.add("phiAmp", value=np.random.random())
    p.add("phiFreq", value=np.random.random())
    p.add("phiPhase", value=np.random.random())
    return p

def str_to_datetime(s):
    """
    Convert timestamp string to datetime object

    Keyword arguments:
    s -- timestamp string to convert

    Returns:
    t -- datetime representation of timestamp
    """
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

def plot_cart(x,y,z):
    """
    Plot 3-D cartesian coordinates with MatPlotLib

    Keyword arguments:
    x, y, z -- Cartesian coordinates
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(x,y,z)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

def plot_spher(r,theta,phi):
    """
    Plot spherical coordinates with MatPlotLib

    Keyword arguments:
    r, theta, phi -- Spherical coordinates
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    x,y,z = spher_to_cart(r,theta,phi)
    ax.scatter(x,y,z)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

def plot_residual_histogram(r, save_path=None, num_bins=30):
    """
    Plots residuals in a histogram

    Keyword arguments:
    r         -- Residuals to plot
    save_path -- Path to save image to, if none is given then will show plot
    num_bins  -- Number of bins in the histogram, by default 30
    """
    fig = plt.figure()
    fig.suptitle('Residuals Histogram', fontsize=20)
    hist, bins = np.histogram(r, bins=num_bins)
    plt.bar((bins[:-1] + bins[1:]) / 2, hist, align='center', width=0.8 * (bins[1] - bins[0]))
    if save_path:
        plt.savefig(save_path + "residual_histogram.png")
    plt.show()

def plot_residual_over_time(t, r, save_path=None):
    """
    Plots residuals as a function of time

    Keyword arguments:
    t         -- Array of datetime object series representing timestamp of each measurement
    r         -- Residual corresponding with the timestamp
    save_path -- Path to save image to, if none is given then will show plot
    """
    fig = plt.figure()
    fig.suptitle('Residuals over time')
    ax = fig.add_subplot()

    if len(t) == 1:
        ax.scatter(t[0], r)
    else:
        # If there are multiple datasets used, plot in separate colors
        ax.scatter(t[0], r[0:len(t[0])], label="char_1")
        ax.scatter(t[1], r[len(t[0]):], label="char_2")
        plt.legend()
    ax.set_xlabel("Time")
    ax.set_ylabel("Residual")
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    if save_path:
        plt.savefig(save_path + "residuals_over_time.png")
    plt.show()