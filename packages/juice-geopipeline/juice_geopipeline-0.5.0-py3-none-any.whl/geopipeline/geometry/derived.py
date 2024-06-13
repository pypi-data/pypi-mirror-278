import spiceypy as spice
import numpy as np


def crossproduct_tour_zaxis_flip(utc: str = '', et = None):
    """
    Compute the Cross Product of +Xsc in the "Default Attitude" and +Z of the "ECLIP2000" frame.

    Parameters
    ----------
    time_et : float or np.ndarray
        Ephemeris time. It represents the time in seconds past J2000 epoch. If it's a single float value, the computation
        will be performed for that specific time. If it's a NumPy array, the computation will be done for each value in
        the array, and the resulting cross product vectors will be returned as a 2D NumPy array.

    body : str
        The name of the body for which the cross product is to be calculated. This specifies the frame transformation
        from the "Default Attitude" frame to the "ECLIP2000" frame.

    Returns
    -------
    np.ndarray or List[np.ndarray]
        If `time_et` is a single float, this function returns a 1D NumPy array representing the cross product vector of
        +Xsc and +Zsc in the specified body's frame.
        If `time_et` is a 1D NumPy array, this function returns a list of 1D NumPy arrays, each representing the cross
        product vector at the corresponding time in the `time_et` array.

    Note
    ----
    This function is used to calculate the S/C flips during the Tour phase assuming default attitude,
    and as requested by the MAJIS team during the PJ12 Meeting in January 2023.
    """
    if utc:
        et = spice.utc2et(str(utc))
    # Express +Xsc in the JUICE_JUPITER_NPO FRAME
    xsc = [1, 0, 0]
    # +Z in ECLIPJ2000
    z_eclipj2000 = [0, 0, 1]
    # rotation matrix from JUICE_JUPITER_NPO to ECLIPJ2000
    mat_sc_eclipj2000 = spice.pxform('JUICE_JUPITER_NPO', 'ECLIPJ2000', et)
    # Take +Xsc position in ECLIPJ2000 frame
    xsc_eclipj2000 = spice.mxv(mat_sc_eclipj2000, xsc)
    # Cross product of +Xsc and Zeclipj200 in ECLIPJ2000 frame
    crossxsczecl = spice.vcrss(xsc_eclipj2000, z_eclipj2000)

    # Express cross product of +Xsc and +Zeclipj2000 in JUICE_JUPITER_NPO
    # rotation matrix from ECLIPJ2000 to JUICE_SPACECRAFT
    mat_eclipj2000_sc = spice.pxform('ECLIPJ2000', 'JUICE_JUPITER_NPO', et)
    # Compute cross product vecor coordinates in JUICE_SPACECRAFT frame
    crossxsczecl_sc = spice.mxv(mat_eclipj2000_sc, crossxsczecl)

    return crossxsczecl_sc


def dotproduct_cruise_yaxis_polarity(utc: str = '', et = None, target='EARTH'):
    '''
    Calculate the spacecraft's Y-axis polarity between a given target (Earth, Moon, Venus) and the Sun.

    If the result is > 0 this means that the favorable polarity of the JUICE S/C Hot Cruise Default Attitude in
    order to have an intersection of the S/C +Z axis with the target is positive (+Y towards the Ecliptic
    North), if the result is < 0 the favorable polarity for an intersection is negative (+Y towards the
    Ecliptic South).

    This has been described by Flight Dynamics' as:

         Xsc = -Sc2SunDir
         Ysctmp = Xsc ^ Sc2EarthDir
         Zsctmp = Xsc ^ Ysctmp

         If( Zsctmp . Sc2EarthDir >= 0 )
         {
             Ysc = Ysctmp
             Zsc = Zsctmp
         }
         Else
         {
             Ysc = -Ysctmp
             Zsc = -Zsctmp
         }

    Parameters
    ----------
    utc : str, optional
        UTC time string, by default ''
    et : float, optional
        Ephemeris time, by default None
    target : str, optional
        Target celestial body ('EARTH', 'MOON', 'VENUS'), by default 'EARTH'

    Returns
    -------
    float
        Dot product of the spacecraft's +Z axis and the vector from the spacecraft to the target.
    '''
    if utc:
        et = spice.utc2et(str(utc))

    sc2tar, lt = spice.spkpos(target, et, 'J2000', 'NONE', 'JUICE')
    sc2tar, mod = spice.unorm(sc2tar)

    mat = spice.pxform('JUICE_CRUISE_HOT_POS', 'J2000', et)

    zsc = spice.mxv(mat, [0, 0, 1])

    dotxtarsun_sc = spice.vdot(zsc, sc2tar)

    return dotxtarsun_sc


