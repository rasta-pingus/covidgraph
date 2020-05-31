import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from datetime import datetime
import json


class DataSet:

    def __init__(self, file_str):
        self.file = file_str
        with open(self.file, 'r') as fp:
            self.data_set = json.load(fp)

    def add_data(self, data):
        self.data_set.append(data)

    def write_data(self):
        with open(self.file, 'w') as fp:
            json.dump(self.data_set, fp)

    def get_data_by_date(self, date_str):
        return [x for x in self.data_set if x['date']==date_str]

    def input_data(self):
        date = input('date:')
        suspected = int(input('suspected:'))
        discarded = int(input('discarded:'))
        discarded_tested = int(input('discarded tested:'))
        confirmed = int(input('confirmed:'))
        uti = int(input('uti:'))
        healed = int(input('healed:'))
        deaths = int(input('deaths:'))
        data_dict = {
            'date': date,
            'suspected': suspected,
            'discarded': discarded,
            'discarded_tested': discarded_tested,
            'confirmed': confirmed,
            'uti': uti,
            'healed': healed,
            'deaths': deaths
        }
        self.add_data(data_dict)

    def __str__(self):
        string = ""
        for data in self.data_set:
            string += f"\nDia: {data['date']} \n"
            string += f"Suspeito: {data['suspected']} \n"
            string += f"Descartado: {data['discarded']} \n"
            string += f"Descartado por teste: {data['discarded_tested']} \n"
            string += f"Confirmado: {data['confirmed']} \n"
            string += f"Em UTI: {data['uti']} \n"
            string += f"Curado: {data['healed']} \n"
            string += f"Mortes: {data['deaths']} \n"
        return string

    def graph_covid(self):
        suspected = [x['suspected'] for x in self.data_set]
        discarded = [x['discarded'] for x in self.data_set]
        discarded_tested = [x['discarded_tested'] for x in self.data_set]
        confirmed = [x['confirmed'] for x in self.data_set]
        # uti = [x['uti'] for x in self.data_set]
        healed = [x['healed'] for x in self.data_set]
        deaths = [x['deaths'] for x in self.data_set]

        # uti_max = [5 for _ in self.data_set]

        notifications = [sum(x) for x in zip(suspected, discarded, confirmed)]

        inbetween_confirmed = [x[0]-x[1]-x[2] for x in zip(confirmed, deaths, healed)]

        x = [datetime.strptime(x['date'],"%d %m %y").date() for x in self.data_set]

        fig, ax = plt.subplots()

        formatter = mdates.DateFormatter("%d/%m")
        ax.xaxis.set_major_formatter(formatter)

        locator = mdates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(locator)

        ax.yaxis.set_major_locator(ticker.IndexLocator(base=5, offset=0))
        ax.set_ylim(ymin=-0.5,auto=True)

        ax.set_ylabel('Número total de casos', fontweight="bold", fontsize="14")
        

        ax.set_xlim(x[0],x[-1])
        fig.suptitle('COVID Leopoldina')

        def init():
            ax.plot(x[0],inbetween_confirmed[0], color='darkred')
            ax.plot(x[0],confirmed[0], color='black', label='Total de casos')
            ax.plot(x[0], deaths[0], color='black')
            # ax.plot(x[0], uti[0], '--', label='Leitos UTI ocupados')
            # ax.plot(x[0], uti_max[0], '--', color='red', label='Leitos UTI disponíveis')
            legend2 = ax.legend(loc='upper left', shadow=False, fontsize='medium')
            green_patch = mpatches.Patch(color='green', label='curados')
            red_patch = mpatches.Patch(color='red', label='infectados')
            black_patch = mpatches.Patch(color='black', label='mortos')
            legend = ax.legend(handles=[green_patch, red_patch, black_patch], loc='center left')

            ax.add_artist(legend2)

        
        def animate(i):
            # try:
            #     if confirmed[i]>5:
            #         ax.set_ylim(auto=True)
            # except IndexError:
            #         ax.set_ylim(auto=True)
            # ax.plot(x[:i],inbetween_confirmed[:i], color='darkred')
            ax.plot(x[:i],confirmed[:i], color='black', label='Total de casos')
            # ax.plot(x[:i], deaths[:i], color='black')
            # ax.plot(x[:i], uti[:i], '--', color='lightblue', label='Leitos UTI ocupados')
            # ax.plot(x[:i], uti_max[:i], '--', color='red', label='Leitos UTI disponíveis')
        
            ax.fill_between(x[:i],confirmed[:i], color='green')
            ax.fill_between(x[:i],inbetween_confirmed[:i], color='darkred')
            ax.fill_between(x[:i],deaths[:i], color='black')

        ani = animation.FuncAnimation(
            fig, animate, init_func=init, interval=20)

        dpi = 350
        writer = animation.writers['ffmpeg'](fps=10)
        ani.save('data/covidgraph.mp4', writer=writer, dpi=dpi)
        

        # plt.show()


        # ax.plot(x,confirmed, color='black', label='Total de casos')
        # ax.plot(x,inbetween_confirmed, color='darkred')
        # ax.plot(x, deaths, color='black')
        # ax.plot(x, uti, '--', label='Leitos UTI ocupados')
        # ax.plot(x, uti_max, '--', color='red', label='Leitos UTI disponíveis')

        # ax.fill_between(x,confirmed,alpha=0.5,color='green')
        # ax.fill_between(x,inbetween_confirmed,alpha=0.5,color='red')
        # ax.fill_between(x,deaths,alpha=1,color='black')
        # ax.fill_between(x,uti,alpha=0.2,color='lightblue')

        # green_patch = mpatches.Patch(color='green', label='curados')
        # red_patch = mpatches.Patch(color='red', label='infectados')
        # black_patch = mpatches.Patch(color='black', label='mortos')
        # legend = ax.legend(handles=[green_patch, red_patch, black_patch], loc='center left')

        # fig.suptitle('COVID leopoldina')
        # legend2 = ax.legend(loc='upper left', shadow=False, fontsize='x-large')
        # ax.add_artist(legend)

        # ax.set_ylabel('Número total de casos', fontweight="bold", fontsize="14")

        # plt.show()
    
    def graph_covid2(self):
        suspected = [x['suspected'] for x in self.data_set]
        discarded = [x['discarded'] for x in self.data_set]
        discarded_tested = [x['discarded_tested'] for x in self.data_set]
        confirmed = [x['confirmed'] for x in self.data_set]
        uti = [x['uti'] for x in self.data_set]
        healed = [x['healed'] for x in self.data_set]
        deaths = [x['deaths'] for x in self.data_set]

        uti_max = [5 for _ in self.data_set]

        notifications = [sum(x) for x in zip(suspected, discarded, confirmed)]

        tests = [sum(x) for x in zip(confirmed, discarded_tested)]

        x = [datetime.strptime(x['date'],"%d %m %y").date() for x in self.data_set]

        fig, ax = plt.subplots()

        formatter = mdates.DateFormatter("%d/%m")
        ax.xaxis.set_major_formatter(formatter)

        locator = mdates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(locator)

        ax.set_xlim(x[0],x[-1])
        fig.suptitle('COVID Leopoldina')

        def init():
            ax.plot(x[0], notifications[0], color='black', label='Notificações')
            ax.plot(x[0], tests[0], color='green', label='Testes realizados')
            ax.plot(x[0], confirmed[0], color='darkred',label='Testes Positivos')
            plt.legend(loc='upper left', shadow=False, fontsize='medium')


        def animate(i):

            ax.plot(x[:i], notifications[:i], color='black', label='Notificações')
            ax.plot(x[:i], tests[:i], color='green', label='Testes realizados')
            ax.plot(x[:i], confirmed[:i], color='darkred',label='Testes Positivos') 

            ax.fill_between(x[:i],notifications[:i],alpha=0.5,color='yellow')
            ax.fill_between(x[:i],tests[:i],alpha=0.8,color='green')
            ax.fill_between(x[:i],confirmed[:i],alpha=0.9,color='red')

        ani = animation.FuncAnimation(
            fig, animate, init_func=init, interval=20)

        ani.save('data/covidgraph2.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

        # plt.show()

# class Data:
#     def __init__(self, **kwargs):
#         self.date = kwargs.get('date')
#         self.suspected = kwargs.get('suspected')
#         self.discarded = kwargs.get('discarded')
#         self.disarded_tested = kwargs.get('disarded_tested')
#         self.confirmed = kwargs.get('confirmed')
#         self.healed = kwargs.get('healed')
#         self.deaths = kwargs.get('deaths')

    