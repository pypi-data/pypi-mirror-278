import spiceypy as spice
from astroquery.simbad import Simbad
from PyAstronomy import pyasl
import logging

def jupiter_altitude_limit(altitude=1000):
    """
    Set the altitude limit for occultation above the 1 bar level of Jupiter.

    Parameters
    ----------
    altitude : int or float, optional
        Altitude value to be added to the 1 bar level (default: 1000).

    Returns
    -------
    numpy.ndarray
        Updated ellipsoid radii of Jupiter.
    """
    radii = spice.gdpool("BODY599_RADII", 0, 3)
    radii += altitude
    spice.pdpool("BODY599_RADII", radii)

    return radii


def star2kpool(star, verbose=False):
    '''Obtain star coordinates and add them to the kernel pool.'''

    try:
        star_simbad = Simbad.query_object(star)
        # Convert coordinates from h:m:s to degrees
        ra, dec = pyasl.coordsSexaToDeg(f"{star_simbad['RA'][0]} {star_simbad['DEC'][0]}")
        if verbose:
            logging.info(f'Star {star} found in DB with RA {ra} deg, DEC {dec} deg')
        # Add star to kernel pool
        if len(star.split()) > 1:
            star = '-'.join(star.split())
        spice.pdpool(f"{star.upper()}_COORDS",  [ra, dec])
    except BaseException:
        logging.exception(f"Star {star} not found in Simbad.")
        raise

    return ra, dec