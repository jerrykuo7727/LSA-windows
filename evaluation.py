import readquery as rq
import recallpercision as rp



correct_result_path = 'AssessmentTrainSet.txt'
query_result_path = 'final-ranking.log'


correct_result_set = rq.ReadInputFile(correct_result_path, 'A')

for e_a in correct_result_set:
    print '$ {0} : {1}'.format(len(e_a), str(e_a))

print '1-----------------------'
#rq.ReadInputFile(result_training_path)
query_result_set = rq.ReadInputFile(query_result_path, 'R')

for e_r in query_result_set:
    print '$ {0} : {1}'.format(len(e_r), str(e_r))

#rq.CheckCall()
print '2-----------------------'
final_table_in_queries = []
rp_in_every_query = []
rank_of_rpc_in_every_query = []

for i in range(0, 16) :
    rp_in_every_query = rp.CalculateRecallPercision(query_result_set[i], correct_result_set[i])
    rank_of_rpc_in_every_query = rp.InterpolatedRPC(query_result_set[i], rp_in_every_query)
    final_table_in_queries.append(rank_of_rpc_in_every_query)
#end for

print len(final_table_in_queries)
print '3-----------------------'
average_rp_in_final_table = []
index_in_rank_table = 0
sum_of_percision = 0
average_percision = 0

for index_in_rank_table in range(0, 100):
    for index_in_final_table in range(0, len(final_table_in_queries)): #0~15
        sum_of_percision = final_table_in_queries[index_in_final_table][index_in_rank_table]['percision'] + sum_of_percision

    #end for
    average_percision = sum_of_percision / len(final_table_in_queries)
    #print '** ' + str(average_percision)
    average_rp_in_final_table.append(average_percision)
    average_percision = 0
    sum_of_percision = 0
#end for
print '4-----------------------'
#rp curve:
print average_rp_in_final_table

sum_of_percision_in_rank_table = 0
every_average_percision_list = []

direct_cal_map = 0
print '5-----------------------'

for i_in_final in final_table_in_queries:
    for j_in_rank_table in range(0, 100):
        sum_of_percision_in_rank_table = i_in_final[j_in_rank_table]['percision'] + sum_of_percision_in_rank_table
    #end for
    every_average_percision_list.append(sum_of_percision_in_rank_table / 100)
    direct_cal_map = (sum_of_percision_in_rank_table / 100 ) + direct_cal_map
    sum_of_percision_in_rank_table = 0
    #do this 16 times
#end for

print direct_cal_map / 16
