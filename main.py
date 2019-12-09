import sys
import numpy as np
import math


def leave_one_out_cross_validation(x, curr_set):
    switch = {
        1: 0.84,
        2: 0.87,
        3: 0.79,
        4: 0.88,
        5: 0.64,
        6: 0.45,
        7: 0.87,
        8: 0.86,
        9: 0.65,
        10: 0.12,
    }
    return switch.get(x, 0)

def leave_one_out(data, curr_set, k):
    num_correct = 0
     #iterate through rows
    for i in range(0, len(data) - 1):
        #print('I am looping over the rows '+ str(i) )
        #check feature of the rows
        best_so_far = sys.float_info.max
        best_loc = None
        accuracy = None
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
        if data[i][0] == data[best_loc][0]:
            num_correct += 1
            #print('exempler '+str(i)+' is correct')
    Accuracy = num_correct / len(data)
    #print(Accuracy)
    return Accuracy


def ForwardSelection():
    #print('Foward Selection is cool')
    best_set = set()
    best_acc = 0

    with open('CS170_SMALLtestdata__27.txt') as file:
        result = [[float(val) for val in line.split()] for line in file]
    print(result[0][1])
    featureCount = len(result[0]) - 1
    curr_set = set()
    #print(leave_one_out(result, 1))
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





def BackwardElimination():
    print('Backward Elimination is cool')

def OGAlgorithm():
    print('My own original algorithm')


while True:
    #print(dataSet.read())
    print('Welcome to Stanley Muzhuthettu Feature Generation Extravaganza\nPlease select the wrapper:')
    print('Forward Selection: 1\nBackward Elimination: 2\nYour original search algorithm: 3\n')
    choice = int(sys.stdin.readline())

    if choice == 1:
        ForwardSelection()
    elif choice == 2:
        BackwardElimination()
    elif choice == 3:
        OGAlgorithm()
    else:
        print('Invalid Entry')

