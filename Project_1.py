import mysql.connector
import networkx as Nt

# Connecting to database server
cnx = mysql.connector.connect(host='172.16.34.1', port='3307', user='umls', password='umls', database='umls2019')

# Creating a cursor for execution of queries
cursor = cnx.cursor()
query = 'SELECT CUI1, CUI2, RELA FROM MRREL limit 10000'
cursor.execute(query)

# Building graph of CUIs
G = Nt.DiGraph()
for cui1, cui2, rela in cursor:
    G.add_edge(cui1, cui2)

# Function for checking the cycles in graph
def D_C(node, graph, explored, p):
    explored.add(node)
    p.append(node)
    for S_N in graph[node]:
        if S_N in p:
            return True
        if S_N not in explored:
            if D_C(S_N, graph, explored, p):
                return True
    path.pop()
    return False

# Check for cycles in the graph
n_cycles = 0
for node in G:
    explored = set()
    path = []
    if D_C(node, G, explored, path):
        path.append(path[0])
        if len(path)>4:
            print(path)
            n_cycles += 1
            if n_cycles == 5:
                break

# Close cursor
cursor.close()

# Close the connection with the database
cnx.close()