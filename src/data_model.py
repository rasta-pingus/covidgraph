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

    def write_graph_covid_video(self, all_data=True):
        suspected = [x['suspected'] for x in self.data_set]
        discarded = [x['discarded'] for x in self.data_set]
        discarded_tested = [x['discarded_tested'] for x in self.data_set]
        confirmed = [x['confirmed'] for x in self.data_set]
        healed = [x['healed'] for x in self.data_set]
        deaths = [x['deaths'] for x in self.data_set]

        # uti = [x['uti'] for x in self.data_set]
        # uti_max = [5 for _ in self.data_set]

        notifications = [sum(x) for x in zip(suspected, discarded, confirmed)]
        tests = [sum(x) for x in zip(confirmed, discarded_tested)]

        inbetween_confirmed = [x[0]-x[1]-x[2] for x in zip(confirmed, deaths, healed)]

        x = [datetime.strptime(x['date'],"%d %m %y").date() for x in self.data_set]

        fig, ax = plt.subplots()

        formatter = mdates.DateFormatter("%d/%m")
        ax.xaxis.set_major_formatter(formatter)

        locator = mdates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(locator)        

        ax.set_xlim(x[0],x[-1])
        fig.suptitle('COVID Leopoldina')

        def init():
            green_patch = mpatches.Patch(color='green', label='Curados')
            red_patch = mpatches.Patch(color='red', label='Infectados')
            black_patch = mpatches.Patch(color='black', label='Mortes')

            if all_data:
                line_confirmed, = ax.plot(x[0],tests[0], ':', color='black', label='Total de testes')
            
                yellow_patch = mpatches.Patch(color='lightyellow', label='Notificações')
                blue_patch = mpatches.Patch(color='lightcyan', label='Testes Negativos')

                legend = ax.legend(handles=[yellow_patch, line_confirmed, blue_patch, green_patch, red_patch, black_patch], loc='upper left')

            else:
                line_confirmed, = ax.plot(x[0],confirmed[0], color='black', label='Testes positivos')
                
                legend = ax.legend(handles=[line_confirmed, green_patch, red_patch, black_patch], loc='upper left')

        
        def animate(i):
            if all_data:
                ax.plot(x[:i],tests[:i], ':', color='black')
                ax.fill_between(x[:i],notifications[:i], color='lightyellow')
                ax.fill_between(x[:i],tests[:i], color='lightcyan')
            else:
                ax.plot(x[:i],confirmed[:i], color='black')
            
            ax.fill_between(x[:i],confirmed[:i], color='green')
            ax.fill_between(x[:i],inbetween_confirmed[:i], color='darkred')
            ax.fill_between(x[:i],deaths[:i], color='black')

        ani = animation.FuncAnimation(
            fig, animate, init_func=init, interval=20)

        dpi = 350
        writer = animation.writers['ffmpeg'](fps=10)

        filepath = '../data/covid_graph'
        filepath += '_all.mp4' if all_data else '.mp4'

        ani.save(filepath, writer=writer, dpi=dpi)
        

        # plt.show()



    
    def write_graph_covid_png(self, all_data=True):
        suspected = [x['suspected'] for x in self.data_set]
        discarded = [x['discarded'] for x in self.data_set]
        discarded_tested = [x['discarded_tested'] for x in self.data_set]
        confirmed = [x['confirmed'] for x in self.data_set]
        healed = [x['healed'] for x in self.data_set]
        deaths = [x['deaths'] for x in self.data_set]

        # uti = [x['uti'] for x in self.data_set]
        # uti_max = [5 for _ in self.data_set]

        notifications = [sum(x) for x in zip(suspected, discarded, confirmed)]
        tests = [sum(x) for x in zip(confirmed, discarded_tested)]

        inbetween_confirmed = [x[0]-x[1]-x[2] for x in zip(confirmed, deaths, healed)]

        x = [datetime.strptime(x['date'],"%d %m %y").date() for x in self.data_set]

        fig, ax = plt.subplots()

        formatter = mdates.DateFormatter("%d/%m")
        ax.xaxis.set_major_formatter(formatter)

        locator = mdates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(locator)        

        fig.suptitle('COVID Leopoldina')

        green_patch = mpatches.Patch(color='green', label='Curados')
        red_patch = mpatches.Patch(color='red', label='Infectados')
        black_patch = mpatches.Patch(color='black', label='Mortes')

        if all_data:
            line_confirmed, = ax.plot(x,tests, ':', color='black', label='Total de testes')
            ax.fill_between(x,notifications, color='lightyellow')
            ax.fill_between(x,tests, color='lightcyan')
            yellow_patch = mpatches.Patch(color='lightyellow', label='Notificações')
            blue_patch = mpatches.Patch(color='lightcyan', label='Testes Negativos')

            legend = ax.legend(handles=[yellow_patch, line_confirmed, blue_patch, green_patch, red_patch, black_patch], loc='upper left')

        else:
            line_confirmed, = ax.plot(x,confirmed, color='black', label='Testes positivos')
            
            legend = ax.legend(handles=[line_confirmed, green_patch, red_patch, black_patch], loc='upper left')

        ax.fill_between(x,confirmed, color='green')
        ax.fill_between(x,inbetween_confirmed, color='darkred')
        ax.fill_between(x,deaths, color='black')

        filepath = "../data/covid_graph"
        filepath += '_all.png' if all_data else '.png'

        plt.savefig(filepath, dpi=300)