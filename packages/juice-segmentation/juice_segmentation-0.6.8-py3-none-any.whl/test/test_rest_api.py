"""
Created on May, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle SHT rest-api

"""
import logging


from juice_segmentation.commons.rest_api import get_segmentation_definition, get_and_create_segmentation_file


def test_get_segmentation_definition():

    url = 'http://localhost:8001/rest_api/trajectory/CREMA_3_0/segment_definition'
    file_name = 'segment_definition.json'

    get_segmentation_definition(url, file_name)


if __name__ == '__main__':

    import os

    from esac_juice_pyutils.commons.my_log import setup_logger

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)

    print(here)
    print(test_dir)

    setup_logger('debug')
    print(os.getcwd())

    print('\n-----------------------------------------------\n')

    logging.info('Start of test ...')

    # get_and_create_segmentation_file(crema='crema_3_0', output_dir='../TDS',
    #                                  url_root='https://juicesoc.esac.esa.int/rest_api/trajectory')

    get_and_create_segmentation_file(crema='crema_3_0', output_dir='../TDS')
    # get_and_create_segmentation_file(crema='crema_4_2b', output_dir='../TDS')

    # "curl -X GET "https://juicesoc.esac.esa.int/rest_api/trajectory/CREMA_3_0/segment_definition" -H  "accept: application/json

    logging.info('End test!')

