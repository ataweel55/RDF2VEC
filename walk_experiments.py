from class_n3_parser import generate_subject_predicate_object_dict
from new_generatewalks import generate_random_walks
import weigher
import gzip
import inspect


# writing method
def write_to_gz(generator):
    cframe = inspect.currentframe()
    func = inspect.getframeinfo(cframe.f_back).function
    output_file = "outputs/" + func + "_" + str(number_of_walks_per_resource) + "_" + str(depth) + ".txt.gz"
    f = gzip.open(output_file, 'wb')
    for t in generator:
        f.write(' '.join(str(x) for x in t).encode("utf-8") + '\n'.encode("utf-8"))
    f.close()


# parameters
kg = "data/mappingbased_objects_en.ttl"
page_rank_file = "data/pageranks_sorted_without_id.csv"
click_stream_file = "data/clickstream-enwiki-2017-11.tsv"
number_of_walks_per_resource = 250
depth = 8
# parsing the graph
sub_pred_obj_dict, node_dict, edge_weight_dict = generate_subject_predicate_object_dict(kg)


def uniform_weight():
    # weighting and normalization
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def predicate_frequency_weight():
    weigher.freq_predicate(sub_pred_obj_dict, edge_weight_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_predicate_frequency_weight():
    weigher.freq_predicate(sub_pred_obj_dict, edge_weight_dict)
    weigher.inverse_freq(edge_weight_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def predicate_object_frequency_weight():
    weigher.freq_predicate_object(sub_pred_obj_dict, edge_weight_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_predicate_object_frequency_weight():
    weigher.freq_predicate_object(sub_pred_obj_dict, edge_weight_dict)
    weigher.inverse_freq(edge_weight_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def object_frequency_weight():
    object_frequency = weigher.freq_object(sub_pred_obj_dict)
    weigher.push_down(edge_weight_dict, object_frequency)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_object_frequency_weight():
    object_frequency = weigher.freq_object(sub_pred_obj_dict)
    weigher.inverse_freq(object_frequency)
    weigher.push_down(edge_weight_dict, object_frequency)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_object_frequency_split_weight():
    object_frequency = weigher.freq_object(sub_pred_obj_dict)
    weigher.inverse_freq(object_frequency)
    weigher.split_down(edge_weight_dict, object_frequency, node_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def page_rank_weight():
    page_rank = weigher.pagerank_dict(page_rank_file)
    weigher.push_down(edge_weight_dict, page_rank)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_page_rank_weight():
    page_rank = weigher.pagerank_dict(page_rank_file)
    weigher.inverse_freq(page_rank)
    weigher.push_down(edge_weight_dict, page_rank)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def page_rank_split_weight():
    page_rank = weigher.pagerank_dict(page_rank_file)
    weigher.split_down(edge_weight_dict, page_rank, node_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_page_rank_split_weight():
    page_rank = weigher.pagerank_dict(page_rank_file)
    weigher.inverse_freq(page_rank)
    weigher.split_down(edge_weight_dict, page_rank, node_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def click_stream_weight():
    weigher.click_stream_weigher(click_stream_file, edge_weight_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def inverse_click_stream_weight():
    weigher.click_stream_weigher(click_stream_file, edge_weight_dict)
    weigher.inverse_freq(edge_weight_dict)
    weigher.normalization(edge_weight_dict, node_dict)
    generator = generate_random_walks(sub_pred_obj_dict, node_dict, edge_weight_dict, number_of_walks_per_resource, depth)
    write_to_gz(generator)


def experiment_number(argument):
    switcher = {
        1: uniform_weight,
        2: predicate_frequency_weight,
        3: inverse_predicate_frequency_weight,
        4: predicate_object_frequency_weight,
        5: inverse_predicate_object_frequency_weight,
        6: object_frequency_weight,
        7: inverse_object_frequency_weight,
        8: inverse_object_frequency_split_weight,
        9: page_rank_weight,
        10: inverse_page_rank_weight,
        11: page_rank_split_weight,
        12: inverse_page_rank_split_weight,
        13: click_stream_weight,
        14: inverse_click_stream_weight
    }
    func = switcher.get(argument, lambda: "Invalid experiment number")
    func()


# experiment_number(9)
# experiment_number(11)
experiment_number(13)
# experiment_number(14)
# for i in range(13):
# experiment_number(10)
# experiment_number(13)
# write_to_gz(uniform_weight())
