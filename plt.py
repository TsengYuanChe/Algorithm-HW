import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('fifodata/fifocyc.csv')  
df2 = pd.read_csv('optdata/optcyc.csv')  
df3 = pd.read_csv('excdata/exccyc.csv')   

plt.plot(df1['frame_sizes'], df1['disk_writes'], label="FIFO", color='blue', marker='o')
plt.plot(df2['frame_sizes'], df2['disk_writes'], label="Optimal", color='green', marker='x')
plt.plot(df3['frame_sizes'], df3['disk_writes'], label="ESC", color='red', marker='s')

plt.xlabel("Frame Sizes")
plt.ylabel("Page Faults")
plt.title("Disk Writes of Cyclic Data")

plt.legend()

plt.savefig('resultplt/writes_cyc.png')

plt.show()