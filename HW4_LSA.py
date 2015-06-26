# -*- coding: utf-8 -*-
import read_doc_query as rd
import os
import readLSA as rl
import vsm_term as t
import math
import numpy as np
from operator import itemgetter
from numpy import linalg as la

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
    return 0
#end GetTermIDF()


lsa_dim = 50

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
#end for read doc files

#print GetTermFreq('doc', full_docs_wf_list[0]['doc_id'], 44022 ,full_docs_wf_list)
#Usage:: VOM19980220.0700.0166's term lists below:
## [{'freq': 5, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '40889'},
##  {'freq': 2, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '44022'},    <= taget
##  {'freq': 1, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '10092'},
##  {'freq': 1, 'appeared_in_doc': 'VOM19980220.0700.0166', 'word_id': '2471'}]
#if input = 44022, then GetTermFreq('doc', VOM19980220.0700.0166, 44022, full_docs_wf_list) will get 2


#把每個documents的結果寫入檔案來確認是否正確
#print '--------------------------------Writing Documents logs'
#f = open('dump_doc.log', 'w')

#for pr in full_docs_wf_list:
#    f.write('--------------------------------{0}\n'.format(pr['doc_id']))
#    #print(pr['word_freq_list'])
#    for w in pr['word_freq_list']: #word_id是-1不用印
#        if int(w['word_id'], 10) != -1:
#            f.write('    word_id ={0}\t|\tfreq ={1}\n'.format(w['word_id'], w['freq']))
#    f.write('--------------------------------End {0}\n\n'.format(pr['doc_id']))
#    f.write('\n')
#f.close()
#print 'Success write! @dump_query.log'
#print 'NumOfDoc= ' + str(len(doc_file_names_list))
#print '//////'



#-----------------------
#read preprocessed term-IDF   #讀取term的IDF資料 （讀檔term_IDF.log）
#-----------------------
print '--------------------------------Start Reading term_IDF.log'
idf_file_name = 'term_IDF.log'
term_IDF_list = rd.ReadIDF(idf_file_name)
#for d in term_IDF_list:    print str(d['word_id']) + '\t' + str(d['freq']) + '\t' + str(d['idf']) + '\n'
print 'Read {0} terms!'.format(len(term_IDF_list))


#-----------------------
#read query-file
#-----------------------
print '--------------------------------Start Reading Query filename'
query_dir = 'QUERY_WDID_NEW/'
cmdq = 'cd ' + query_dir + '\nls\n'

#下指令抓QUERY_WDID_NEW下的query檔名
query_file_names_txt = os.popen(cmdq).read()
query_file_names_list = query_file_names_txt.split('\n')

#ls會多印一個換行, 拿掉那個換行
del query_file_names_list[-1]

#印出讀到的query數量
print 'Read {0} queries!'.format(len(query_file_names_list))
#for q in query_file_names_list: print '  ' + q

#開始建立每個query的term-freq list
this_qry_word_freq = []
full_qrys_wf_list = []

for qrys in query_file_names_list:
    #for docs in range(0, ):
    this_qry_word_freq = rd.ReadOneQuery(query_dir, qrys)
    temp = { 'qry_id': qrys, 'word_freq_list': this_qry_word_freq }
    full_qrys_wf_list.append(temp)
#end for read qery files

#把每個query的結果寫入檔案來確認是否正確
#print '--------------------------------Writing Query logs'
#f = open('dump_query.log', 'w')

#for pr in full_qrys_wf_list:
#    f.write('--------------------------------{0}\n'.format(pr['qry_id']))
#    for w in pr['word_freq_list']: #word_id是-1不用印
#        if int(w['word_id'], 10) != -1:
#            f.write('    word_id ={0}\t|\tfreq ={1}\n'.format(w['word_id'], w['freq']))
#    f.write('--------------------------------End {0}\n\n'.format(pr['qry_id']))
#    f.write('\n')
#f.close()
#print 'Success write! @dump_query.log'


#還沒產生query的matrix
#TODO: 把query的matrix建出來, 每個row是一個query, 每個元素是term在該query的TF-IDF
#                  column = term數量
#               ------------------------
#               |                      |
#               |                      |
#  row = query  |                      |
#       16個    |                      |
#               |                      |
#               ------------------------
###query中每個term的freq可以從full_qrys_wf_list[0~15]['word_freq_list']中取得
###呼叫 GetTermFreq('query', full_qrys_wf_list[0~15]['qry_id'], term-id ,full_qrys_wf_list)

