'''
Created on Feb 16, 2016

@author: petar
'''
import gensim, logging, os, sys


model = gensim.models.Word2Vec.load('DB2Vec_sg_500_5_5_15_2_500')

print ('dbr:Rocky')
print (model.most_similar(positive=['dbr:Rocky'], topn=100))

print ('dbr:Bambi')
print (model.most_similar(positive=['dbr:Bambi'], topn=100))

print ('dbr:Batman_&_Robin_(film)')
print (model.most_similar(positive=['dbr:Batman_&_Robin_(film)'], topn=100))

print ('dbr:Germany')
print (model.most_similar(positive=['dbr:Germany'], topn=100))

print ('dbr:Google')
print (model.most_similar(positive=['dbr:Google'], topn=100))

print ('dbr:Facebook')
print (model.most_similar(positive=['dbr:Facebook'], topn=100))


print ('dbr:MKD')
print (model.most_similar(positive=['dbr:Macedonia'], topn=100))

print ('dbr:Mannheim')
print (model.most_similar(positive=['dbr:Mannheim'], topn=100))

print ('dbr:Barack_Obama')
print (model.most_similar(positive=['dbr:Barack_Obama'], topn=100))

print('dbr:Ford_Torino')
print (model.most_similar(positive=['dbr:Ford_Torino'], topn=100))

print('dbr:dbr:Vietnam_War')
print (model.most_similar(positive=['dbr:Vietnam_War'], topn=100))

