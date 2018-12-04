import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import ipdb

samples = pd.read_csv('./data/samples.csv')

# Save clicks as percentage of video for D3
video_length = 450*1000
clicks = (100*samples.ms/video_length) # convert to percentage of video length
clicks.to_csv('./data/clicks.csv', index=False, float_format='%.2f', header=['click'])

# Create histogram for bottom of webpage
ipdb.set_trace()
bar = plt.hist(samples.ms/1000, np.arange(0, 455, 20))
sec_to_min = lambda time: '%.2i:%.2i' % (time/60, time%60)
bins = [sec_to_min(el) for el in bar[1][1:]]
pd.DataFrame({'time':bins, 'value':bar[0]}).to_csv('./data/bar-data.csv', index=False)
