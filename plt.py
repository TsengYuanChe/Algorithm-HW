import pandas as pd
import matplotlib.pyplot as plt


datas = ['ran','loc','cyc']
results = ['page_faults', 'interrupts', 'disk_writes']

for x in datas:
    df1 = pd.read_csv('fifodata/fifocyc.csv')  
    df2 = pd.read_csv('optdata/optcyc.csv')  
    df3 = pd.read_csv('excdata/exccyc.csv')  
    for y in results:
        plt.plot(df1['frame_sizes'], df1[f'{y}'], label="FIFO", color='blue', marker='o')
        plt.plot(df2['frame_sizes'], df2[f'{y}'], label="Optimal", color='green', marker='x')
        plt.plot(df3['frame_sizes'], df3[f'{y}'], label="ESC", color='red', marker='s')

        plt.xlabel("frame_sizes")
        plt.ylabel(f"{y}")
        plt.title(f"{y} of {x}")

        plt.legend()

        plt.savefig(f'resultplt/{y}_{x}.png')

        plt.show()