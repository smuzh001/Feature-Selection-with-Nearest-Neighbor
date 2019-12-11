import sys
import math


#data = our current data file, curr_set = our current set of features (our testing set), k = our new feature we are considering
def leave_one_out(data, curr_set, k):
    num_correct = 0
     #iterate through rows
    for i in range(0, len(data) - 1):
        #print('I am looping over the rows '+ str(i) )
        best_so_far = sys.float_info.max
        best_loc = None
        for j in range(0, len(data)- 1):
            if i != j:
                #print('for exemplar '+str(i)+' i am comparing to '+ str(j))
                #distance = math.sqrt((data[i][k] - data[j][k])**2 )
                distance = 0
                for feature in curr_set:
                    distance += (data[i][feature] - data[j][feature] )**2
                distance = math.sqrt(distance + (data[i][k] - data[j][k] )**2 )

                if distance < best_so_far:
                    best_so_far = distance
                    best_loc = j

        #print('for exemplar '+ str(i)+ ' I believe its NN is '+str(best_loc))
        #check if NN is same class
        if data[i][0] == data[best_loc][0]:
            num_correct += 1
            #print('exempler '+str(i)+' is correct')
    Accuracy = num_correct / len(data)
    #print(num_correct)
    return Accuracy


def ForwardSelection(path):
    #print('Foward Selection is cool')
    best_set = set()
    best_acc = 0

    with open(path) as file:
        result = [[float(val) for val in line.split()] for line in file]
    
    featureCount = len(result[0]) - 1
    curr_set = set()
    
    for i in range(1, featureCount + 1):
        feature_to_add_at_this_level = None
        best_acc_so_far = 0
        
        for j in range(1, featureCount + 1):
            #ignore if j is already part of set
            if j in curr_set:
                continue
            #print('\tConsidering adding the '+ str(j)+ ' feature')
            accuracy = leave_one_out(result, curr_set ,j)
            if accuracy > best_acc_so_far:
                best_acc_so_far = accuracy
                feature_to_add_at_this_level = j        
        
        print('most accurate feature at level '+str(i)+': ' + str(feature_to_add_at_this_level) +' with an accuracy of '+str(best_acc_so_far))
        
        curr_set.add(feature_to_add_at_this_level)

        if best_acc_so_far > best_acc:
            best_acc = best_acc_so_far
            best_set = curr_set.copy()   
        #print('On the '+ str(i) + ' level of the search tree')
    print('On small dataset, the error rate can be '+str(best_acc) + ' when using only features: '+ str(best_set))





def BackwardHelper(data, curr_set, k):
    num_correct = 0
     #iterate through rows
    for i in range(0, len(data) - 1):
        #print('I am looping over the rows '+ str(i) )
        best_so_far = sys.float_info.max
        best_loc = None
        for j in range(0, len(data)- 1):
            if i != j:
                #print('for exemplar '+str(i)+' i am comparing to '+ str(j))
                #distance = math.sqrt((data[i][k] - data[j][k])**2 )
                distance = 0
                for feature in curr_set:
                    if feature == k:
                        continue
                    distance += (data[i][feature] - data[j][feature] )**2
                #distance = math.sqrt(distance + (data[i][k] - data[j][k] )**2 )

                if distance < best_so_far:
                    best_so_far = distance
                    best_loc = j

        #print('for exemplar '+ str(i)+ ' I believe its NN is '+str(best_loc))
        if data[i][0] == data[best_loc][0]:
            num_correct += 1
            #print('exempler '+str(i)+' is correct')
    Accuracy = num_correct / len(data)
    #print(Accuracy)
    return Accuracy