def ground_track_velocity(time_et, body):
    """Get the ground-track velocity as computed by the RIME team.

    Parameters
    ----------
    time_et : float or np.ndarray
        Ephemeris time.
    body : str
        Name of the celestial body on which the ground-track
        is wanted. The body must have an ``IAU_``` frame associated.

    Returns
    -------
    gtvel_rad : float
        Radial velocity of the ground track in km/s.
    gtvel_tan : float
        Tangential velocity of the ground track in km/s.
    gt_vel : float
        Total velocity of the ground track in km/s.

    Note
    ----
    This function is adapted/discussed/compared with Massimo Santoni
    from the RIME Team in February 2019.

    Translated from the IDL procedure:`Planning.pro:Get_Ground_Track_velocity`
    """
    # Initialize variables
    if not isinstance(time_et, np.ndarray):
        time_et = np.full(1, time_et)

    n_t = len(time_et)

    observer = 'JUICE'
    ref_frame = 'IAU_' + body
    radii = spice.bodvrd(body, 'RADII', 3)[1]
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re

    geodetic_speed = np.zeros((n_t, 3))
    lon = np.zeros(n_t)
    lat = np.zeros(n_t)
    radial_speed = np.zeros(n_t)
    tangential_speed = np.zeros(n_t)
    gt_speed = np.zeros(n_t)

    for i in range(n_t):
        # Compute the state vector (position (1:3), speed(4:6)) for each second
        state, _ = spice.spkezr(observer, time_et[i], ref_frame, 'NONE', body)

        # Compute longitude, latitude, and altitude from the state vector
        lon_tmp, lat_tmp, alt = spice.recgeo(state[:3], re, f)
        lon[i] = lon_tmp
        lat[i] = lat_tmp

        # Compute the Jacobian Matrix to convert the speed to a body-fixed reference frame (in this case in Geodetic coordinates)
        jacobi = spice.dgeodr(state[0], state[1], state[2], re, f)
        vel = state[3:]
        temp = spice.mxv(jacobi, vel)
        geodetic_speed[i,:] = temp

        # From the geodetic speed extract the radial component
        radial_speed[i] = geodetic_speed[i, 2]

        # the tangential speed is obtained as product of the local radius of the
        #  observed body with the tangential angular speed:
        #
        #  latitudinal component
        #  ^  x
        #  | / tangential component
        #  |/
        #  o---> longitudinal component (the cos is to compensate the "shrinking" of
        #                                 longitude incerasing the latitude)
        #
        local_radius = (re * rp) / np.sqrt((re**2 * np.sin(lat[i])**2) + (rp**2 * np.cos(lat[i])**2))
        tangential_speed[i] = local_radius * np.sqrt((np.array([geodetic_speed[i,0]*np.cos(lat[i])])**2) + (np.array([geodetic_speed[i,1]])**2))
        gt_speed[i] = np.sqrt(tangential_speed[i]**2 + radial_speed[i]**2)

        # if the output is not an array, then turn a float per value
        if len(radial_speed) == 1:
            radial_speed = radial_speed[0]
            tangential_speed = tangential_speed[0]
            gt_speed = gt_speed[0]

    return radial_speed, tangential_speed, gt_speed



def ray_tangent_point(utc: str = '', et = None, ray_target = 'EARTH', target='JUPITER', abcorr='LT+S',):
    """
    Get the tangent point of a ray on a target.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    ray_target : str, optional
        Target for the ray's position calculation (default: 'EARTH').
    target : str, optional
        Target celestial body for tangent point calculation (default: 'JUPITER').
    abcorr : str, optional
        Aberration correction method (default: 'LT+S').

    Returns
    -------
    tuple
        A tuple containing two values:
        - Ratio of the altitude of the tangent point to the target's equatorial radius.
        - Tuple containing spherical coordinates of the tangent point's surface position:
            (altitude ratio, longitude in degrees, latitude in degrees).
    """
    if utc:
        et = spice.utc2et(str(utc))

    ray_frame = 'J2000'
    radii = spice.gdpool("BODY599_RADII", 0, 3)
    ray = spice.spkezr(ray_target, et, ray_frame, abcorr, 'JUICE')[0][0:3]
    tanpt, alt, range, srfpt, trgepc, srfvec = \
        spice.tangpt('ELLIPSOID', target, et, f'IAU_{target}', abcorr, 'TANGENT POINT', 'JUICE', ray_frame, ray)

    srfpt_alt, srfpt_lon, srfpt_lat = spice.reclat(srfpt)

    return alt/radii[1], (srfpt_alt/radii[1], srfpt_lon*spice.dpr(), srfpt_lat*spice.dpr())


def sun_direction(utc='', et=None, abcorr='NONE', frame='JUICE_SPACECRAFT'):
    """
    Calculate the direction vector from JUICE to Sun.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    np.ndarray
        A normalized vector representing the direction from the spacecraft to Sun.
    """
    if utc:
        et = spice.utc2et(str(utc))
        # Calculate the spacecraft to Sun vector in the spacecraft frame
    sc2sun_vec, lt = spice.spkpos('SUN', et, frame, abcorr, 'JUICE')
    # Normalize the spacecraft to Sun vector
    return sc2sun_vec / np.linalg.norm(sc2sun_vec)


