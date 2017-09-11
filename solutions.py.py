# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3rd 14:19:49 2017

@author: ypaparna
"""
import copy
## Question 1 -  Determine whether some anagram of t is a substring of s
'''
Given two strings s and t, determine whether some anagram of t is a substring 
of s. For example: if s = "udacity" and t = "ad", then the function returns 
True. Your function definition should look like: question1(s, t) and return a 
boolean True or False.
'''

def question1(s,t):
 ## if length of t is greater than s, t cannot be a sbustring of s   
    if len(t) > len(s):
          return False
### Loop through the characters in t and see if they are in s
##if the letter is in s, replace it with ""
    for i in t:
        if i not in s:
            return False
        else:
           s = s.replace(i, "",1) 
    return True
    
##Test Case 1
s= 'abcdef'
t = 'bc'    
print (question1(s,t))
##Expected Answer :  True

##Test Case 2
s= 'abcdef'
t = 'gh'    
print (question1(s,t))
##Expected Answer :  False

##Test Case 3
s= 'angrm'
t = 'ana'    
print (question1(s,t))
##Expected Answer :  False

######################################end of question 1

##Question 2  -- Find longest palindromic substring
'''
Given a string a, find the longest palindromic substring contained in a. Your 
function definition should look like question2(a), and return a string.
'''
# A Dynamic Programming based solution using Python
# Returns the length of the longest palindromic subsequence
def question2(a):
    n = len(a) 
    #create array to store results
    L = [[0 for x in range(n)] for x in range(n)]
 
    # Strings of length 1 are palindrome of length 1
    for i in range(n):
        L[i][i] = 1
 
    # The values in the matrix are filled in a
    # manner similar to Matrix Chain Multiplication. Result stored
    #in the right top corner of the matrix gives the length of the palindrome
    
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            if a[i] == a[j] and l == 2:
                L[i][j] = 2
            elif a[i] == a[j]:
                L[i][j] = L[i+1][j-1] + 2
            else:
                L[i][j] = max(L[i][j-1], L[i+1][j]);
               
 
    return L[0][n-1]

# Test Case 1
a = "racecar"
print("The length of the longest palindrome is  " + str(question2(a)))
##expected answer is 7

# Test Case 2
a = "abcdef"
print("The length of the longest palindrome is  " + str(question2(a)))
##expected answer is 1

# Test Case 3
a = "anagram"
print("The length of the longest palindrome is  " + str(question2(a)))
##expected answer is 3


######################################end of question 2

##Question 3 - Find the minimum spanning tree in an undirected graph
'''
Given an undirected graph G, find the minimum spanning tree within G. A 
minimum spanning tree connects all vertices in a graph with the smallest 
possible total weight of edges. Your function should take in and return an 
adjacency list structured like this:

{'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}

Vertices are represented as unique strings. The function definition should be 
question3(G)
'''

def create_edge_list(graph):
    """
   ## Convert the input format to one that can be used with this program
    """
    edge_list = []
    nodes_visited = {}

    for key in graph:
        nodes_visited[key] = 0
        for edge in graph[key]:
            new_edge = (edge[1], edge[0], key)
            edge_list.append(new_edge)

    return sorted(edge_list), nodes_visited


def convert_to_graph(edge_list):
    """
  ##  Convert the format back to a graph for display in the console
    """
    updated_graph = {}
    sorted_graph = {}

    # initalize a key mapped to an empty list
    for edge in edge_list:
        updated_graph[edge[2]] = []
        updated_graph[edge[1]] = []

    # populate the list for each key
    for edge in edge_list:
        updated_graph[edge[2]].append((edge[1], edge[0]))
        updated_graph[edge[1]].append((edge[2], edge[0]))

    # sort the dictionary alphabetically by key
    for key in sorted(updated_graph):
        sorted_graph[key] = updated_graph[key]

    return sorted_graph


def cycle_check(edge, paths):
    """
   ## Checks is a cycle exists with the addition of a given edge
    """
    if edge[1] in paths[edge[2]] or edge[2] in paths[edge[1]]:
        return True
    return False


def repeat_check(edge, edge_list):
    """
  ##  Checks if an edge is a repeat
    """
    reverse_edge = (edge[0], edge[2], edge[1])
    if reverse_edge in edge_list:
        return True
    return False


def update_paths(paths, node1, node2):
    """
    Updates the paths for each node. The path of each node includes all the
    other nodes it's connected to
    """
    n1 = copy.deepcopy(paths[node1])
    n2 = copy.deepcopy(paths[node2])

    for node in paths[node1]:
        paths[node].extend(n2)
    for node in paths[node2]:
        paths[node].extend(n1)

    paths[node1].extend(n2)
    paths[node2].extend(n1)
    paths[node1].append(node2)
    paths[node2].append(node1)

    return paths


def question3(graph):
    """
 ##   Takes in a graph and outputs a graph with an idealized path that connects
  ##  all nodes in the graph with the least total weight
    """
    if graph == {} or graph == None:
        return None

    edge_list, nodes_visited = create_edge_list(graph)
    updated_edges = []

    # initalize the paths for each node
    paths = {}
    for edge in edge_list:
        paths[edge[2]] = []

    for edge in edge_list:
        is_cycle = cycle_check(edge, paths)
        is_repeat = repeat_check(edge, updated_edges)
        if len(updated_edges) == len(nodes_visited)-1 or is_cycle or is_repeat:
            continue

        if nodes_visited[edge[1]] == 0 or nodes_visited[edge[2]] == 0:
            # sets the status of each node in this operation to 1 for 'visited'
            nodes_visited[edge[1]] = 1
            nodes_visited[edge[2]] = 1

            paths = update_paths(paths, edge[1], edge[2])
            updated_edges.append(edge)
        elif nodes_visited[edge[1]] == 1 and nodes_visited[edge[2]] == 1:
            paths = update_paths(paths, edge[1], edge[2])
            updated_edges.append(edge)

    return convert_to_graph(updated_edges)

#Test Case1
G1 = {'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}
print(question3(G1))
# Expected result: {
#{'C': [('B', 5)], 'B': [('A', 2), ('C', 5)], 'A': [('B', 2)]}

#Test Case2
G2 = {}
print(question3(G2))
# Expected result: None

#Test Case3
G3 = {
    'A': [('B', 9),('C', 3),('D', 2)],
    'B': [('A', 9),('C', 8),('H', 9)],
    'C': [('A', 3),('B', 8),('D', 7),('E', 6),('F', 1)],
    'D': [('A', 2),('C', 7),('I', 10)],
    'E': [('C', 6),('G', 3)],
    'F': [('C', 1),('G', 5),('I', 8)],
    'G': [('E', 3),('F', 5)],
    'H': [('B', 9),('I', 4)],
    'I': [('D', 10),('F', 8),('H', 4)]
}
print(question3(G3))
# Expected result: {
# 'A': [('D', 2), ('C', 3)],
# 'B': [('C', 8)],
# 'C': [('F', 1), ('A', 3), ('B', 8)],
# 'D': [('A', 2)], 'E': [('G', 3)],
# 'F': [('C', 1), ('G', 5), ('I', 8)],
# 'G': [('E', 3), ('F', 5)],
# 'H': [('I', 4)],
# 'I': [('H', 4), ('F', 8)]
# }
######################################end of question 3


##Question 4 - Find the least common ancestor
'''
  Find the least common ancestor between two nodes on a binary search tree. 
  The least common ancestor is the farthest node from the root that is an 
  ancestor of both nodes. For example, the root is a common ancestor of all 
  nodes on the tree, but if both nodes are descendents of the root's left 
  child, then that left child might be the lowest common ancestor. You can 
  assume that both nodes are in the tree, and the tree itself adheres to all 
  BST properties. The function definition should look like 
  question4(T, r, n1, n2), where T is the tree represented as a matrix, 
  where the index of the list is equal to the integer stored in that node and 
  a 1 represents a child node, r is a non-negative integer representing the 
  root, and n1 and n2 are non-negative integers representing the two nodes in
  no particular order. For example, one test case might be

question4([[0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          4)

and the answer would be 3.
'''
     
def question4(T, r, n1, n2):
  if not T or r is None or n1 is None or n2 is None:
    return None
  # if n1 and n2 are on oposing sides from the root
  if (n1 <= r and n2 >= r) or (n1 >= r and n2 <= r):
    return r
  if n1 == n2:
    return n1

  # make sure n2 is the most distant from the root
  if abs(n2 - r) < abs(n1 - r):
    aux = n1
    n1 = n2
    n2 = aux

  # go up from n2 until the value crosses n1 
  lca = n2
  n2 = get_parent(T, lca)
  while abs(n2 - r) > abs(n1 - r):
    lca = n2
    n2 = get_parent(T, lca)
    
  return lca

""" Returns the parent of the specified node or None if it does not have one """
def get_parent(T, n):
  for idx, row in enumerate(T):
    if row[n] == 1:
      return idx
  return None

#Test case 1
print (question4(None, None, None, None))
# Expected Result
# None
#Test case 2
print (question4([[0]],
                0,
                0,
                0))
# Expected Result
# 0
#Test case 3
print (question4([[0, 0, 1, 0],
                 [0, 0, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 0]],
                0,
                1,
                3))
#Expected result
# 2
#Test case 4
print (question4([[0,1,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [1,0,0,0,1],
                  [0,0,0,0,0]],3,1,4))
#Expected result
#3
######################################end of question 4
##Question 5 - Find the mth element in linked list from the end.
'''
 Find the element in a singly linked list that's m elements from the end. For 
 example, if a linked list has 5 elements, the 3rd element from the end is the 
 3rd element. The function definition should look like question5(ll, m), where
 ll is the first node of a linked list and m is the "mth number from the end".
 You should copy/paste the Node class below to use as a representation of a 
 node in the linked list. Return the value of the node at that position.
'''

def question5(ll, m):
    if m <1:
        return None
    end_pointer = ll
    mid_pointer = ll
    for num in range(m):
        end_pointer = end_pointer.next  
    while end_pointer:  # Advance end pointer through complete ll
        end_pointer = end_pointer.next
        mid_pointer = mid_pointer.next # midpointer will land at the right node
    return mid_pointer.data

### create a Node class

class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None
    
# Build a linked list with n nodes
def build_ll(n):
    root = Node(1)
    current_node = root
    for num in range(n-1):
        new_node = Node(num + 2)
        current_node.next = new_node
        current_node = new_node
    return root

if __name__ == '__main__':
##Test case 1
    root = build_ll(5)
    print (question5(root,3))
##expected result
# 3
##Test case 2
    root = build_ll(13)
    print (question5(root,-2))
##expected result
# None
##Test case 3
    root = build_ll(13)
    print (question5(root,2))
##expected result
# 12


    
