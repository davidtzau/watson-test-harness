###########################################################################################################################
#getting started with IBM Watson Natural Language Classifier : https://www.ibm.com/watson/developercloud/nl-classifier.html
#Python SDK for Watson NLC  :  https://github.com/watson-developer-cloud/python-sdk
#Author: David Tzau
###########################################################################################################################
import json
import csv
from watson_developer_cloud import NaturalLanguageClassifierV1

SERVICE_ID = 'YOUR_WATSON_SERVICE_ID'

natural_language_classifier = NaturalLanguageClassifierV1(
    username='YOUR_WATSON_ACCOUNT_USERNAME',
    password='YOUR_WATSON_ACCOUNT_PASSWORD')


#check the status of the NLC to see if is available.  During trianing the service is not available
status = natural_language_classifier.status(SERVICE_ID)

if status['status'] == 'Available':    

    #open the top category input CSV file and create a list of lists.  Each line represents one list
    with open('test_input_file.csv', 'rb') as f:
        reader = csv.reader(f)
        full_list = list(reader)

    output_file = open('test_results_file.csv', 'w')
    output_file.write('Keyword,WatsonRank1,WatsonRank1Category,WatsonRank1Confidence,WatsonRank2,WatsonRank2Category,WatsonRank2Confidence,WatsonRank3,WatsonRank3Category,WatsonRank3Confidence,WatsonRank4,WatsonRank4CateCategorygory,WatsonRank4Confidence,WatsonRank5,WatsonRank5Category,WatsonRank5Confidence\n')

    #ingore the header 
    full_list = full_list[1:len(full_list)]

    #iterate through the list, calling the Watson service to extract top 5 categories
    for input_record in full_list:
        #get the keyword
        keyword = input_record[0]

        print keyword
        
        #call the watson natural language classifier with the query
        response  = natural_language_classifier.classify(SERVICE_ID, keyword)

        #get the top classes return by Watson
        categories = response['classes']
        
        #sort the categories by the confidence rating returned by Watson.  This whould already be sorted, but sorting again just in case
        sorted_categories = sorted(categories, key=lambda k:k['confidence'], reverse=True)

        #print '---'
        #print (json.dumps(sorted_categories, indent=2))
        
        #grab only the top 5 categories
        top_5_categories = sorted_categories[:5]

        #output the results to file
        output_file.write(keyword)

        #output results from Watson algorithm to file
        for category_result in top_5_categories:
            output_file.write("," + category_result['class_name'] + "," + str(category_result['confidence']))

        output_file.write('\n')
        
    #close the file
    output_file.close()
        
print "done"
