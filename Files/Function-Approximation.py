import random
import math
import copy
import matplotlib.pyplot as plt
import time
import numpy as np
import os
class node:
    def __init__(self,value):
        self.value = value
        self.right = None
        self.left = None
        self.Probability = None
        
    def __lt__(self, other):
         return self.Probability > other.Probability
     
def truncate(n, decimals=0):
    if n == math.nan:
        return 0
    else:
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier
        
def PopulationCreator(size):
    Operators = ['+' , '-' , '*' , '/' , '^' , 'sin' , 'cos']
    Operands = [-9 , -8 , -7 , -6 , -5 , -4 , -3 , -2 , -1 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 0.5 ]
    FirstPopulation = list()
    for i in range(size):
        operator = random.choice(Operators)
        operand = random.choice(Operands)
        ParentNode = node(operator)
        ParentNode.left = node('x')
        if operator == 'sin' or operator == 'cos':
            ParentNode.right = node(None)
        else:
            ParentNode.right = node(operand)
        FirstPopulation.append(ParentNode)
    return FirstPopulation

def inorder(root):
    if root is not None:
        inorder(root.left)
        print (root.value)
        inorder(root.right)
def PrintExpressionTree(root):
    if root is None:
        return 
    if root.left is None and root.right is None:
        if root.value == 'x':
            return 'x'
        else:
            return root.value  
    LeftSum = PrintExpressionTree(root.left)
    RightSum = PrintExpressionTree(root.right)
    
    if root.value == '+':
        return '(',LeftSum ,'+', RightSum,')'
    
    elif root.value == '-':
        return '(',LeftSum,'-', RightSum,')'
    
    elif root.value == '*':
        return '(',LeftSum ,'*', RightSum,')'
    
    elif root.value == '^':
        return '(',LeftSum,'^',RightSum,')'
    
    elif root.value == '/':
        return '(',LeftSum ,'/', RightSum,')'
    
    elif root.value == 'sin':
        return 'sin(',LeftSum,')'
    
    elif root.value == 'cos':
        return 'cos(',LeftSum,')'
    
def EvaluateExpressionTree(root , s):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        if root.value == 'x':
            return s
        else:
            return root.value  
    LeftSum = EvaluateExpressionTree(root.left , s=s)
    RightSum = EvaluateExpressionTree(root.right , s=s)
    
    if type(LeftSum) is complex or type(RightSum) is complex:
        return 0
    if root.value == '+':
        return LeftSum + RightSum
    
    elif root.value == '-':
        return LeftSum - RightSum
    
    elif root.value == '*':
        return LeftSum * RightSum
    
    elif root.value == '^':
        if LeftSum == 0:
            return 0
        else:
            if LeftSum < -10000 or RightSum < -1000 or LeftSum > 10000 or RightSum > 1000:
                return 0
            else:
                if RightSum < 0:
                    if (1/LeftSum) < -10000 or (1/LeftSum) > 10000 or RightSum < -1000 :
                        return 0
                    else:
                        return (1/LeftSum) ** (-1*RightSum)
                else:
                    return LeftSum ** RightSum
    
    elif root.value == '/':
        if RightSum == 0:
            return 1000000000000
        else:
            return LeftSum / RightSum
    
    elif root.value == 'sin':
        return math.sin(LeftSum)
    
    elif root.value == 'cos':
        return math.cos(LeftSum)

def CombineTrees(Tree1 , Tree2):
    NewTree = copy.deepcopy(Tree1)
    while(True):
        if NewTree.left.value == 'x':
            NewTree.left = Tree2
            return NewTree
        else:
            NewTree = NewTree.left

def FindProb(Tree , x, y):
    Sum = 0
    Fx = list()
    yx = copy.deepcopy(y)
    for i in range(len(yx)):
        if yx[i] < 0 :
            yx[i] = abs(yx[i])
    yx.sort()
    Max = yx[len(yx) - 1]
    for i in range(len(x)):
        Fx.append(EvaluateExpressionTree(root=Tree , s=x[i]))
    for i in range(len(y)):
        DeltaY = abs(y[i] - Fx[i])
        Sum = Sum + DeltaY
    MeanDeltaY = Sum/(len(y))
    Tree.Probability = (Max - MeanDeltaY)/Max

