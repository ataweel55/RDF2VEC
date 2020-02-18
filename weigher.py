from collections import defaultdict
import codecs
import logging
logger = logging.getLogger(__name__)


def freq_object(sub_pred_obj_dict):
    logger.info("====initialize weighting====")
    absolute_freq_obj = defaultdict(float)
    for key in sub_pred_obj_dict:
        for pre in sub_pred_obj_dict[key]:
            for obj in sub_pred_obj_dict[key][pre]:
                absolute_freq_obj[obj] += 1
    return absolute_freq_obj


def freq_predicate(sub_pred_obj_dict, edge_weight_dict):
    logger.info("====initialize weighting====")
    absolute_freq_pre = defaultdict(float)
    for key in sub_pred_obj_dict:
        for pre in sub_pred_obj_dict[key]:
            absolute_freq_pre[pre] += 1
    for edge in edge_weight_dict:
        var_pred = edge.split('>')[1]
        tmp_weight_var = absolute_freq_pre[var_pred]
        edge_weight_dict[edge] = tmp_weight_var


def freq_predicate_object(sub_pred_obj_dict, edge_weight_dict):
    logger.info("====initialize weighting====")
    absolute_freq = defaultdict(float)
    for key in sub_pred_obj_dict:
        for pre in sub_pred_obj_dict[key]:
            for obj in sub_pred_obj_dict[key][pre]:
                po = pre + ">" + obj
                absolute_freq[po] += 1
    for edge in edge_weight_dict:
        edge_weight_dict[edge] = absolute_freq[edge.split('>')[1] + ">" + edge.split('>')[2]]


def normalization(edge_weight_dict, node_dict):
    new_edge_wieght_dict = defaultdict(float)
    for key in edge_weight_dict:
        current_resource = key.split('>')[0]
        out_edges = node_dict[current_resource][2]
        total_weight = 0
        for edge in out_edges:
            total_weight += edge_weight_dict[edge]
        for edge in out_edges:
            normalized_weight = edge_weight_dict[edge] / total_weight
            new_edge_wieght_dict[edge] = normalized_weight
    edge_weight_dict.clear()
    edge_weight_dict.update(new_edge_wieght_dict)


def inverse_freq(absolute_freq):
    for key in absolute_freq:
        tmp_var = absolute_freq[key]
        tmp_var = 1.0/tmp_var
        absolute_freq[key] = tmp_var


def push_down(edge_weight_dict, node_weight_dict, default_value=0.2):
    for edge in edge_weight_dict:
        chosen_object = edge.split('>')[2]
        if chosen_object in node_weight_dict.keys():
            edge_weight_dict[edge] = node_weight_dict[chosen_object]
        else:
            edge_weight_dict[edge] = default_value


def split_down(edge_weight_dict, node_weight_dict, node_dict, default_value=0.2):
    for edge in edge_weight_dict:
        chosen_object = edge.split('>')[2]
        node_in_degree = node_dict[chosen_object][0]
        if chosen_object in node_weight_dict.keys():
            tmp_weight = node_weight_dict[chosen_object]/node_in_degree
            edge_weight_dict[edge] = tmp_weight
        else:
            edge_weight_dict[edge] = default_value/node_in_degree


def pagerank_dict(path="data/pageranks_sorted_without_id.csv"):
    logger.info("====initialize weighting====")
    page_rank_dict = defaultdict(float)
    f = codecs.open(path, "r", "utf8")
    for line in f:
        if line.startswith("#"):
            continue
        try:
            line = line.rstrip('\n').rstrip('\r')
            tokens = line.split(",")
            sub = 'http://dbpedia.org/resource/' + tokens[0]
            page_rank_dict[sub] = float(tokens[1])
        except ValueError:
            logger.error("line %s is invalid in pagerank file")
    f.close()
    return page_rank_dict


def click_stream_weigher(path, edge_weight_dict, default_value=0.2):
    logger.info("====initialize weighting====")
    click_stream_dict = defaultdict(float)
    f = codecs.open(path, "r", "utf8")
    for line in f:
        if line.startswith("#"):
            continue
        try:
            line = line.rstrip('\n').rstrip('\r')
            tokens = line.split("\t")
            if tokens[2] == "external":
                continue
            else:
                sub = 'http://dbpedia.org/resource/' + tokens[0]
                obj = 'http://dbpedia.org/resource/' + tokens[1]
                sub_obj = sub + ">" + obj
                click_stream_dict[sub_obj] = float(tokens[3])
        except ValueError:
            logger.error("line %s is invalid in click stream file")
    for edge in edge_weight_dict:
        sub = edge.split('>')[0]
        obj = edge.split('>')[2]
        sub_obj = sub + ">" + obj
        if sub_obj in click_stream_dict:
            edge_weight_dict[edge] = click_stream_dict[sub_obj]
        else:
            edge_weight_dict[edge] = default_value
