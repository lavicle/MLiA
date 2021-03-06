import numpy as np


def create_data():
    # just for little test
    posting_list = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                    ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                    ['stop', 'posting', 'worthless', 'stupid', 'garbage'],
                    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                    ['quit', 'buying', 'worthless', 'food', 'dog', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]
    return posting_list, class_vec


def create_vocab_list(data_set):
    vocab = set([])
    for i in data_set:
        vocab = vocab | set(i)
    return list(vocab)


def words_set2vec(vocal, input_set):
    return_vec = [0] * len(vocal)
    for i in input_set:
        if i in vocal:
            return_vec[vocal.index(i)] += 1  # noting the difference with bayes.py
        else:
            print('there is no %s in vocabulary' % i)
    return return_vec


def train_nb0(input_word2vec_set, input_class_set):
    # get the index of each class
    input_word2vec_set = np.matrix(input_word2vec_set)  # m*n, where m is the number of samples, n is the number of fe
    input_class_set = np.matrix(input_class_set)
    class0_index = np.where(input_class_set == 0)[1]  # array
    class1_index = np.where(input_class_set == 1)[1]
    # get the input_data matrix of each class
    input_word2vec0 = input_word2vec_set[class0_index, :]
    input_word2vec1 = input_word2vec_set[class1_index, :]
    # get the token (not sample) number of each class
    m0 = np.sum(input_word2vec0)  # !!! noting the difference with bayes.py and np.sum and sum is different
    m1 = np.sum(input_word2vec1)
    p_true = m1 / (m0 + m1)
    # sum the num of columns(corresponding to feature or token)
    sum0_of_vec0 = np.sum(input_word2vec0,  axis=0)  # where 0 represents 'axis = 0'
    sum0_of_vec1 = np.sum(input_word2vec1, axis=0)
    # number of features or tokens
    num_fea = input_word2vec_set.shape[1]
    # get conditional probabilities
    x_prob_vec0 = np.log((sum0_of_vec0 + 1) / (m0 + num_fea))  # !!!noting the difference with bayes
    x_prob_vec1 = np.log((sum0_of_vec1 + 1) / (m1 + num_fea))  # the plus of 1 or k is to prevent 0 probability
    return x_prob_vec0, x_prob_vec1, p_true


def classify(x_prob_vec0, x_prob_vec1, p_true, test_data):
    # test_data should be single
    test_data = np.asmatrix(test_data)
    # p1 = test_data * x_prob_vec1.T + np.log(p_true)
    # p0 = test_data * x_prob_vec0.T + np.log(p_true)
    # why not multiply those x with test_data = 0 (not showing in the documents)
    # the original codes not fit in with Andrew Wu's two NB codes
    p1 = test_data * (x_prob_vec1).T + (1 - test_data) * (1 - x_prob_vec1).T + np.log(p_true)
    p0 = test_data * (x_prob_vec0).T + (1 - test_data) * (1 - x_prob_vec0).T + np.log(1 - p_true)
    # print(p1)
    # print(p0)
    # p1_exp = np.exp(p1)
    # p0_exp = np.exp(p0)
    # print(p1_exp)
    # print(p0_exp)
    # print("%f, %f" % ((p1_exp)/(p1_exp+p0_exp), p0_exp/(p1_exp+p0_exp)))
    if p0 > p1:
        return 0
    else:
        return 1


# def test_nb():
#     # the little test of the naive bayes
#     input_data_set, input_class_set = create_data()
#     vocal_list = create_vocab_list(input_data_set)
#     output_lists = []
#     for i in range(len(input_class_set)):
#         output_lists.append(words_set2vec(vocal_list, input_data_set[i]))
#     x_prob_vec0, x_prob_vec1, p_true = train_nb0(output_lists, input_class_set)
#     test_entry = ['love', 'my', 'dalmation']
#     test_list = words_set2vec(vocal_list, test_entry)
#     print(classify(x_prob_vec0, x_prob_vec1, p_true, test_list))
#     test_entry = ['stupid', 'garbage']
#     test_list = words_set2vec(vocal_list, test_entry)
#     print(classify(x_prob_vec0, x_prob_vec1, p_true, test_list))
#
#
# test_nb()


def text_parse(email_string):
    import re
    list_tokens = re.split(r'\W', email_string)  # this could generate ''
    return [i.lower() for i in list_tokens if len(i) > 2]


def email2data_list():
    # put email into word/class list
    class_list = []
    words_list = []
    full_list = []
    for i in range(1, 26):
        words = text_parse(open('email/spam/%d.txt' % i).read())
        words_list.append(words)
        class_list.append(1)
        words = text_parse(open('email/ham/%d.txt' % i).read())
        words_list.append(words)
        class_list.append(0)
    return words_list, class_list


def test_nb_full():
    list_words, list_class = email2data_list()
    list_vocal = create_vocab_list(list_words)
    # get random testing index and the other is the training index
    training_index = list(range(50))
    testing_index = []
    for i in range(10):
        index = np.int(np.random.uniform(0, len(training_index)))  # get a index in training_index
        # !!!why we need len(training_set), not 50, since it is changing in the loop
        testing_index.append(training_index[index])  # add the number related to the index to testing_index
        del(training_index[index])  # remove that number related to the index in training_index
    # train
    training_set = []
    training_class = []
    for index in training_index:
        training_set.append(words_set2vec(list_vocal, list_words[index]))
        training_class.append(list_class[index])
    x_prob_vec0, x_prob_vec1, p_true = train_nb0(training_set, training_class)
    # test
    error_count = 0
    for index in testing_index:
        single_test_set = words_set2vec(list_vocal, list_words[index])
        single_result = classify(x_prob_vec0, x_prob_vec1, p_true, single_test_set)
        if single_result != list_class[index]:
            error_count += 1
    print("error rate: %f" % (float(error_count)/len(testing_index)))


test_nb_full()