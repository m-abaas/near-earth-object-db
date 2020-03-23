from database import NEODatabase

x = NEODatabase('./data/neo_data.csv')
x.load_data()
print(x.date_to_NEOs)