# -*- coding: utf-8 -*-
import read_doc_query as rd
import os
import vsm_term as t
import math
from operator import itemgetter
import numpy as np




#計算每個term各出現在幾篇文章中, 並存成檔案


def GetTermFreq(type, doc_id, term_id, full_structure_list):
    if type == 'doc' :
        i = map(itemgetter('doc_id'), full_structure_list).index(doc_id)
    elif type == 'query':
        i = map(itemgetter('qry_id'), full_structure_list).index(doc_id)
    #end if doc or query
    j = map(itemgetter('word_id'), full_structure_list[i]['word_freq_list']).index(str(term_id))

    return full_structure_list[i]['word_freq_list'][j]['freq']
#end GetTermFreq()

def GetTermIDF(term_id, term_IDF_list):
    #i = map(itemgetter('word_id'), term_IDF_list).index(str(term_id))
    for t in term_IDF_list:
        if t['word_id'] == term_id:
            return t['idf']
    #end for
    return -1
#end GetTermIDF()





#Read_QtUS_matrix('qt#U#lsaS.log')



'''
print '--------------------------------Start Reading term_IDF.log'
idf_file_name = 'term_IDF.log'
term_IDF_list = rd.ReadIDF(idf_file_name)
#for d in term_IDF_list:    print str(d['word_id']) + '\t' + str(d['freq']) + '\t' + str(d['idf']) + '\n'
print 'Read {0} terms!'.format(len(term_IDF_list))

print '36206'
print GetTermIDF(001, term_IDF_list)


#-----------------------
##read doc-file
#-----------------------
print '--------------------------------Start Reading Documents filename'
doc_dir = 'SPLIT_DOC_WDID_NEW/'
cmd = 'cd ' + doc_dir + '\nls\n'

word_freq_list = []

#下指令抓所有doc的檔名
doc_file_names_txt = os.popen(cmd).read()
doc_file_names_list = doc_file_names_txt.split('\n')
#ls會多印一個換行, 拿掉那個換行
del doc_file_names_list[-1]

#印出讀到的document數量
print 'Read {0} documents!'.format(len(doc_file_names_list))
#for d in doc_file_names_list: print '  ' + d

this_doc_word_freq = []
full_docs_wf_list = []

#this_doc_word_freq = rd.ReadOneDocument(doc_dir, doc_file_names_list[0])

for docs in doc_file_names_list:
#for docs in range(0, 30):
#    this_doc_word_freq = rd.ReadOneDocument(doc_dir, doc_file_names_list[docs])
    this_doc_word_freq = rd.ReadOneDocument(doc_dir, docs)
    temp = { 'doc_id': docs, 'word_freq_list': this_doc_word_freq }
    full_docs_wf_list.append(temp)


#print GetTermFreq('doc', full_docs_wf_list[0]['doc_id'], 44022 ,full_docs_wf_list)
#ex: VOM19980220.0700.0166's term lists below:
##[{'freq': 5, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '40889'},
## {'freq': 2, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '44022'},    <= taget
## {'freq': 1, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '10092'},
## {'freq': 1, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '2471'}]
#if input = 44022, then GetTermFreq('doc', VOM19980220.0700.0166, 44022, full_docs_wf_list) will get 2

#temp

#f = open('dump.txt', 'w')

#for pr in full_docs_wf_list:
#    f.write('$....Document= {0}\n'.format(pr['doc_id']))
#    f.write('.........WordFreqList= {0}\n'.format(pr['word_freq_list']))
#    f.write('$....EndThisDocument\n')
#    f.write('\n')
#f.close()


#把每個documents的結果寫入檔案來確認是否正確
print '--------------------------------Writing Documents logs'
f = open('dump_doc.log', 'w')

for pr in full_docs_wf_list:
    f.write('--------------------------------{0}\n'.format(pr['doc_id']))
    #print(pr['word_freq_list'])
    for w in pr['word_freq_list']: #word_id是-1不用印
        if int(w['word_id'], 10) != -1:
            f.write('    word_id ={0}\t|\tfreq ={1}\n'.format(w['word_id'], w['freq']))
    f.write('--------------------------------End {0}\n\n'.format(pr['doc_id']))
    f.write('\n')
f.close()
print 'Success write! @dump_query.log'


print 'NumOfDoc= ' + str(len(doc_file_names_list))
print '//////'

all_term_list_in_docs = []
#從Document中取得所有的term種類, 之後再記錄這個term的document freq
for a_doc in full_docs_wf_list:
    temp = { 'word_id': '', 'doc_freq': 0 }
    #print '--Scanning doc= {0}'.format(a_doc['doc_id'])
    for a_term in a_doc['word_freq_list']:
        #如果目前看到的term已經在新list內, 把它的doc_freq +1
        if any(saved_term['word_id'] == a_term['word_id'] for saved_term in all_term_list_in_docs):
            i = map(itemgetter('word_id'), all_term_list_in_docs).index(a_term['word_id'])
            all_term_list_in_docs[i]['doc_freq'] = all_term_list_in_docs[i]['doc_freq'] + 1
            do_nothing = 0
        else: #否則存進去
            temp = { 'word_id': a_term['word_id'], 'doc_freq': 1 }
            all_term_list_in_docs.append(temp)
    #end for wf list
#end for full_docs_wf_list

#到這裡已經有所有term的集合, 接下來要計算每個term出現在幾個document

print len(all_term_list_in_docs)
#print all_term_list_in_docs

fw = open('term_docFreq+IDF.log', 'w')

for walk in all_term_list_in_docs:
    fw.write(str(walk['word_id']) + '\t' + str(walk['doc_freq']) + '\t' + str(math.log(2265/walk['doc_freq'])) + '\n')

fw.close()

'''