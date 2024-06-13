"""
Created on Jun 2023

@author: Claudio Munoz Crego (ESAC)

This Module is a containers for function allowing to handle
segment opportunity to prime segment renaming
"""

import copy
import fnmatch
import logging


def seg_opportunity_2_prime_seg(wgx, opportunity_vs_prime):
    """
    Rename segment opportunities to prime segment names when defined.

    Note:
    - if not defined (i.e. DL_) maintain the old name.
    - if partial mapping:
        - JUPITER_PERIJOVE renamed as specified
        - Correspond to PRIME _xx as for instance GANYMEDE_GM renamed as specified

    :param opportunity_vs_prime: mapping segment opportunity - prime segment
    :param wgx: Working Group segments
    :return:
    """

    for wg in wgx:

        new_wgx = {wg: {}}
        opportunity_vs_prime_keys = opportunity_vs_prime[wg].keys()

        for seg in wgx[wg]:

            # First looking for exact mapping
            if seg in opportunity_vs_prime_keys:

                opp_seg_prime_name = opportunity_vs_prime[wg][seg]
                new_seg = seg.replace(seg, opp_seg_prime_name)
                logging.debug(f'Mapping: Segment Opportunity {seg} -- to Prime --> {opp_seg_prime_name}')

                if new_seg in list(new_wgx[wg].keys()):
                    new_wgx[wg][new_seg].extend(wgx[wg][seg])
                else:
                    new_wgx[wg][new_seg] = copy.copy(wgx[wg][seg])

            else:  # Next looking for partial mapping

                seg_mapped = False  # a flag to only update renamed seg

                for opp_seg_name in opportunity_vs_prime_keys:

                    if opp_seg_name in seg:

                        opp_seg_prime_full_name = opportunity_vs_prime[wg][opp_seg_name]

                        if opp_seg_name == 'JUPITER_PERIJOVE':
                            opp_seg_prime_name = opp_seg_prime_full_name.split('_PExx')[0]
                            new_seg = seg.replace(opp_seg_name, opp_seg_prime_name)
                            logging.debug(f'Perijove: Segment Opportunity {seg} -- to Prime --> {new_seg}')
                            new_wgx[wg][new_seg] = wgx[wg][seg]
                            seg_mapped = True
                            break

                        elif '_xx' in opp_seg_prime_full_name:
                            opp_seg_prime_name = opp_seg_prime_full_name.split('_xx')[0]
                            new_seg = seg.replace(opp_seg_name, opp_seg_prime_name)
                            logging.debug(f'Partial Mapping: Segment Opportunity {seg} -- to Prime --> {new_seg}')
                            new_wgx[wg][new_seg] = wgx[wg][seg]
                            seg_mapped = True
                            break

                    elif fnmatch.fnmatch(seg, opp_seg_name):
                        opp_seg_prime_name = opportunity_vs_prime[wg][opp_seg_name]
                        new_seg = opp_seg_prime_name
                        logging.info(f'Wild-card Mapping: Segment Opportunity {seg} -- to Prime --> {new_seg}')
                        new_wgx[wg][new_seg] = wgx[wg][seg]
                        seg_mapped = True
                        break

                if not seg_mapped:
                    new_wgx[wg][seg] = wgx[wg][seg]
                    if not str(seg).startswith('OPNAV_') and not is_prime_segment(wg, seg, opportunity_vs_prime):
                        logging.info(f'No PRIME defined for Segment {seg}')

        wgx[wg] = new_wgx[wg]

    return wgx


def reset_opportunity_2_prime_seg_mapping_using_wild_card(wgx, opportunity_vs_prime):
    """
    Check if there are opportunity segments mapping with wild_card,
    and add them to the mapping

    :param opportunity_vs_prime: mapping segment opportunity - prime segment
    :param wgx: Working Group segments
    :return:
    """

    for wg in wgx:

        opportunity_vs_prime_keys = sorted(opportunity_vs_prime[wg].keys())

        for seg in wgx[wg]:

            if seg not in opportunity_vs_prime_keys:

                for opp_seg_name in opportunity_vs_prime_keys:

                    if fnmatch.fnmatch(seg, opp_seg_name):
                        opp_seg_prime_name = opportunity_vs_prime[wg][opp_seg_name]
                        logging.info(f'Wild-card added to Mapping: Segment Opportunity {seg}'
                                     f' -- to Prime --> {opp_seg_prime_name}')
                        opportunity_vs_prime[wg][seg] = opp_seg_prime_name  # add this mapping
                        break

    return opportunity_vs_prime


def is_prime_segment(wg, seg, opportunity_vs_prime):
    """
    Check if segment is already a prime segment

    :param wg: working group name
    :param seg: segment name
    :param opportunity_vs_prime: mapping segment opportunity - prime segment
    """

    primes = [v.replace('xx', '*') for v in opportunity_vs_prime[wg].values()]

    for prime in primes:

        if fnmatch.fnmatch(seg, prime):
            return True

    return False





