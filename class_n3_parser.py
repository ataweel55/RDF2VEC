import codecs
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
                             level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_subject_predicate_object_dict(path):
    with codecs.open(path, 'r', encoding='utf8') as file:
        sub_pred_obj_dict = defaultdict(lambda: defaultdict(list))
        node_dict = defaultdict(lambda: [0, 0, set()])
        edge_weight_dict = defaultdict(float)
        for i, line in enumerate(file):
            # logging the process every 1m line
            if i % 1000000 == 0:
                logger.info("%s line has been read", i)
            if line.startswith("#"):
                continue 
            token = line.split('>')
            try:
                # remove <> from the entity
                sub, pred, obj = [token[0].strip('<>. '), token[1].strip('<>. '), token[2].strip('<>. ')]
                # if token[2].find('"') != -1:
                #     print(i)
                #     continue
                sub_pred_obj_dict[sub][pred].append(obj)
                # out_degree
                node_dict[sub][1] += 1
                # in_degree
                node_dict[obj][0] += 1
                # initialize with uniform weights
                edge_weight_dict[sub + ">" + pred + ">" + obj] = 1
            except IndexError:
                logger.error("line %s is invalid", i)
    logger.info("====end %s line has been read====", i)
    # adding the out edge for every node
    for resource in sub_pred_obj_dict:
        out_edges = set()
        for pred in sub_pred_obj_dict[resource]:
            for obj in sub_pred_obj_dict[resource][pred]:
                out = resource + ">" + pred + ">" + obj
                out_edges.add(out)
        node_dict[resource][2] = out_edges

    return sub_pred_obj_dict, node_dict, edge_weight_dict


# generate_subject_predicate_object_dict("data/mappingbased_objects_en.ttl")