query_term_matrix = []
#
#對所有query, 依照term id的index放入它的TF-IDF
q_num = 0
#先試試看只用IDF會怎麼樣！
for a_query in full_qrys_wf_list:
    term_vector = [0]*51254
    for qt in a_query['word_freq_list'] :
        #term_vector[int(qt['word_id'], 10)] = GetTermIDF(qt['word_id'], term_IDF_list)
        tf = float(GetTermFreq('query', a_query['qry_id'], int(qt['word_id'], 10), full_qrys_wf_list))
        idf = float(GetTermIDF(qt['word_id'], term_IDF_list))
        term_vector[int(qt['word_id'], 10)] = tf*idf
        #print str(qt['word_id']) + '\t' + str(term_vector[int(qt['word_id'], 10)]) + '\t' + str(tf) + '\t' + str(idf) + '\t' + str(tf*idf) + '\n'
        #def GetTermFreq(type, doc_id, term_id, full_structure_list):

    #end for word_freq_list for every query
    q_num = q_num + 1
    query_term_matrix.append(term_vector)
    term_vector = [0]*51254
#end for
#GetTermIDF(2572, term_IDF_list)


#試試看TF-IDF

#print GetTermFreq('query', full_qrys_wf_list[0]['qry_id'], '2280',full_qrys_wf_list)

#print '=============================check'
#for pr in range(0, 51254):
#    if query_term_matrix[0][pr] != 0:
#        print str(pr) + '\t' + str(query_term_matrix[0][pr])



#//////////////////////////////////////////////////////////////
#以Column major讀入LSA-Ut檔案, 並印出結果

print '--------------------------------Read LSA-Ut matrix '
filename = 'LSA' + str(lsa_dim) + '-Ut'
#cmd = "awk '{print $2}' " + filename
#os.system(cmd)

#After read LSA-Ut, the matrix(list) will show below:
#                  column = dimension
#               ------------------------
#               |                      |
#               |                      |
#  row = term   |           U          |
#               |                      |
#               |                      |
#               ------------------------
lsa_U_matrix = []
#fu = open('LSA_U_matrix.log', 'w')

for d in range(0, lsa_dim):
    file_column = rl.getRow(filename)[d]
    lsa_U_matrix.append(file_column)

    #fu.write('\n--------------------------------Column {0}\n'.format(d))
    #for c in file_column:
    #    fu.write('    ' + str(c))
    #    fu.write('\n')
    #fu.write('\n\n')

#fu.write(str(lsa_U_matrix))
#fu.close()


#//////////////////////////////////////////////////////////////
#以Column major讀入LSA-Vt檔案, 並印出結果

print '--------------------------------Read LSA-Vt matrix '
filename = 'LSA' + str(lsa_dim) + '-Vt'
#cmd = "awk '{print $2}' " + filename
#os.system(cmd)

#After read LSA-VT, the matrix(list) will show below:
#                    column = dimension
#                 ------------------------
#                 |                      |
#                 |                      |
#  row = document |           V          |
#                 |                      |
#                 |                      |
#                 ------------------------
lsa_V_matrix = []
#fv = open('LSA_V_matrix.log', 'w')

for d in range(0, lsa_dim):
    file_column = rl.getRow(filename)[d]
    lsa_V_matrix.append(file_column)

    #fv.write('\n--------------------------------Column {0}\n'.format(d))
    #for c in file_column:
    #    fv.write('    ' + str(c))
    #    fv.write('\n')
    #fv.write('\n\n')

#fv.write(str(lsa_V_matrix))
#fv.close()



#//////////////////////////////////////////////////////////////
#以Column major讀入LSA-S檔案, 並印出結果

print '--------------------------------Read LSA-S matrix '
filename = 'LSA' + str(lsa_dim) + '-S'
#cmd = "awk '{print $2}' " + filename
#os.system(cmd)

#LSA-S是對角矩陣， 存他的對角值就好
lsa_S_diagonal = []
#fs = open('LSA_S_diagonal.log', 'w')

#只有一直行, 直接讀就好
file_column = rl.getCol(filename)[0]

#不知道為甚麼讀完之後, list裏面每個element都會多\n, 把它拿掉
for fix in range(0, lsa_dim):
    file_column[fix] = file_column[fix].replace('\n', '')

#拿掉才照之前的工作方式作
lsa_S_diagonal.append(file_column)

#fs.write(str(file_column))
#fs.write('\n--------------------------------Column Only 1\n')
#for c in file_column:
#    fs.write('    ' + str(c))
#    fs.write('\n')
#fs.close()
#print '************************'
#print lsa_S_diagonal


#現在我們有   LSA-U    和   LSA-V       的矩陣, 以及  對角矩陣S的對角線
#分別存在  lsa_U_matrix, lsa_V_matrix,              lsa_S_diagonal

#還有
'--------------------------------Prepare matrix'
lsa_U = np.array(lsa_U_matrix, float)
lsa_U = np.transpose(lsa_U)

lsa_S = np.zeros((lsa_dim, lsa_dim), float) #create 50x50 matrix filled with 0
np.fill_diagonal(lsa_S, lsa_S_diagonal) #assign diagonal values

qt_matrix = np.array(query_term_matrix, float)

lsa_Vt = np.array(lsa_V_matrix, float)
lsa_Vt = np.transpose(lsa_Vt)

print 'Size of qt_matrix = {0}'.format(qt_matrix.shape)
print 'Size of lsa_U = {0}'.format(lsa_U.shape)
print 'Size of lsa_S = {0}'.format(lsa_S.shape)
print 'Size of lsa_Vt = {0}'.format(lsa_Vt.shape)

