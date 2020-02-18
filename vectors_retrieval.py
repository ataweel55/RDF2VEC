from gensim.models import KeyedVectors, Word2Vec
import pandas as pd
import codecs
# import gensim


model = Word2Vec.load("C:/models/uniform_weight/model 200 5_5_25_200_4_with_duplicats/DB2Vec_sg_200_5_5_15_2_200")
# model = KeyedVectors.load_word2vec_format("C:/models/model.bin", binary=True)
wv = model.wv
# wv = KeyedVectors.load('DB2Vec_sg_500_5_5_15_4_500', mmap='r')
# vector = wv['http://dbpedia.org/resource/Damascus']
# print(vector)


gold_file = 'C:/recommender system/LODrecsys-datasets-master/Movielens1M/MappingMovielens2DBpedia-1.2.tsv'
fields = ['DBpedia_URI15']
gold = pd.read_csv(gold_file, "\t", encoding='latin1')
vectors = gold.iloc[ : , 2 ].values.tolist()
dict_s = {}

f = codecs.open("C:/recommender system/LODrecsys-datasets-master/Movielens1M/uniform_200_200v_4d_Movielens.txt", "w", "utf8")
i = 0
for vector in vectors:
    try:
        f.write(vector + "\t" + "\t".join(str(x) for x in wv[vector]) + '\n')
    except KeyError:
        i += 1
print(i)
f.close()
