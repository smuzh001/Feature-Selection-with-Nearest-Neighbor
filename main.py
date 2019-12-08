import sys
import numpy


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

def ForwardSelection():
    print('Foward Selection is cool')
    with open('CS170_SMALLtestdata__27.txt') as file:
        result = [[float(val) for val in line.split()] for line in file]
    #print(result[0])
    featureCount = len(result[0]) - 1
    curr_set = set()

    for i in range(1, featureCount + 1):
        feature_to_add_at_this_level = []
        best_acc_so_far = 0
        
        for j in range(1, featureCount + 1):
            #ignore if j is already part of set
            if j in curr_set:
                continue
            print('\tConsidering adding the '+ str(j)+ ' feature')
            accuracy = leave_one_out_cross_validation(j,curr_set)
            if accuracy > best_acc_so_far:
                best_acc_so_far = accuracy
                feature_to_add_at_this_level = j        
        
        print('best accuracy this level: ' + str(feature_to_add_at_this_level) +' with an accuracy of '+str(best_acc_so_far))
        curr_set.add(feature_to_add_at_this_level)        
        print('On the '+ str(i) + ' level of the search tree')








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