np.savetxt('S.log', lsa_S)
np.savetxt('U.log', lsa_U)
np.savetxt('V.log', lsa_U)
np.savetxt('qt.log', qt_matrix)
#first, we multiply matrixes => qt_matrix * lsa_U
#fout = open('qt#lsaU.log', 'w')
print '--------------------------------Calculating qt_matrix * lsa_U_matrix'
qt_mult_lsaU = np.dot(qt_matrix, lsa_U)
np.savetxt('qt#lsaU.log', qt_mult_lsaU)
print 'Success writing file: qt#lsaU.log'
print 'Size of qt_matrix*lsa_U = {0}'.format(qt_mult_lsaU.shape)

print '--------------------------------Calculating qt_matrix * lsa_U_matrix * lsa_S_diagonal'
qtU_mult_lsaS = np.dot(qt_mult_lsaU, lsa_S)
np.savetxt('qt#U#lsaS.log', qtU_mult_lsaS)
print 'Success writing file: qt#U#lsaS.log'
print 'Size of (qt_matrix*lsa_U)*lsa_S = {0}'.format(qtU_mult_lsaS.shape)

#print '--------------------------------Read matrix (qt_matrix * lsa_U_matrix * lsa_S_diagonal)'
#qUS_matrix = rl.Read_QtUS_matrix('qt#U#lsaS.log')

result_qtUS_cos_lsaV = []
r = 0
#把qtU_mult_lsaS的row跟lsa_Vt的row算cos

print '--------------------------------Calculating cosine '
print 'Size of QUS = {0}'.format(qtU_mult_lsaS.shape)
print 'Size of lsa_Vt = {0}'.format(lsa_Vt.shape)


for q in range(0, len(qtU_mult_lsaS)):

    temp_QUS_cos_every_row_ofVt = [0]*2266
    for v in range(0, len(lsa_Vt)):
        molecule = np.dot(lsa_Vt[v], qtU_mult_lsaS[q]) #分子 Molecule
        denominator = la.norm(lsa_Vt[v])*la.norm(qtU_mult_lsaS[q]) #分母 Denominator
        temp_QUS_cos_every_row_ofVt[v] = molecule / denominator
    #end for every doc in Vt

    #以lsa維度＝50為例, 每一個query分別與2265篇documents做cosine, temp_QUS_cos_every_row_ofVt 應該是 1x2265的row vector
    result_qtUS_cos_lsaV.append(temp_QUS_cos_every_row_ofVt)
#end for


result_qtUS_cos_lsaV = np.array(result_qtUS_cos_lsaV, float)

np.savetxt('result.log', result_qtUS_cos_lsaV)
print '\nSize of result = {0}'.format(result_qtUS_cos_lsaV.shape)

print '--------------------------------Aligning documents and scores '
#把算好的cos matrix分別對應到各自的query
#doc_file_names_list 存doc的名字, 從名字編號小到大
final_ranking = []
map_result2query = []
print doc_file_names_list[0]
print doc_file_names_list[1]
print doc_file_names_list[2]
print doc_file_names_list[3]
#print result_qtUS_cos_lsaV[0][1]

for q in range(0, len(result_qtUS_cos_lsaV)):
    for id in range(0, len(doc_file_names_list)):
        temp = { 'doc_id': doc_file_names_list[id] , 'rank': result_qtUS_cos_lsaV[q][id] }
        map_result2query.append(temp)
    #end for every docs
    final_ranking.append(map_result2query)
    map_result2query = []
#for every query


print final_ranking[0]


ff = open('final-before-ranking.log', 'w')
#ff.write(str(final_ranking))
t = 1
for op in range(0, len(final_ranking)):
    ff.write('Query' + str(t) + '\n')

    for d in range(0, len(final_ranking[op])):
        ff.write(final_ranking[op][d]['doc_id'] + '\t' )
        ff.write(repr(final_ranking[op][d]['rank']))
        ff.write('\n')

    t = t + 1
#end for

ff.close()

#對應完之後照cos值排序

ranked_list = []

for i in range(0, len(final_ranking)):
    sorted_row_dic = sorted(final_ranking[i], key=itemgetter('rank'), reverse=True)
    ranked_list.append(sorted_row_dic)
#end for

print ranked_list[0]

print '-----'

print ranked_list[1]
print ranked_list[1]

#Query 7      20023.query 2265
ff = open('final-ranking.log', 'w')
#ff.write(str(final_ranking))
t = 1
for op in range(0, len(ranked_list)):
    ff.write('Query ' + str(t) + ' .query  2265\n')

    for d in range(0, len(ranked_list[op])):
        ff.write(ranked_list[op][d]['doc_id'] + '\t' )
        ff.write(repr(ranked_list[op][d]['rank']))
        ff.write('\n')
    #end for

    ff.write('\n')

    t = t + 1
#end for

ff.close()



