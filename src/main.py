from data_model import DataSet


def create_data():
    filename = input('filename:')
    covid = DataSet(filename)
    while((x:=input('?'))!='q'):
        covid.input_data()
        covid.write_data()

# with open('data.json', 'w') as fp:
#     fp.write('[]')

data_set = DataSet('../data/data.json')
data_set.write_graph_covid_video(all_data=True)
data_set.write_graph_covid_video(all_data=False)
data_set.write_graph_covid_png(all_data=True)
data_set.write_graph_covid_png(all_data=False)
print(data_set)


