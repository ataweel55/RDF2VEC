import logging
import random
logger1 = logging.getLogger(__name__)


def __select_edge(edge_weight_dict, node_dict, current_resource):
    r = random.random()
    # possible_preds is the same as out edges for the current node
    out_edges_of_current_node = node_dict[current_resource][2]
    if not out_edges_of_current_node:
        return None, None
    possible_edges_weight = {k: edge_weight_dict[k] for k in out_edges_of_current_node}
    for edge in possible_edges_weight:
        if possible_edges_weight[edge] > r:
            chosen_predicate = edge.split('>')[1]
            chosen_object = edge.split('>')[2]
            return chosen_predicate, chosen_object
        elif possible_edges_weight[edge] < r:
            r = r - possible_edges_weight[edge]


def generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource=40,
                          maximum_length_of_a_walk=8, only_unique_walks=False):
    # sub_pred_obj_dict, node_dict, edge_weight_dict = generate_subject_predicate_object_dict(kg)
    # weigher.normalization(edge_weight_dict, node_dict)
    logger1.info("start the walks")
    subject_count = len(sub_pred_obj_dict.keys())
    total_number_of_walks = 0
    for i, resource in enumerate(sub_pred_obj_dict.keys()):
        walks_per_resource = []
        for k in range(number_of_walks_per_resource):
            current = resource
            one_walk = [current]
            for l in range(maximum_length_of_a_walk):
                (chosen_predicate, chosen_object) = __select_edge(edge_weight_dict, node_dict, current)
                if chosen_predicate is None or chosen_object is None:
                    break
                one_walk.append(chosen_predicate)
                one_walk.append(chosen_object)
                current = chosen_object
            walks_per_resource.append(tuple(one_walk))
        for walk in set(walks_per_resource) if only_unique_walks else walks_per_resource:
            total_number_of_walks += 1
            yield walk

        if i % 100000 == 0:
            logger1.info("%d / %d", i, subject_count)
    logger1.info("done: subject_count %d / total_number_of_walks %d", subject_count, total_number_of_walks)


# test_sample = "data/SmallTest4.nt"
# test_sample = "data/mappingbased_objects_en.ttl"
# f = gzip.open('uniform_200_4-new.txt.gz', 'wb')
# for t in generate_random_walks(test_sample, 200, 4):
#     f.write(' '.join(str(x) for x in t).encode("utf-8") + '\n'.encode("utf-8"))
#     # f.write()
# f.close()
