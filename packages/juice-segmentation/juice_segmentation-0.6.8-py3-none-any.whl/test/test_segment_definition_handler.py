from juice_segmentation.commons.segment_definition_handler import *
from juice_segmentation.commons.rest_api import get_and_create_segmentation_file

if __name__ == '__main__':

    from esac_juice_pyutils.commons.my_log import setup_logger

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)

    setup_logger()

    logging.info('here: {}'.format(here))
    print(test_dir)

    logging.info('Start Test ...')

    get_and_create_segmentation_file(crema='crema_3_0', output_dir='../TDS/JIRA_TEST/SHT_32/input_update')

    input_file = '../TDS/JIRA_TEST/SHT_32/input_update/segment_definition.json'

    segment_handler = SegmentDefinitionHandler(input_file)

    dic = segment_handler.dico

    print(dic.keys())

    get_vs_group = get_map_segment_vs_group(dic)

    print('{} group is {}'.format('G_RS', get_vs_group['G_RS']))

    logging.info('End Test!')

