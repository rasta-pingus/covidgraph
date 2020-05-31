from data_model import DataSet


def create_data():
    filename = input('filename:')
    covid = DataSet(filename)
    while((x:=input('?'))!='q'):
        covid.input_data()
        covid.write_data()

# with open('data.json', 'w') as fp:
#     fp.write('[]')

data_set = DataSet('data/data.json')
data_set.graph_covid()
# print(data_set)


