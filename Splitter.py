import random
import sys

sentences_filename = sys.argv[1]
indices_filename = sys.argv[2]
sentences_file = open(sentences_filename + '.txt', 'r')
indices_file = open(indices_filename + '.txt', 'r')
sentences = sentences_file.readlines()
indices = indices_file.readlines()
sentences_file.close()
indices_file.close()
dataset = zip(sentences, indices)
random.seed(55)
random.shuffle(dataset)

border = int(0.7 * len(dataset))
train_dataset = dataset[:border]
dev_dataset = dataset[border:]

sentences_train_file = open(sentences_filename + '_train.txt', 'w')
indices_train_file = open(indices_filename + '_train.txt', 'w')
sentences_train_file.writelines(map(lambda x: x[0], train_dataset))
indices_train_file.writelines(map(lambda x: x[1], train_dataset))
sentences_train_file.close()
indices_train_file.close()

sentences_dev_file = open(sentences_filename + '_dev.txt', 'w')
indices_dev_file = open(indices_filename + '_dev.txt', 'w')
sentences_dev_file.writelines(map(lambda x: x[0], dev_dataset))
indices_dev_file.writelines(map(lambda x: x[1], dev_dataset))
sentences_dev_file.close()
indices_dev_file.close()
