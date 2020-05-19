from collections import defaultdict 
import collections
import itertools

# finds shortest path between 2 nodes of a graph using BFS
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph.keys():
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

if __name__ == '__main__':
    orDict=defaultdict(list) 
    graph="New York->New Jersey,New Jersey->Boston,Boston->Philadelphia,New York->Washington,New York->Miami,New Jersey->Houston,Boston->Houston,Miami->Austin,Los Angeles->New Jersey,Los Angeles->Philadelphia,San Francisco->Las Vegas,Las Vegas->Washington,Houston->Las Vegas,Chicago->New Jersey,Los Angeles->Chicago"
    pair=[x.strip() for x in graph.split(',')]
  
    city = []
    for i in pair:
        city.append(i.split('->'))
        
    for key, val in city: 
        orDict[key].append(val) 
    
    finalGraph = dict(orDict)
    
    total = []
    for i in city:
        total += i

    ulist=set(total)
    ulist2=total
    spairs=list(itertools.permutations(ulist2,2))
    all_combinations = []
    for each_permutation in spairs:
        zipped = zip(each_permutation, ulist)
        all_combinations.append(list(zipped))
    
    for i in all_combinations:
        distance=0
        start=i[0][0]
        goal=i[1][0]
        path=find_shortest_path(finalGraph, start, goal)
        if path is None:
            distance=-1
        else:
            distance= len(path)-1
        print(start+', '+ goal+ ':', distance)