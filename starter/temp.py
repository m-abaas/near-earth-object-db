from database import NEODatabase
from search import DateSearch

x = NEODatabase('./data/neo_data.csv')
x.load_data()
print(x.NEOs)
options = DateSearch.list()
print(options)