def Mutation(Tree):
    nodes = list()
    nodes.append(Tree)
    Operators = ['+' , '-' , '*' , '/' , '^' , 'sin' , 'cos']
    Operands = [-9 , -8 , -7 , -6 , -5 , -4 , -3 , -2 , -1 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9  , 0.5 , 'x']
    i = 0
    while len(nodes) > 0:
        UnderTestNode = nodes[i]
        i = i + 1
        probability = random.random()*100
        if probability < 10:
            if UnderTestNode.value in Operators:
                    if UnderTestNode.value == 'cos' or UnderTestNode.value == 'sin':
                        UnderTestNode.value = random.choice(Operators)
                        UnderTestNode.right.value = random.choice(Operands)
                        return
                    else:
                        UnderTestNode.value = random.choice(Operators)
                        return
            elif UnderTestNode.value == 'x':
                UnderTestNode.value = 'x'
                return
            elif UnderTestNode.value in Operands:
                UnderTestNode.value = random.choice(Operands)
                return
        else:
            if UnderTestNode.left is not None and UnderTestNode.right is not None:
                nodes.append(UnderTestNode.left)
                nodes.append(UnderTestNode.right)
            else:
                return
        if i==100:
            return
            
    
def GPAlgorithm(Population , x , y):
    SelectedPopulation = list()
    NewPopulation = list()
    NewPopulation = copy.deepcopy(Population)
    SelectedPopulation = copy.deepcopy(Population)
    Iteration = 0
    while (True):
        Iteration = Iteration + 1
        for i in range(300):
            p1 = random.choice(SelectedPopulation)
            p2 = random.choice(SelectedPopulation)
            NewPopulation.append(CombineTrees(p1 , p2))
            NewPopulation.append(CombineTrees(p2 , p1))
        for Tree in NewPopulation:
            Mutation(Tree=Tree)          
        for Tree in NewPopulation:
            FindProb(Tree=Tree , x=x , y=y)
        NewPopulation.sort()
        SelectedPopulation.clear()
        for i in range(len(Population)):
            SelectedPopulation.append(NewPopulation[i])
        if SelectedPopulation[0].Probability > 0.998:
            return SelectedPopulation[0],Iteration,len(NewPopulation)
        if Iteration == 200:
            return SelectedPopulation[0],Iteration,len(NewPopulation)
        NewPopulation.clear()
        NewPopulation = copy.deepcopy(SelectedPopulation)
        for k in range(len(Population)):
            SelectedPopulation.append(Population[k])
        
    
    
    
start_time = time.time()   
Population = PopulationCreator(200)

x=[x for x in np.arange(-5 , 5 , 0.1)]
y = list()
for i in range(len(x)):
    #y.append(x[i]*np.sin(x[i]+1))
    #y.append(x[i]+0.5)
    y.append(7*x[i]**4 + 2)
    #y.append(x[i]*np.sin(x[i]))
    #y.append(2*x[i]**3 + 2)
    #y.append(6*np.sin(x[i]) + 3)
    #y.append(-1*x[i]+3)
    #y.append(2*x[i]**3 + 8*x[i]**2 + 2*x[i])

#y = 4000*log(x) + 2
#x = [x for x in np.arange(0.1 , 5 , 0.1)]
#y = list()
#for i in range(len(x)):
#    y.append(4000*math.log(x[i]))

# y = x + 5 for 0<=x<=5 and y = x^2 for 5<x<=10
#x = [x for x in np.arange(0 , 10 , 0.1)]
#y = list()
#for i in range(len(x)):
#    if i < (len(x)/2):
#        y.append(x[i]+5)
#    else:
#        y.append(x[i]**2)

#x = [0 , 0.5 , 1 , 1.5 , 2 , 2.5 , 3 , 3.5 , 4 , 4.5 , 5 , 5.5 , 6 , 6.5 , 7 , 7.5 , 8 , 8.5 , 9 , 9.5 , 10 , 10.5 , 11 , 11.5 , 12 , 12.5 , 13 , 13.5 , 14 , 14.5 , 15 , 15.5 , 16 , 16.5 , 17]
#y = [2 , 3.5 , 4 , 1 , 2.5 , 6 , 10 , 6 , 7 , 8 , 3 , 1.4 , 2.5 , 3 , 4 , 5 , 2 , 1 , 0 , -5 , 5 , 3 , 4 , 5 , 6 , 4 , 4 ,5 , 8 , 10.5 , 10.9 , 11 , 12.4 , 8.2 , 5]

[Tree , Iteration , CalculationTime] = GPAlgorithm(Population=Population , x=x , y=y)
Fx = list()
Delta = list()
for s in x:
    Fx.append(EvaluateExpressionTree(root=Tree , s=s))
os.system('cls||clear') 
print('Iteration:', Iteration)
print('Competency', Tree.Probability)  
print('RunTime is:',time.time() - start_time)
print('Time we calculate Compentency:' , Iteration*CalculationTime)
A = PrintExpressionTree(Tree)
print(A)
Sum = 0
for i in range(len(y)):
    Delta.append(abs(y[i]-Fx[i]))
    Sum = Sum + abs(y[i] - Fx[i])
if Sum == 0:
    plt.plot(x , Fx , 'k')
    plt.plot(x , Delta , 'c')
    plt.show()
else:
    plt.plot(x , y , 'r')
    plt.plot(x , Fx , 'b')
    #plt.plot(x , Delta , 'g')
    plt.show()
