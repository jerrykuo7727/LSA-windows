# -*- coding: utf-8 -*-
from operator import itemgetter
import math

def HowManyDocsHaveThisTerm(full_docs_wf_list, term_i):
    #對所有doc的word_freq_list計算出每個term各出現在哪些doc
    #full_docs_wf_list的長相 = { 'doc_id': docs, 'word_freq_list': this_doc_word_freq }

    #每個term的長相 = { 'word_id': this_word_id, 'freq': 1, 'appeared_in_doc': filename }
    #先把第一個term放進term_doc_list

    num_of_appearance = 0

    for doc in full_docs_wf_list:
        for walk in doc['word_freq_list']:
            if walk['word_id'] == term_i:
                num_of_appearance = num_of_appearance + 1
    #end for full_docs_wf_list


    return num_of_appearance
#end HowManyDocsAreThisTermIn


def HowManyQuerysHaveThisTerm(full_qrys_wf_list, term_i):
    num_of_appearance = 0

    for qry in full_qrys_wf_list:
        for walk in qry['word_freq_list']:
            if walk['word_id'] == term_i:
                num_of_appearance = num_of_appearance + 1
    #end for full_docs_wf_list


    return num_of_appearance
#end HowManyDocsAreThisTermIn


def F(term_i, document_j, full_docs_wf_list):
    #return 某個term的詞頻
    i = 0
    #先找到對應的document index
    if any(d['doc_id'] == document_j for d in full_docs_wf_list):
         i = map(itemgetter('doc_id'), full_docs_wf_list).index(document_j)

    for search_term in full_docs_wf_list[i]['word_freq_list']:
        if search_term['word_id'] == term_i:
            return search_term['freq']
        #end if
    #end for
    return 0
#end F


def Weight(term_i, document_j, full_docs_wf_list):
    f = F(term_i, document_j, full_docs_wf_list)
    h = HowManyDocsHaveThisTerm(full_docs_wf_list, term_i)

    if h == 0:
        h = 0.00000000000000000000000000000000000000000000000000000001


    if f == 0:
        weight = math.log(2265/h)
    else:
        weight = (1 + math.log(f))*math.log(2265/h)

    if weight > 0:
        return weight
    else:
        return 0
#Weight()


def WeightQ(term_i, query_j, full_qrys_wf_list):
    f = FQ(term_i, query_j, full_qrys_wf_list)
    h = HowManyQuerysHaveThisTerm(full_qrys_wf_list, term_i)

    if h == 0:
        h = 0.00000000000000000000000000000000000000000000000000000001

    if f == 0:
        weight = math.log(2265/h)
    else:
        weight = (1 + math.log(f))*math.log(2265/h)

    if weight > 0:
        return weight
    else:
        return 0
#Weight()
#-----------------------------------------------


def FQ(term_i, query_j, full_qrys_wf_list):
    #return 某個term的詞頻
    i = 0
    if any(d['qry_id'] == query_j for d in full_qrys_wf_list):
        i = map(itemgetter('qry_id'), full_qrys_wf_list).index(query_j)

    for search_term in full_qrys_wf_list[i]['word_freq_list']:
        if search_term['word_id'] == term_i:
            return int(search_term['freq'])
        #end if
    #end for
    return 0
#end F


def CreateQVector(curr_qry_id, query_terms, term_vector, full_qrys_wf_list):
#根據每個query或term, 只要有出現過, 就在term_vector對應的號碼填1
#0不放
    for i in range(0, len(query_terms)):
        #把該query的wiq算出來存在對應的index(word id)上
        term_vector[int(query_terms[i]['word_id'])] = WeightQ(query_terms[i]['word_id'], curr_qry_id, full_qrys_wf_list)
    #end for
    return term_vector
#end CreateVector()


def CreateDVector(curr_doc_id, doc_terms, term_vector, full_docs_wf_list):
#根據每個query或term, 只要有出現過, 就在term_vector對應的號碼填1
#0不放
    for i in range(0, len(doc_terms)):
        #把該document的wiq算出來存在對應的index(word id)上
        index = int(doc_terms[i]['word_id'])
        w = Weight(doc_terms[i]['word_id'], curr_doc_id, full_docs_wf_list)

        #print '....index= {0}, w= {1}'.format(index, w)
        term_vector[index] = w
    #end for
    return term_vector
#end CreateVector()