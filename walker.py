from collections import defaultdict
import random


def __remove_objects_resulting_in_cycle(possible_preds, seen_nodes):
    new_set = set()
    for predicate in possible_preds:
        obj = predicate.split('>')[2]
        if obj not in seen_nodes:
            new_set.add(predicate)
    return new_set


def __get_next_pred_obj(edge_weight_dict, node_dict, current_resource, seen_nodes):
    # possible_preds is the same as out edges
    possible_preds = node_dict[current_resource][2]
    possible_preds = __remove_objects_resulting_in_cycle(possible_preds, seen_nodes)
    if not possible_preds:
        return None
    possible_edges_weight = {k: edge_weight_dict[k] for k in possible_preds}
    return sorted(possible_edges_weight, key=possible_edges_weight.get, reverse=True)


def __distribute_amount_of_walks(elements, amount_of_walks):
    amount_of_walks_for_every_predicate = amount_of_walks - 1

    predicate_to_amount_of_walks = {predicate: amount_of_walks_for_every_predicate for predicate in elements} \
        if amount_of_walks_for_every_predicate > 0 else defaultdict(int)
    return predicate_to_amount_of_walks


def __edge_into_pred_obj(edge):
    chosen_predicate = edge.split('>')[1]
    chosen_object = edge.split('>')[2]
    return chosen_predicate, chosen_object


def __select_edge(edge_weight_dict, node_dict, current_resource):
    r = random.random()
    # possible_preds is the same as out edges
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


