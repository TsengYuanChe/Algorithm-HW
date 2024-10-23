# Algorithm_HW

This main.py contains three algorithms and three ways of generating data string. It generate all the result automatically. Then using plt.py to obtain the graphics.

# main.py
Setting the parameters x,y from 0 to 2, with two loops I obtain all the result.
The fixed parameters are frame_sizes, num_references, and page_range which are equal to the given values in HW.pdf.
Each algorithm and each database will give a dataframe which include four columns 'frame_sizes', 'page_faults_results',  'interrupts_results', and 'disk_writes_results', and each column in dataframe has 10 values.
Overall I obtain nine dataframes, they are saved in the files 'fifodata', 'optdata', and 'excdata' named by the corresponding algorithm, and the name of the csv files are determined by the name of the algorithm and the way of generating database.

# plt.py
In this program, I plot the datas. In a given plot, x-axis are frame_sizes, y-axis are 'page_faults_results',  'interrupts_results', or 'disk_writes_results', the databases are the same and the three lines are correspond to different algorithms.
Overall nines plot, all of them are saved in resultplt, they are named by the combination of database and results.

# test.py
Ignore it.
