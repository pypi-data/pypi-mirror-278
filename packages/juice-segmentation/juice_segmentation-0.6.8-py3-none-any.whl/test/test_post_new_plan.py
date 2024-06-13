"""
Created on July, 2022

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle SHT rest-api

"""
import logging


from juice_segmentation.commons.sht_rest_api import post_plans, upload_plan

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

    new_plan = '../test_files/segmentation_proposal_crema_5_0_all.json'
    upload_plan(new_plan)

    # "curl -X GET "https://juicesoc.esac.esa.int/rest_api/trajectory/CREMA_3_0/segment_definition" -H  "accept: application/json

    logging.info('End test!')

