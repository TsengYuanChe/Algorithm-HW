# Algorithm_HW

This main.py contains four algorithms and three ways of generating data string. It generate all the result automatically. Then using plt.py to obtain the graphics.

# main.py (My Algorithm='myal')
Setting the parameters x from 0 to 3, y from 0 to 2, with two loops I obtain all the result.
The fixed parameters are frame_sizes, num_references, and page_range which are equal to the given values in HW.pdf.
Each algorithm and each database will give a dataframe which include four columns 'frame_sizes', 'page_faults_results',  'interrupts_results', and 'disk_writes_results', and each column in dataframe has 10 values.
Overall I obtain 12 dataframes, they are saved in the files 'myaldata', 'fifodata', 'optdata', and 'excdata' named by the corresponding algorithm, and the name of the csv files are determined by the name of the algorithm and the way of generating database.

# plt.py
In this program, I plot the datas. In a given plot, x-axis are frame_sizes, y-axis are 'page_faults_results',  'interrupts_results', or 'disk_writes_results', the databases are the same and the three lines are correspond to different algorithms.
Overall nines plot, all of them are saved in resultplt, they are named by the combination of database and results.

# com.py
Comparing my algorithm and FIFO.
There is 3 kinds of database and each of them can generate parameters 'page fault' and 'cost' to compare wich algorithm is better.
According to previous line, my algorithm and FIFO can fight to each other 60 times, so I generate a dataframe with 60 data included, when the value is equal to '1' means my algorithm wins and '0' means FIFO wins.
So I calculate the numbers of '1' and '0' and make them to be the file name, so we can easily observe ehich one wins.

# test.py
Ignore it.