def BackwardElimination(path):
    #print('Backward Elimination is cool')
    with open(path) as file:
        result = [[float(val) for val in line.split()] for line in file]
    featureCount = len(result[0])
    curr_set = set()
    for x in range(1, featureCount):
        curr_set.add(x)
    #initialize our best_accuracy and best set with all the features
    best_set = curr_set.copy()
    best_acc = BackwardHelper(result, curr_set, 0)
    i = 0
    while len(curr_set) != 0:
        i += 1
        #print('Level '+str(i)+' accuracy: '+str(best_acc))

        feature_to_remove_this_level = None
        best_acc_so_far = best_acc
        
        for j in curr_set:
            #print('\tConsidering removing the '+ str(j)+ ' feature')
            accuracy = BackwardHelper(result, curr_set ,j)
            if accuracy > best_acc_so_far:
                best_acc_so_far = accuracy
                feature_to_remove_this_level = j      
        print('least significant feature at level '+str(i)+': ' + str(feature_to_remove_this_level) +' we improve to an accuracy of '+str(best_acc_so_far))
        
        if feature_to_remove_this_level == None:
            break
        
        curr_set.remove(feature_to_remove_this_level)

        if best_acc_so_far > best_acc:
            best_acc = best_acc_so_far
            best_set = curr_set.copy()   
        #print('On the '+ str(i) + ' level of the search tree')

    print('On small dataset, the error rate can be '+str(best_acc) + ' when using only features: '+ str(best_set))


def leave_one_out_prune(data, curr_set, k, prune_limit):
    num_correct = 0
    curr_miss_count = 0

    for i in range(0, len(data) - 1): #validate current row
        best_so_far = sys.float_info.max
        best_loc = None
        for j in range(0, len(data)- 1):    #figure out which is the NN
            if i != j:
                distance = 0
                for feature in curr_set:
                    distance += (data[i][feature] - data[j][feature] )**2
                distance = math.sqrt(distance + (data[i][k] - data[j][k] )**2 )

                if distance < best_so_far:
                    best_so_far = distance
                    best_loc = j


        if data[i][0] == data[best_loc][0]:
            num_correct += 1
        else:
            curr_miss_count += 1
            if curr_miss_count > prune_limit:
                return -1
        
        #check if curr_num_correct 

    return num_correct


def OGAlgorithm(path):
    #print('Foward Selection is cool')
    best_set = set()
    best_acc = 0

    with open(path) as file:
        result = [[float(val) for val in line.split()] for line in file]
    
    featureCount = len(result[0])
    curr_set = set()
    
    for i in range(1, featureCount):
        feature_to_add_at_this_level = None
        best_acc_so_far = 0
        min_miss_count = len(result)

        for j in range(1, featureCount):
            #ignore if j is already part of set
            if j in curr_set:
                continue
            #print('\tConsidering adding the '+ str(j)+ ' feature')
            correct_count = leave_one_out_prune(result, curr_set ,j, min_miss_count)
            
            #fell under prune limit
            if correct_count == -1:
                continue
            
            accuracy = correct_count / len(result)

            #update our accuracy
            if accuracy > best_acc_so_far:
                best_acc_so_far = accuracy
                min_miss_count = len(result) - correct_count
                feature_to_add_at_this_level = j


        print('most accurate feature at level '+str(i)+': ' + str(feature_to_add_at_this_level) +' with an accuracy of '+str(best_acc_so_far))
        
        curr_set.add(feature_to_add_at_this_level)

        if best_acc_so_far > best_acc:
            best_acc = best_acc_so_far
            best_set = curr_set.copy()   
        #print('On the '+ str(i) + ' level of the search tree')
    print('On small dataset, the error rate can be '+str(best_acc) + ' when using only features: '+ str(best_set))


while True:
    #print(dataSet.read())
    print('Welcome to Stanley Muzhuthettu Feature Generation Extravaganza\nPlease select the dataset 1: small 27. Or 2: large 29')
    choice = int(sys.stdin.readline())

    if choice == 1:
        path = 'CS170_SMALLtestdata__27.txt'
    elif choice == 2:
        path = 'CS170_LARGEtestdata__29.txt'
    else:
        print('Invalid Entry')
        continue

    print('Forward Selection: 1\nBackward Elimination: 2\nYour original search algorithm: 3\n')
    choice = int(sys.stdin.readline())

    if choice == 1:
        ForwardSelection(path)
    elif choice == 2:
        BackwardElimination(path)
    elif choice == 3:
        OGAlgorithm(path)
    else:
        print('Invalid Entry')
        continue

