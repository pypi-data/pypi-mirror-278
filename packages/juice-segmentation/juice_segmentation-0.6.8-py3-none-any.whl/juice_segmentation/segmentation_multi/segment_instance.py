"""
Created on Sep 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle a segment instance
"""


class SegmentInstance(object):
    """
    Segment Instance
    """

    def __init__(self, wg_name, segment_name, segment_period):

        self.wg = wg_name
        self.segment = segment_name
        self.period = segment_period

    def to_string(self):

        return '{} ; [{} - {}]; {}; '.format(self.wg, self.segment, self.end, self.period)