def earth_direction(utc='', et=None, abcorr='NONE', frame='JUICE_SPACECRAFT'):
    """
    Calculate the direction vector from JUICE to Earth.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    np.ndarray
        A normalized vector representing the direction from the spacecraft to Earth.
    """
    if utc:
        et = spice.utc2et(str(utc))
        # Calculate the spacecraft to Earth vector in the spacecraft frame
    sc2earth_vec, lt = spice.spkpos('EARTH', et, frame, abcorr, 'JUICE')
    # Normalize the spacecraft to Earth vector
    return sc2earth_vec / np.linalg.norm(sc2earth_vec)


def jupiter_orbit_body_latitude(utc='', et=None, body='AMALTHEA', abcorr='NONE'):
    """
    Get the latitude of a body's orbit around Jupiter.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    body : str, optional
        Name of the celestial body orbiting Jupiter (default: 'AMALTHEA').
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    float
        Latitude of the body's orbit around Jupiter in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))
    moon2jup, lt = spice.spkpos(body.upper(), et, 'JUICE_JSO', abcorr, 'JUPITER')
    radius, intlon, intlat = spice.reclat(moon2jup)
    return intlat * spice.dpr()


def jupiter_moon_transit_latitude(utc='', et=None, moon='AMALTHEA', abcorr='NONE'):
    """
    Get the latitude of a Jupiter moon's transit.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    moon : str, optional
        Name of the Jupiter moon (default: 'AMALTHEA').
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    float
        Latitude of the Jupiter moon's transit in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))
    sc2moon, lt = spice.spkpos(moon.upper(), et, 'IAU_JUPITER', abcorr, 'JUICE')
    sc2jupr, lt = spice.spkpos('JUICE', et, 'IAU_JUPITER', abcorr, 'JUPITER')
    dim, radii = spice.bodvrd('JUPITER', 'RADII', 3)
    try:
        intxyz = spice.surfpt(sc2jupr, sc2moon, radii[0], radii[1], radii[2])
        radius, intlon, intlat = spice.reclat(intxyz)
    except:
        return False
    return intlat * spice.dpr()


def jupiter_moon_distance(utc='', et=None, moon='AMALTHEA', abcorr='NONE'):
    """
    Get the distance of a Jupiter moon from Jupiter.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    moon : str, optional
        Name of the Jupiter moon (default: 'AMALTHEA').
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    float
        Distance of the Jupiter moon from Jupiter normalized by Jupiter's equatorial radius.
    """
    if utc:
        et = spice.utc2et(str(utc))
    pos, lt = spice.spkpos('JUPITER', et, 'J2000', abcorr, moon)
    dist = np.linalg.norm(pos)
    dim, radii = spice.bodvrd('JUPITER', 'RADII', 3)
    return dist / radii[1]


def jupiter_moon_phase_angle(utc='', et=None, moon='AMALTHEA', abcorr='NONE'):
    """
    Get the phase angle of a Jupiter moon.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    moon : str, optional
        Name of the Jupiter moon (default: 'AMALTHEA').
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    float
        Phase angle of the Jupiter moon in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))
    spoint, trgepc, srfvec = spice.subpnt('INTERCEPT/ELLIPSOID', moon, et, f'IAU_{moon}', abcorr, 'JUICE')
    trgepc, srfvec, phase, incdnc, emissn, visibl, lit = \
        spice.illumf('ELLIPSOID', moon.upper(), 'SUN', et, f'IAU_{moon.upper()}', abcorr, 'JUICE', spoint)

    return phase * spice.dpr()


def jupiter_moon_separation(utc='', et=None, moon='AMALTHEA', abcorr='NONE'):
    """
    Get the angular separation between Jupiter and one of its moons.

    Parameters
    ----------
    utc : str, optional
        UTC time string (default: ''). If provided, `et` will be computed using spice.utc2et().
    et : float or None, optional
        Ephemeris Time (default: None). Represents the ephemeris time.
        If `utc` is not provided, it needs to be specified.
    moon : str, optional
        Name of the Jupiter moon (default: 'AMALTHEA').
    abcorr : str, optional
        Aberration correction method (default: 'NONE').

    Returns
    -------
    float
        Angular separation between Jupiter and the specified moon in degrees.
    """
    if utc:
        et = spice.utc2et(str(utc))
    ang = spice.trgsep(et, moon.upper(), 'SPHERE', 'NULL', 'JUPITER', 'SPHERE', 'NULL', 'JUICE', abcorr)
    return ang * spice.dpr()


def sun_earth_juice_angle(utc: str = '', et=None):
    '''Superior Conjunction'''
    if utc:
        et = spice.utc2et(str(utc))

    earth_juice, i = spice.spkpos(targ='JUICE', et=et, ref='J2000', abcorr='NONE', obs='EARTH')
    earth_sun, i = spice.spkpos(targ='SUN', et=et, ref='J2000', abcorr='NONE', obs='EARTH')
    angle = spice.vsep(earth_juice, earth_sun) * spice.dpr()
    return angle