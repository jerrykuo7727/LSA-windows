# -*- coding: utf-8 -*-
import codecs
import re
from operator import itemgetter

def ReadOneDocument(doc_dir, filename):
    #讀取doc後, 回傳這個doc內的所有term及出現次數
    #print 'Read_File= ' + filename
    path = doc_dir + filename
    full_txt = codecs.open( path, 'r').read()
    full_txt = full_txt.replace('\n', ' ')
    full_txt = full_txt.replace('\r', ' ')
    split_line_list = full_txt.split(' ')

    del_index = []
    #print len(split_line_list[0])

    split_line_list = split_line_list[8:]
    #print len(split_line_list)
    #print split_line_list

    #刪掉-1
    for check in split_line_list:
        if check == '-1':
            split_line_list.remove('-1')
    #end for del -1


    #delete空的element的index
    empty = split_line_list.count('')
    for check in range(0, empty):
        split_line_list.remove('')
    #end for delete空元素


    #計算每個word id的出現次數
    word_freq_list = []

    for this_word_id in split_line_list:
        #如果這個word#不是第一次出現, 找到對應的word id, 頻率+1
        if any(d['word_id'] == this_word_id for d in word_freq_list):
            i = map(itemgetter('word_id'), word_freq_list).index(this_word_id)
            word_freq_list[i]['freq'] = word_freq_list[i]['freq'] + 1
        #end if
        else : #第一次出現, 存進新的list
            word_info = { 'word_id': this_word_id, 'freq': 1, 'appeared_in_doc': filename }
            word_freq_list.append(word_info)
        #end else
    #end for
    '''
    print split_line_list
    print '---------'
    print word_freq_list
    '''
    return word_freq_list
#ReadOneDocument()



def ReadOneQuery(query_dir, filename):
    #讀取doc後, 回傳這個doc內的所有term及出現次數
    #print 'Read_File= ' + filename
    path = query_dir + filename
    full_txt = codecs.open( path, 'r').read()
    full_txt = full_txt.replace('\n', ' ')
    full_txt = full_txt.replace('\r', ' ')
    split_line_list = full_txt.split(' ')

    del_index = []

    #刪掉-1
    minus1 = split_line_list.count('-1')
    print '-1$' + str(minus1)
    for check in range(0, minus1):
        split_line_list.remove('-1')
    #end for del -1


    #delete空的element的index
    empty = split_line_list.count('')
    print '    empty$' + str(empty)

    for check in range(0, empty):
        split_line_list.remove('')
    #end for delete空元素

    #計算每個word id的出現次數
    query_word_freq_list = []

    for this_word_id in split_line_list:
        #如果這個word#不是第一次出現, 找到對應的word id, 頻率+1
        if any(d['word_id'] == this_word_id for d in query_word_freq_list):
            i = map(itemgetter('word_id'), query_word_freq_list).index(this_word_id)
            query_word_freq_list[i]['freq'] = query_word_freq_list[i]['freq'] + 1
        #end if
        else : #第一次出現, 存進新的list
            word_info = { 'word_id': this_word_id, 'freq': 1, 'appeared_in_query': filename }
            query_word_freq_list.append(word_info)
        #end else
    #end for
    '''
    print split_line_list
    print '---------'
    print query_word_freq_list
    '''
    return query_word_freq_list
#ReadOneDocument()

def ReadIDF(filename):
    term_list = []
    with open(filename) as file:
        for line in file:
            (word_id, freq, idf) = line.split()
            term_list.append({ 'word_id': word_id, 'freq': freq, 'idf': idf })
        #end for every line in file
    #end read from file
    #for d in term_list:
    #    print str(d['word_id']) + '\t' + str(d['freq']) + '\t' + str(d['idf']) + '\n'
    #end for
    return  term_list
#ReadIDF()


