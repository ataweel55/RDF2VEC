# import modules; set up logging
import gensim, logging, os, sys, gzip
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',filename='word2vec.out', level=logging.INFO)


class MySentences(object):
	def __init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
		for fname in os.listdir(self.dirname):
			try:
				for line in gzip.open(os.path.join(self.dirname, fname), mode='rt'):
					line = line.rstrip('\n')
					words = line.split(" ")
					yield words
			except Exception:
				print("Failed reading file:")
				print(fname)


sentences = MySentences(WalksData) # a memory-friendly iterator
#sg 500
model = gensim.models.Word2Vec(size=500, workers=5, window=10, sg=1, negative=15, iter=5)
model.build_vocab(sentences)
model.train(sentences)
#sg/cbow features iterations window negative hops random walks
model.save('DB2Vec_sg_500_5_5_15_2_500')

#sg 200
model1 = gensim.models.Word2Vec(size=200, workers=5, window=5, sg=1, negative=15, iter=5)
model1.reset_from(model)


#cbow 500
model2 = gensim.models.Word2Vec(size=500, workers=5, window=5, sg=0, iter=5, cbow_mean=1, alpha = 0.05)
model2.reset_from(model)


#cbow 200
model3 = gensim.models.Word2Vec(size=200, workers=5, window=5, sg=0, iter=5, cbow_mean=1, alpha = 0.05)
model3.reset_from(model)

del model

model1.train(sentences)
model1.save('DB2Vec_sg_200_5_5_15_2_500')

del model1

model2.train(sentences)
model2.save('DB2Vec_cbow_500_5_5_2_500')

del model2

model3.train(sentences)
model3.save('DB2Vec_cbow_200_5_5_2_500')
