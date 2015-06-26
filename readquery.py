import codecs


def CheckCall():
    print 'readquery.py !'
#end CheckCall()



##read the filename, and stored in a dictionary of list.
def ReadInputFile(filename, option):
    answer = []
    query = []
    full_txt = codecs.open( filename, 'r').read()
    full_txt = full_txt.replace('\r', ' ')
    split_line_list = full_txt.split('\n')


    if option == 'A' : #AssessmentTrainSet.txt
        for element in split_line_list:
            #if the current line is [Query   1 20001.query  95]
            if element.find('Query') != -1:
                if len(query) != 0 :
                    answer.append(query)
                    #print '$ {0} : {1}'.format(str(len(query)), str(query))
                    query = []
                #end if
            #end if
            else : #else if [VOM19980603.0730.0280]
                if len(element) != 0:
                    dic_of_every_doc = { 'recall' : 0, 'percision' : 0, 'doc' : element }
                    query.append(dic_of_every_doc)
            #end else
        #end for

        if len(query) != 0 :
            answer.append(query)
            query = []
        #end if last check
    #end if AssessmentTrainSet.txt
    ## ------------------------------------------------------
    else : #if option == 'R': #ResultsTrainSet.txt
        for element in split_line_list:
            #if the current line is [Query   1 20001.query  95]
            if element.find('Query') != -1:
                if len(query) != 0 :
                    answer.append(query)
                    #print '$ {0} : {1}'.format(str(len(query)), str(query))
                    query = []
                #end if
            #end if
            else : #else if [VOM19980510.0700.0568 -1.938743e+003]
                if len(element) != 0:
                    query.append(element[:21])
            #end else
        #end for

        if len(query) != 0 :
            answer.append(query)
            query = []
        #end if last check
    #end if ResultsTrainSet.txt

    return answer
#end ReadInputFile()
