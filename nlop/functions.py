import numpy as np

def cart_to_spher(x, y, z):
    """
    Calculates spherical coordinates based off of 3-D cartesian coordinates

    Based off Wolfram reference: https://mathworld.wolfram.com/SphericalCoordinates.html

    Keyword arguments:
    x, y, z       -- Cartesian coordinates

    Returns:
    r, theta, phi -- Spherical coordinate equivalent (in rads)
    """
    r = np.sqrt(np.square(x) + np.square(y) + np.square(z))
    theta = np.arctan2(y,x)
    phi = np.arccos(z/r)
    return r, theta, phi

def spher_to_cart(r, theta, phi):
    """
    Calculates 3-D cartesian coordinates based off of spherical coordinates

    Based off Wolfram reference: https://mathworld.wolfram.com/SphericalCoordinates.html

    Keyword arguments:
    r, theta, phi -- Spherical coordinates (in rads)

    Returns:
    x, y, z       -- Cartesian coordinate equivalent
    """
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    return x, y, z

def f(r, theta, phi, p):
    """
    Specific function for NL LS optimization

    f(r,theta,psi,p) = p[0]*r^2 + p[1]*sin(p[2]*theta+p[3])^2 + p[4]*sin(p[5]*psi+p[6])^2

    Keyword Arguments:
    r, theta, phi       -- Spherical coordinates (in rads)
    p                   -- 7 weight dictionary
    
    Returns:
    f(r, theta, phi, p) -- calculation defined in Project Objective
    """
    return p["rAmp"] * np.square(r) +\
        p["thetaAmp"] * np.square(np.sin(p["thetaFreq"] * theta + p["thetaPhase"])) +\
        p["phiAmp"] * np.square(np.sin(p["phiFreq"] * phi + p["phiPhase"]))

def residual_calc(p, x, y, z, v):
    """
    Calculates residuals using measured & predicted outputs

    Keyword Arguments:
    p       -- Dictionary of weight parameters
    x, y, z -- Cartesian coordinates
    v       -- Output vector corresponding with coordinates

    Returns:
    Vector of residuals
    """
    return v - f(*cart_to_spher(x, y, z), p)