# -*- coding: utf-8 -*-
from operator import itemgetter

#Given a list of queries and correct result lists, return the value of recall
def CalculateRecallPercision(query_list, result_list):
    num_correct = 0.00
    num_doc = 0.00
    sequencial_answer = []
    temp_answer_dic = {}

    for every_doc in query_list :
        num_doc = num_doc + 1
        #是relevant的文章才要算recall
        if IsInList(every_doc, result_list):
            num_correct = num_correct + 1
            index = map(itemgetter('doc'), result_list).index(every_doc)

            if index != -1:
                temp_answer_dic['doc'] = result_list[index]['doc']
                temp_answer_dic['recall'] = num_correct / len(result_list)
                temp_answer_dic['percision'] = num_correct / num_doc
                sequencial_answer.append(temp_answer_dic)
                temp_answer_dic = {}
            #print '# r= {0}, p= {1}'.format(result_list[index]['recall'], result_list[index]['precision'])
        #不是
        #print IsInList( 'VOM19980606.0730.0134', result_list[15] )
    #end for
    return sequencial_answer
#end CalculateRecallPercision()


def InterpolatedRPC(query_list, result_list):
    table = []

    #index = query_list.index(result_list[-1]['doc'])
    #table.append(result_list[index])

    #initiallize the table with 0.00
    for sample in range(0, 100):
        table.append({ 'doc' : '', 'recall' : 0.00, 'percision' : 0.00 })
    #end for
    #print '@@ ' + str(len(table))

    for flag in result_list:
        num_of_index = int(flag['recall']* 100.00)
        table[num_of_index-1] = flag

    current_rp = { 'doc' : '', 'recall' : 0.00, 'percision' : 0.00 }
    #print '&' + str(table[99]['recall'])
    for step in range(99, -1, -1):
        #print '%%   ' + str(step)
        if table[step]['recall'] != 0.00:
            if table[step]['percision'] > current_rp['percision'] :
                current_rp = table[step]
                #print '//////////////  ' + str(current_rp)

        else : #step['recall'] is 0.00
            table[step] = current_rp
            #print '\\\\\\\\\\\\\\\\\  ' + str(step)
    #end for
    return table
    #print '@@ ' + str(table)
#end InterpolatedRPC()


def IsInList(target, result_list):
    for e in result_list:
        if e['doc'] == target :
            return True
    return False
#end SearchFromList()