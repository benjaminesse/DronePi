import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation

# Set filepath for results folders
fpath = '/home/pi/PiSpec/Results'

# Get all the results folders
results_folders = [
    f for f in os.listdir(fpath) if os.path.isdir(f'{fpath}/{f}')
]

# Find the latest
results_folders.sort()
folder = results_folders[-1]

# Set the path to the SO2 output file
fname = f'{fpath}/{folder}/so2_output.csv'

print(fname)

# Make the plots
plt.ion()
fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(
    2, 2, figsize=[10, 6]
)

ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax2.set_xlabel('Time (UTC)')
ax2.set_ylabel('Altitude (m a.s.l.)')
ax3.set_xlabel('Time (UTC)')
ax3.set_ylabel('SO$_2$ SCD (ppm.m)')

for ax in [ax2, ax3]:
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%H:%M:%S")
    ) 

# Make plot items
scat1, = ax1.plot([], [])
scat2, = ax2.plot([], [])
line1, = ax3.plot([], [])

# Define update function
while True:

    # Read in the results file
    df = pd.read_csv(fname, parse_dates=['Time'])

    scat1.set_data(df['Lon'], df['Lat'])
    scat2.set_data(df['Time'], df['Alt'])
    line1.set_data(df['Time'], df['SO2_SCD_ppmm'])
    
    for ax in [ax1, ax2, ax3, ax4]:
        ax.relim()
        ax.autoscale_view()
    plt.pause(0.01)
