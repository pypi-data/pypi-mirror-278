import logging
import spiceypy as spice
from geopipeline.geometry.derived import crossproduct_tour_zaxis_flip
from geopipeline.geometry.derived import dotproduct_cruise_yaxis_polarity
from geopipeline.time import utc2win, win2lst, sec2hhmmss
from geopipeline.geometry.support import star2kpool


def stellar_occultations(utc_start='', utc_end='',
                         interval=False, step=600,
                         method='ELLIPSOID',
                         front_body='JUPITER',
                         fb_frame='IAU_JUPITER',
                         observer='JUICE',
                         star='ANTARES',
                         abcorr='NONE',
                         verbose=False,
                         **kwargs):
    """
     Find the stellar occultation of a given star by the indicated front body as seen from JUICE.

     Parameters
     ----------
     utc_start : str, optional
         Start time in UTC format (default: '').
     utc_end : str, optional
         End time in UTC format (default: '').
     interval : bool, optional
         Time interval (default: False).
     step : int, optional
         Step size (default: 600).
     method : str, optional
         Method to use (default: 'ELLIPSOID').
     front_body : str, optional
         Name of the front celestial body (default: 'JUPITER').
     fb_frame : str, optional
         Frame for the front body (default: 'IAU_JUPITER').
     observer : str, optional
         Name of the observer (default: 'JUICE').
     star : str, optional
         Name of the star (default: 'ANTARES').
     abcorr : str, optional
         Aberration correction (default: 'NONE').
     verbose : bool, optional
         Verbosity flag (default: False).
     **kwargs : dict
         Additional keyword arguments.

     Returns
     -------
     tuple
         Tuple containing the SPICE window and a list of time intervals.
     """
    # Get the star RA/Dec
    star_key_names = spice.gnpool("*_NAME", 0, 1000, 1000)
    for key_name in star_key_names:
        try:
            name = spice.gcpool(key_name, 0, 100, 100)[0]
        except:
            name = spice.gipool(key_name, 0, 100)
            name = f'{int(name):04}'
            pass
        if name.upper() == star.upper():
            star_key = f"{key_name.split('_NAME')[0]}_COORDS"
            break

    coords = spice.gdpool(star_key, 0, 2)
    ra = spice.convrt(coords[0], 'DEGREES', 'RADIANS')
    dec = spice.convrt(coords[1], 'DEGREES', 'RADIANS')

    ray2star = spice.radrec(1.0, ra, dec)

    # ensure no numpy bool conversion deprication warning is raised
    if not interval:
        cnfine = utc2win(utc_start, utc_end)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    nintvls = 40000

    riswin = spice.cell_double(nintvls)
    cnfine_filtered = spice.cell_double(nintvls)
    adjust = 0.0

    front_body_id = spice.bodn2c(front_body.upper())

    @spice.utils.callbacks.SpiceUDFUNS
    def gfqf(et):
        ptarg, lt = spice.spkezp(front_body_id, et, 'J2000', abcorr, -28)
        angsep = spice.vsep(ray2star, ptarg)
        if angsep > refval:
            return -1 * et
        else:
            return et

    @spice.utils.callbacks.SpiceUDFUNS
    def gfq(et):
        try:
            srfpt, epoch, rayd = spice.sincpt(method, front_body, et,
                                              fb_frame, abcorr, observer,
                                              "J2000", ray2star)
        except spice.utils.exceptions.NotFoundError:
            return -1 * et
        return et

    @spice.utils.callbacks.SpiceUDFUNB
    def gfdecrx(udfuns, et):
        return spice.uddc(udfuns, et, 10)

    spice.gfuds(gfq, gfdecrx, '>', 0, adjust, step, 20000, cnfine, riswin)

    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.warning(f'No stellar occultations for {star} with {front_body}.')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'{star} stellar occultation by {front_body}')
            logging.info('------------------------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info(f'Method:             {method}')
            logging.info(f'Front Body Name:    {front_body}')
            logging.info(f'Front Body Frame:   {fb_frame}')
            logging.info(f'Observer Name:      {observer}')
            logging.info(f'Star RA/DEC [deg]:  {ra * spice.dpr():3f} {dec * spice.dpr():3f}')
            logging.info('-----------------------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])
        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis


def sun_occultations(utc_start='', utc_end='',
                     interval=False, step=600,
                     method='ELLIPSOID',
                     front_body='JUPITER',
                     fb_frame='IAU_JUPITER',
                     observer='JUICE',
                     occtyp='ANY',
                     abcorr='NONE',
                     verbose=False,
                     **kwargs):
    """
    Find the Sun occultation by the indicated front body as seen from JUICE.

    Parameters
    ----------
    utc_start : str, optional
        Start time in UTC format (default: '').
    utc_end : str, optional
        End time in UTC format (default: '').
    interval : bool, optional
        Time interval (default: False).
    step : int, optional
        Step size (default: 600).
    method : str, optional
        Method to use (default: 'ELLIPSOID').
    front_body : str, optional
        Name of the front celestial body (default: 'JUPITER').
    fb_frame : str, optional
        Frame for the front body (default: 'IAU_JUPITER').
    observer : str, optional
        Name of the observer (default: 'JUICE').
    occtyp : str, optional
        Type of occultation (default: 'ANY').
    abcorr : str, optional
        Aberration correction (default: 'NONE').
    verbose : bool, optional
        Verbosity flag (default: False).
    **kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    tuple
        Tuple containing the SPICE window and a list of time intervals.
    """
    riswin, rislis = transits(utc_start=utc_start, utc_end=utc_end,
                              interval=interval, step=step,
                              method=method,
                              front_body=front_body,
                              fb_frame=fb_frame,
                              observer=observer,
                              back_body='SUN',
                              bb_frame='IAU_SUN',
                              occtyp=occtyp,
                              abcorr=abcorr,
                              verbose=verbose)

    return riswin, rislis

def earth_occultations(utc_start='', utc_end='',
                      interval=False, step=600,
                      method='ELLIPSOID',
                      front_body='JUPITER',
                      fb_frame='IAU_JUPITER',
                      observer='JUICE',
                      occtyp='ANY',
                      verbose=False,
                      abcorr='NONE',
                      **kwargs):
    """
    Find the Earth occultations by the indicated front body as seen from JUICE.

    Parameters
    ----------
    utc_start : str, optional
        Start time in UTC format (default: '').
    utc_end : str, optional
        End time in UTC format (default: '').
    interval : bool, optional
        Time interval (default: False).
    step : int, optional
        Step size (default: 600).
    method : str, optional
        Method to use (default: 'ELLIPSOID').
    front_body : str, optional
        Name of the front celestial body (default: 'JUPITER').
    fb_frame : str, optional
        Frame for the front body (default: 'IAU_JUPITER').
    observer : str, optional
        Name of the observer (default: 'JUICE').
    occtyp : str, optional
        Type of occultation (default: 'ANY').
    abcorr : str, optional
        Aberration correction (default: 'NONE').
    verbose : bool, optional
        Verbosity flag (default: False).
    **kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    tuple
        Tuple containing the SPICE window and a list of time intervals.
    """
    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    riswin = spice.cell_double(40000)

    spice.gfoclt(occtyp, front_body, 'ELLIPSOID', fb_frame, 'EARTH', 'ELLIPSOID', 'IAU_EARTH',
                 abcorr, 'JUICE', step, cnfine, riswin)

    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.warning(f'No EARTH occultations with {front_body}.')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'Earth occultation by {front_body}')
            logging.info('------------------------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info(f'Method:             {method}')
            logging.info(f'Front Body Name:    {front_body}')
            logging.info(f'Front Body Frame:   {fb_frame}')
            logging.info(f'Observer Name:      {observer}')
            logging.info('-----------------------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])
        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis


def tour_flip_zaxis(utc_start='', utc_end='', interval='',  step=3000, verbose=False):
    """
    Geometry Finder function for +Z axis flip events during the Tour.

    This function searches for flip events during the specified time interval (in UTC) and returns the
    intervals where +Z axis flips occur.

    A flip is defined when the cross product of +Xsc in the Jupiter Tour default attitude
    and +Z of the "ECLIP2000" frame changes its sign.

    Parameters:
    -----------
    utc_start : str
        Start time of the interval in UTC format.
    utc_end : str
        End time of the interval in UTC format.
    step : int, optional
        Time step used for searching flip events (default: 3000).
    verbose : bool, optional
        If True, logging.info additional information (default: False).

    Returns:
    --------
    tuple
        A tuple containing:
            - `riswin`: A SPICE window containing the time intervals where flip events occur.
            - `rislis`: A list of flip event intervals represented as [start_time, end_time] in UTC format.

    Note:
    -----
    The function uses SPICE utility gfuds to search for flip events and then converts the results
    into a list of intervals.
    """

    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    riswin = spice.cell_double(40000)
    adjust = 0.0

    @spice.utils.callbacks.SpiceUDFUNS
    def gfq(et):
        crossproduct = crossproduct_tour_zaxis_flip(et=et)
        if crossproduct[-1] > 0:
            return -1 * et
        return et

    @spice.utils.callbacks.SpiceUDFUNB
    def gfdecrx(udfuns, et):
        return spice.uddc(udfuns, et, 10)

    spice.gfuds(gfq, gfdecrx, '=', 0, adjust, step, 20000, cnfine, riswin)

    # The function wncard returns the number of intervals in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0:
        pass
    else:
        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            if verbose:
                timstr = spice.et2utc(intbeg, 'ISOC', 0, 70)
                logging.info(f'{timstr}')

            rislis.append([intbeg, intend])

    return riswin, rislis


def cruise_yaxis_polarity(utc_start='', utc_end='', interval='', target='EARTH', step=3000, verbose=False):
    """
    Calculate the intervals of Hot Cruise Phase with negative polarity.

    Provides the windows of the intervals of JUICE Hot Cruise Default Attitude with negative polarity (S/C +Y towards
    the Ecliptic South) for which a target (Earth, Moon, Venus) is towards the +Z S/C axis.

    Parameters
    ----------
    utc_start : str, optional
        Start time in UTC format (default: '').
    utc_end : str, optional
        End time in UTC format (default: '').
    interval : str, optional
        Time interval (default: '').
    target : str, optional
        Polarity target interval (default: 'EARTH').
    step : int, optional
        Step size (default: 3000).
    verbose : bool, optional
        Verbosity flag (default: False).

    Returns
    -------
    tuple
        Tuple containing the SPICE window and a list of time intervals.
    """
    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    riswin = spice.cell_double(40000)
    adjust = 0.0

    @spice.utils.callbacks.SpiceUDFUNS
    def gfq(et):
        dotproduct = dotproduct_cruise_yaxis_polarity(et=et, target=target)
        if dotproduct < 0:
            return -1 * et
        return et

    @spice.utils.callbacks.SpiceUDFUNB
    def gfdecrx(udfuns, et):
        return spice.uddc(udfuns, et, 10)

    spice.gfuds(gfq, gfdecrx, '<', 0, adjust, step, 20000, cnfine, riswin)

    # The function wncard returns the number of intervals in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0:
        pass
    else:
        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            if verbose:
                timstr = spice.et2utc(intbeg, 'ISOC', 0, 70)
                logging.info(f'{timstr}')

            rislis.append([intbeg, intend])

    return riswin, rislis


def transits(utc_start='', utc_end='',
             interval=False, step=60,
             method='ELLIPSOID',
             front_body='AMALTHEA',
             fb_frame='IAU_AMALTHEA',
             observer='JUICE',
             back_body='JUPITER',
             bb_frame='IAU_JUPITER',
             occtyp='ANY',
             abcorr='NONE',
             verbose=False):
    """
     Find transits or occultations between celestial bodies.

     Parameters
     ----------
     utc_start : str, optional
         Start time in UTC format (default: '').
     utc_end : str, optional
         End time in UTC format (default: '').
     interval : bool, optional
         Time interval (default: False).
     step : int, optional
         Step size (default: 60).
     method : str, optional
         Method to use (default: 'ELLIPSOID').
     front_body : str, optional
         Name of the front celestial body (default: 'AMALTHEA').
     fb_frame : str, optional
         Frame for the front body (default: 'IAU_AMALTHEA').
     observer : str, optional
         Name of the observer (default: 'JUICE').
     back_body : str, optional
         Name of the back celestial body (default: 'JUPITER').
     bb_frame : str, optional
         Frame for the back body (default: 'IAU_JUPITER').
     occtyp : str, optional
         Type of occultation (default: 'ANY').
     abcorr : str, optional
         Aberration correction (default: 'NONE').
     verbose : bool, optional
         Verbosity flag (default: False).

     Returns
     -------
     tuple
         Tuple containing the SPICE window and a list of time intervals.
     """
    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    riswin = spice.cell_double(40000)

    spice.gfoclt(occtyp, front_body, 'ELLIPSOID', fb_frame, back_body, 'ELLIPSOID', bb_frame, abcorr, 'JUICE',
                 step, cnfine, riswin)

    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.info(f'No {back_body} transits were found for {front_body}.')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'{back_body} occultation by {front_body}')
            logging.info('-----------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info(f'Method:             {method}')
            logging.info(f'Front Body Name:    {front_body}')
            logging.info(f'Front Body Frame:   {fb_frame}')
            logging.info(f'Observer Name:      {observer}')
            logging.info('-----------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])

        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis


def jovian_system_occultations(utc_start='', utc_end='', interval='', target='ANTARES',
                                system=['JUPITER','IO','EUROPA', 'GANYMEDE', 'CALLISTO','RINGS'],
                                step=600, occtyp='ANY', abcorr='LT+S', verbose=False):
    """
    Geometry Finder function for the Jovian System Occultations.

    This function searches for occultations for the specified target by the Jovian System. The Jovian
    system is a construct that includes the planet Jupiter, its rings and its moons. The system itself
    can be specified as a parameter. The occultations are searched for the specified time interval either
    provided as a SPICE Time Window or as a start and end time in UTC calendar format.

    Parameters
    ----------
    utc_start :  str, optional
        Start time of the interval in UTC format.
    utc_end : str, optional
        End time of the interval in UTC format.
    interval : SPICE Time Window
        Time interval in SPICE Time Window format.
    target : str, optional
        Name of the target body occulted by the Jovian System.
    system : list, optional
        List of the bodies that form the Jovian System specified with their SPICE names.
        (default: ['JUPITER','IO','EUROPA', 'GANYMEDE', 'CALLISTO','RINGS'])
        The list can contain the following bodies:
        - Jupiter: JUPITER. Even it not specified Jupiter is always included in the system but its
          occultations will not be displayed as results (they are used to discriminate occultations hidden
          by Jupiter itself).
        - Moons: The Inner Moons, Galilean Moons, and irregular moons (any Moon available in the SPICE kernels).
        - Rings: You can either specify the Rings as a System (RINGS) or as individual rings. The rings are:
            - Halo Ring: JUICE_JUP_HALO_RING
            - Main Ring: JUICE_JUP_MAIN_RING
            - Gossamer Ring: JUICE_JUP_THE_GOS_RING
            - Amalthea Ring: JUICE_JUP_AMA_RING
            - Thebe Ring Extension: JUICE_JUP_THE_RING_EXT
        (default: ['JUPITER','IO','EUROPA', 'GANYMEDE', 'CALLISTO','RINGS'])
    step : int, optional
        Time step used for searching occultations (default: 600).
    occ_type : str, optional
        Type of occultation to search for (default: ANY).
    abcorr : str, optional
        Aberration correction (default: LT+S).
    verbose : bool, optional
        If True, log information will be generated. (default: False).

    Returns
    -------
    dict
        A dictionary containing the results of the occultation search. The dictionary keys are the
        bodies that form the Jovian System. The values are lists of occultation intervals represented
        as [start_time, end_time] in UTC format.
    """

    # if system is not a list then convert it to a list
    if not isinstance(system, list):
        system = [system]

    if target == 'EARTH':
        occultation = earth_occultations
    elif target == 'SUN':
        occultation = sun_occultations
    else:
        occultation = stellar_occultations

    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    occ_dict = {}

    # 1-Jupiter Occultations
    riswin_jupiter, rislst_jupiter = occultation(interval=cnfine, front_body='JUPITER', fb_frame='IAU_JUPITER',
                                                 star=target, verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
    if 'JUPITER' in system:
        if rislst_jupiter:
            occ_dict['JUPITER'] = rislst_jupiter
        else:
            occ_dict['JUPITER'] = []

    # 2-Moon Occultations
    for moon in system:
        if 'RING' not in moon and moon != 'JUPITER':
            occ_dict[moon.upper()] = []
            cnfine_moon = spice.wndifd(cnfine, riswin_jupiter)
            riswin_moon, rislst_moon = occultation(interval=cnfine_moon, front_body=moon.upper(), fb_frame=f'IAU_{moon.upper()}',
                                                  star=target, verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
            if rislst_moon:
                occ_dict[moon.upper()] = rislst_moon

    # 3-Rings Occultations
    # 3.1-Rings as a System Occultations
    if 'RINGS' in system:
        occ_dict['RINGS'] = []
        cnfine_rings = spice.wndifd(cnfine, riswin_jupiter)
        # 3.1-Thebe Ring Extention Occultations
        riswin_ring_ext, rislst_ring_ext = occultation(interval=cnfine_rings, front_body='JUICE_JUP_THE_RING_EXT',
                                                     fb_frame='JUICE_JUP_THE_RING_EXT', star=target,
                                                     verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        cnfine_rings_ext = spice.wndifd(cnfine_rings, riswin_ring_ext)
        # 3.2-Halo Ring Occultations
        riswin_ring_halo, rislst_ring_halo = occultation(interval=cnfine_rings_ext, front_body='JUICE_JUP_HALO_RING',
                                                       fb_frame='JUICE_JUP_HALO_RING', star=target,
                                                       verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.3-Rings Boundary Occultations
        riswin_ring_bound, rislst_ring_bound = occultation(interval=cnfine_rings, front_body='JUICE_JUP_RING_BOUNDARY',
                                                         fb_frame='JUICE_JUP_RING_BOUNDARY', star=target,
                                                         verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.4-Rings Boundary Substraction
        riswin_rings = spice.wnunid(riswin_ring_halo, riswin_ring_ext)
        riswin_rings = spice.wndifd(riswin_rings, riswin_ring_bound)
        rislst_rings = win2lst(riswin_rings)

        if rislst_rings:
            occ_dict['RINGS'] = rislst_rings

    # 3.2-Individual Rings Occultations
    #     ~ - ,
    #           ' ,
    #               ,     _________
    #                ,   |         |___________________________________________
    #                 ,  |         |________________  Amalthea    | Thebe      |Thebe
    #     Jupiter     ,  |         |==== Main Ring  | Gossamer    | Gossamer   |Ring
    #                 ,  |         |----------------' Ring        | Ring       |Ext
    #                ,   |         |------------------------------'------------'
    #               ,    '---------'
    #            , '      Halo Ring
    #     _ ,  '
    # 3.2.1-Thebe Ring Extention Occultations
    elif 'JUICE_JUP_THE_RING_EXT' in system:
        cnfine_ring = spice.wndifd(cnfine, riswin_jupiter)
        riswin_ring, rislst_moon = occultation(interval=cnfine_ring, front_body='JUICE_JUP_THE_RING_EXT',
                                                fb_frame='JUICE_JUP_THE_RING_EXT',
                                                star=target, verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)

        riswin_ring_bound, rislst_ring_bound = occultation(interval=cnfine_ring, front_body='JUICE_JUP_THE_GOS_RING',
                                                           fb_frame='JUICE_JUP_THE_GOS_RING', star=target,
                                                           verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.4-Rings Boundary Substraction
        riswin_ring = spice.wndifd(riswin_ring, riswin_ring_bound)
        rislst_ring = win2lst(riswin_ring)

        if rislst_ring:
            occ_dict['JUICE_JUP_THE_RING_EXT'] = rislst_ring
        else:
            occ_dict['JUICE_JUP_THE_RING_EXT'] = []
    # 3.2.2.-Thebe Gossamer Ring Occultations
    elif 'JUICE_JUP_THE_GOS_RING' in system:
        cnfine_ring = spice.wndifd(cnfine, riswin_jupiter)
        riswin_ring, rislst_moon = occultation(interval=cnfine_ring, front_body='JUICE_JUP_THE_GOS_RING',
                                                fb_frame='JUICE_JUP_THE_GOS_RING',
                                                star=target, verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)

        riswin_ring_bound, rislst_ring_bound = occultation(interval=cnfine_ring, front_body='JUICE_JUP_AMA_GOS_RING',
                                                           fb_frame='JUICE_JUP_AMA_GOS_RING', star=target,
                                                           verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.4-Rings Boundary Substraction
        riswin_ring = spice.wndifd(riswin_ring, riswin_ring_bound)
        rislst_ring = win2lst(riswin_ring)

        if rislst_ring:
            occ_dict['JUICE_JUP_THE_RING_EXT'] = rislst_ring
        else:
            occ_dict['JUICE_JUP_THE_RING_EXT'] = []
    # 3.2.3.-Amalthea Gossamer Ring Occultations
    elif 'JUICE_JUP_AMA_GOS_RING' in system:
        cnfine_ring = spice.wndifd(cnfine, riswin_jupiter)
        riswin_ring, rislst_moon = occultation(interval=cnfine_ring, front_body='JUICE_JUP_AMA_GOS_RING',
                                                fb_frame='JUICE_JUP_AMA_GOS_RING',
                                                star=target, verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)

        riswin_ring_bound, rislst_ring_bound = occultation(interval=cnfine_ring, front_body='JUICE_JUP_HALO_RING',
                                                           fb_frame='JUICE_JUP_HALO_RING', star=target,
                                                           verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.4-Rings Boundary Substraction
        riswin_ring = spice.wndifd(riswin_ring, riswin_ring_bound)
        rislst_ring = win2lst(riswin_ring)

        if rislst_ring:
            occ_dict['JUICE_JUP_AMA_GOS_RING'] = rislst_ring
        else:
            occ_dict['JUICE_JUP_AMA_GOS_RING'] = []
    # 3.2.4.-Main Ring Occultations
    elif 'JUICE_JUP_MAIN_RING' in system:
        cnfine_ring = spice.wndifd(cnfine, riswin_jupiter)
        riswin_ring, rislst_moon = occultation(interval=cnfine_ring, front_body='JUICE_JUP_MAIN_RING',
                                                fb_frame='JUICE_JUP_MAIN_RING',
                                                star=target, verbose=verbose, step=step, abcorr=abcorr)

        riswin_ring_bound, rislst_ring_bound = occultation(interval=cnfine_ring, front_body='JUICE_JUP_HALO_RING',
                                                           fb_frame='JUICE_JUP_HALO_RING', star=target,
                                                           verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.4-Rings Boundary Substraction
        riswin_ring = spice.wndifd(riswin_ring, riswin_ring_bound)
        rislst_ring = win2lst(riswin_ring)

        if rislst_ring:
            occ_dict['JUICE_JUP_MAIN_RING'] = rislst_ring
        else:
            occ_dict['JUICE_JUP_MAIN_RING'] = []
    # 3.2.4.-Halo Ring Occultations
    elif 'JUICE_JUP_HALO_RING' in system:
        cnfine_ring = spice.wndifd(cnfine, riswin_jupiter)
        riswin_ring, rislst_moon = occultation(interval=cnfine_ring, front_body='JUICE_JUP_HALO_RING',
                                                fb_frame='JUICE_JUP_HALO_RING',
                                                star=target, verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)

        riswin_ring_bound, rislst_ring_bound = occultation(interval=cnfine_ring, front_body='JUICE_JUP_RING_BOUNDARY',
                                                           fb_frame='JUICE_JUP_RING_BOUNDARY', star=target,
                                                           verbose=verbose, step=step, occtyp=occtyp, abcorr=abcorr)
        # 3.4-Rings Boundary Substraction
        riswin_ring = spice.wndifd(riswin_ring, riswin_ring_bound)
        rislst_ring = win2lst(riswin_ring)

        if rislst_ring:
            occ_dict['JUICE_JUP_HALO_RING'] = rislst_ring
        else:
            occ_dict['JUICE_JUP_HALO_RING'] = []

    return occ_dict


def jupiter_minor_moons_transits(utc_start='', utc_end='', step=60,
                                 minor_moons=None, verbose=False):
    """
    Get transit windows for Jupiter's minor moons.

    Parameters
    ----------
    utc_start : str, optional
        Start time in UTC string format (default: '').
    utc_end : str, optional
        End time in UTC string format (default: '').
    step : int, optional
        Step size for interval checks (default: 60).
    minor_moons : list or None, optional
        List of minor moons to consider (default: ['AMALTHEA', 'THEBE', 'ADRASTEA', 'METIS']).
    verbose : bool, optional
        Verbosity flag (default: False).

    Returns
    -------
    dict
        Dictionary containing transit windows for each minor moon.
    """
    if minor_moons is None:
        minor_moons = ['AMALTHEA', 'THEBE', 'ADRASTEA', 'METIS']

    minor_moons_transits = {}
    for moon in minor_moons:

        riswin, rislis = transits(utc_start=utc_start, utc_end=utc_end,
                                  step=step,
                                  method='ELLIPSOID',
                                  front_body=moon.upper(),
                                  fb_frame=f'IAU_{moon.upper()}',
                                  observer='JUICE',
                                  back_body='JUPITER',
                                  bb_frame='IAU_JUPITER',
                                  verbose=verbose)

        minor_moons_transits[moon.upper()] = riswin

    return minor_moons_transits


def jupiter_minor_moons_occultations(utc_start='', utc_end='', step=60,
                                   minor_moons=None, verbose=False):
    """
    Get occultation windows for Jupiter's minor moons.

    Parameters
    ----------
    utc_start : str, optional
        Start time in UTC string format (default: '').
    utc_end : str, optional
        End time in UTC string format (default: '').
    step : int, optional
        Step size for interval checks (default: 60).
    minor_moons : list or None, optional
        List of minor moons to consider (default: ['AMALTHEA', 'THEBE', 'ADRASTEA', 'METIS']).
    verbose : bool, optional
        Verbosity flag (default: False).

    Returns
    -------
    dict
        Dictionary containing occultation windows for each minor moon.
    """
    if minor_moons is None:
        minor_moons = ['AMALTHEA', 'THEBE', 'ADRASTEA', 'METIS']

    minor_moons_occs = {}
    for moon in minor_moons:

        # Discard the periods where the moon is behind Jupiter. We chose
        # a full occultation not to prevent the start of the transit to be
        # excluded.
        riswin, rislis = transits(utc_start=utc_start, utc_end=utc_end,
                                  step=step,
                                  method='ELLIPSOID',
                                  front_body='JUPITER',
                                  fb_frame='IAU_JUPITER',
                                  observer='JUICE',
                                  back_body=moon.upper(),
                                  bb_frame=f'IAU_{moon.upper()}',
                                  occtyp='FULL',
                                  verbose=verbose)

        minor_moons_occs[moon.upper()] = riswin

    return minor_moons_occs


def solar_conjunction(utc_start='', utc_end='',
                      interval=False, step=600,
                      observer='JUICE',
                      observer_frame='JUICE_SPACECRAFT',
                      conj_degrees=3,
                      abcorr='NONE',
                      verbose=False):
    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    nintvls = 40000
    adjust = 0.0
    riswin = spice.cell_double(40000)

    spice.gfsep(targ1='SUN',
                shape1='POINT',
                inframe1='IAU_SUN',
                targ2=observer,
                shape2='POINT',
                inframe2=observer_frame,
                abcorr='NONE',
                obsrvr='EARTH',
                relate='<',
                refval=conj_degrees * spice.rpd(),
                step=step,
                nintvls=nintvls,
                adjust=adjust,
                cnfine=cnfine,
                result=riswin)

    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.info(f'No Solar Conjunctions were found for {observer}.')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'{observer} Solar Conjunctions')
            logging.info('-----------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info('-----------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])

        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis


def juice_distance(utc_start='', utc_end='',
                 interval=False, step=600,
                 target='SUN',
                 observer='JUICE',
                 verbose=False,
                 abcorr='NONE',
                 relation='>',
                 distance=1.34,
                 distance_unit='AU',
                 is_altitude=False):

    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval


    if relation in ['ABSMIN', 'ABSMAX', 'LOCMAX', 'LOCMIN']:
        distance = ''
        distance_unit = ''
        distance_km = 0
    else:
        distance_km = spice.convrt(distance, distance_unit, 'KM' )
        if is_altitude:
            id = spice.bodn2c(target.upper())
            radii = spice.gdpool(f"BODY{id}_RADII", 0, 3)
            distance_km += radii[0]

    nintvls = 40000
    adjust = 0.0
    riswin = spice.cell_double(nintvls)

    spice.gfdist(target,
                 abcorr,
                 observer,
                 relation,
                 distance_km,
                 adjust,
                 step,
                 nintvls,
                 cnfine,
                 riswin)

    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.warning(f'No {target} distance range for {observer}.')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'{observer}-{target} distance is {relation} {distance} {distance_unit}')
            logging.info('------------------------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info('-----------------------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])
        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis


def juice_position(utc_start='', utc_end='',
                 interval=False, step=600,
                 target='GANYMEDE',
                 frame='IAU_GANYMEDE',
                 observer='JUICE',
                 verbose=False,
                 abcorr='NONE',
                 coordinate_system = 'RECTANGULAR',
                 coordinate = 'Z',
                 relation='=',
                 distance=0,
                 distance_unit='km',
                 is_altitude=False):

    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval


    if relation in ['ABSMIN', 'ABSMAX', 'LOCMAX', 'LOCMIN']:
        distance = ''
        distance_unit = ''
        distance_km = 0
    else:
        distance_km = spice.convrt(distance, distance_unit, 'KM' )
        if is_altitude:
            id = spice.bodn2c(target.upper())
            radii = spice.gdpool(f"BODY{id}_RADII", 0, 3)
            distance_km += radii[0]

    nintvls = 40000
    adjust = 0.0
    riswin = spice.cell_double(nintvls)

    spice.gfposc(target,
                 frame,
                 abcorr,
                 observer,
                 coordinate_system,
                 coordinate,
                 relation,
                 distance_km,
                 adjust,
                 step,
                 nintvls,
                 cnfine,
                 riswin)

    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.warning(f'No {target} position range for {observer}.')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'{observer}-{target} position is {coordinate} {relation} {distance} {distance_unit}')
            logging.info('------------------------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info('-----------------------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])
        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis



def terminator_crossing(utc_start='', utc_end='',
                        interval=False, step=600,
                        target='MOON',
                        verbose=False,
                        abcorr='NONE'):
    if not interval:
        et_start = spice.utc2et(utc_start)
        et_stop = spice.utc2et(utc_end)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_stop, cnfine)
    else:
        cnflst = win2lst(interval, verbose=False)
        utc_start = spice.et2utc(min(cnflst)[0], 'ISOC', 0, 70)
        utc_end = spice.et2utc(max(cnflst)[-1], 'ISOC', 0, 70)
        cnfine = interval

    maxlen = 40000
    adjust = 0.0
    riswin = spice.cell_double(maxlen)


    @spice.utils.callbacks.SpiceUDFUNS
    def gfq(et):
        juice_pos, _ = spice.spkpos('JUICE', et, 'J2000', abcorr, target)
        sun_pos, _ = spice.spkpos('SUN', et, 'J2000', abcorr, target)
        ang = spice.vsep(juice_pos,sun_pos) * spice.dpr()
        if ang > 90:
            return -1 * et
        return et

    @spice.utils.callbacks.SpiceUDFUNB
    def gfdecrx(udfuns, et):
        return spice.uddc(udfuns, et, 10)

    spice.gfuds(gfq, gfdecrx, '=', 0, adjust, step, 20000, cnfine, riswin)


    # The function wncard returns the number of intervals
    # in a SPICE window.
    winsiz = spice.wncard(riswin)

    # Define the list of events.
    rislis = []

    if winsiz == 0 and verbose:
        logging.warning(f'JUICE not crossing the {target} terminator')
    else:
        # Display the visibility time periods.
        if verbose:
            logging.info('')
            logging.info(f'JUICE crossing the {target} terminator')
            logging.info('------------------------------------------------------')
            logging.info(f'Interval start:     {utc_start}')
            logging.info(f'Interval end:       {utc_end}')
            logging.info(f'Step [s]:           {step}')
            logging.info('-----------------------------------------------------')

        for i in range(winsiz):
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            [intbeg, intend] = spice.wnfetd(riswin, i)

            # Convert the time to a UTC calendar string.
            timstr_beg = spice.et2utc(intbeg, 'ISOC', 0, 70)
            timstr_end = spice.et2utc(intend, 'ISOC', 0, 70)
            duration = intend - intbeg

            # Write the string to standard output.
            if verbose:
                logging.info(f'{timstr_beg} - {timstr_end}: {sec2hhmmss(duration)}')

            rislis.append([intbeg, intend])
        if verbose:
            logging.info('-----------------------------------------------------')
            logging.info(f'Number of results: {len(rislis)}')
            logging.info('')

    return riswin, rislis