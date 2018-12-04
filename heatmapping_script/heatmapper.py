from heatmappy import Heatmapper
from heatmappy import VideoHeatmapper
from PIL import Image
import numpy as np
import argparse
import os
import sys
import csv

''

class ClickMapper():

    def __init__(self, video_in_path, data_path, video_out_path, test_mode=False):
        '''
        Class to add a heatmap to a video. 

        Parameters:
            video_in_path  (str) -- Filepath to video to add the heatmap to
            video_out_path (str) -- Filepath to write heatmapped video to
            data_path      (str) -- Filepath to csv file containing coordinates 
                                    and times at which to add points for the 
                                    heatmap. Each line of data in the file should 
                                    be formatted (x, y, milliseconds, count). The 
                                    first three elements dictate where the point
                                    will be added in the video, and count 
                                    specifies how many random augmented points 
                                    to add around that location and time. 
        '''

        self.video_path = video_in_path
        self.data_path = data_path
        self.out_path = video_out_path
        self.test_mode = test_mode

        # to write to video
        self.heat_points = [] 
        # to export distribution points without missing values
        self.distributions = [] 

        self.load_data()
        
    
    def load_data(self):
        '''
        Loads the data found in self.data_path into self.heat_points. A line in
        the data file looks like this: (x,y,millisecond,count). Each line is
        passed to self.add_point_distribution, which creates a gaussian 
        distribution of "count" many points. For x and y, the default standard
        deviation used is 15. For the milliseconds, the default is 1000. All
        of these defaults can be changed by setting the optional fields in the
        data file. See self.add_point_distribution for details.
        
        Takes no arguments and returns nothing, populates self.heat_points.
        '''

        def is_int(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False

        with open(self.data_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader) # header

            for l in reader:
                bad_format = np.any([e != '' and not is_int(e) for e in l])
                if len(l) < 4: continue
                elif bad_format: continue

                self.add_point_distribution(l)



    def add_point_distribution(self, line):
        '''
        Creates gaussian distributions using values from the line argument.
        Line contains (x,y,ms,count,[duration,x_std_dev,y_std_dev]), where 
        the last three fields are optional. A distribution is created for each
        of x, y and ms, using count to define the number of samples. 

        '''


        x_std = int(line[4]) if len(line) > 4 and len(line[4]) > 0 else 15
        y_std = int(line[5]) if len(line) > 5 and len(line[5]) > 0 else 15
        ms_std = int(line[6]) if len(line) > 6 and len(line[6]) > 0 else 1500


        # convert to ints after using string properties above 
        line = [int(e) if len(e) > 0 else e for e in line] 
        x, y, ms, num_points = line[0], line[1], line[2], line[3]
        
        if self.test_mode: num_points //= 10
        x_gaus = np.random.normal(x, x_std, num_points)
        y_gaus = np.random.normal(y, y_std, num_points)
        ms_gaus = np.random.normal(ms, ms_std, num_points)         

        distr = (line[0], line[1], line[2], ms_std, x_std, y_std)
        self.distributions.append(distr)
        
        for i in range(num_points):
            point = (x_gaus[i], y_gaus[i], ms_gaus[i])
            self.heat_points.append(point)
            


    def apply_heatmap(self):
        '''
        Uses the heatmappy library to add points from self.heat_points to the 
        video in self.video_path. Takes no args and returns nothing, but creates
        a video with an overlaid heatmap at self.out_path.
        '''

        header = ['x','y','ms','x_std','y_std','ms_std']
        self.export_data('distributions.csv', self.distributions, header)
        self.export_data('samples.csv', self.heat_points, header[:3])

        img_hm = Heatmapper()
        video_hm = VideoHeatmapper(img_hm)
        video_out = video_hm.heatmap_on_video_path(video_path=self.video_path,
                                                   points=self.heat_points)
    
        video_out.write_videofile(self.out_path, bitrate="5000k", fps=24)


    def export_data(self, out_path, data, header=None, verbose=True):
        '''
        Writes a list of data points to a file. This is called to write
        the fully populated distributions and their corresponding samples
        to their own files for later reference. 

        Parameters:
            data     -- List of lists or tuples to write to csv file
            out_path -- filepath to write to
            
        '''

        if verbose: print('Exporting data to', out_path,'...',)
        with open(out_path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            if header is not None: writer.writerow(header)
            for point in data:
                p = [p for p in point] # in case of tuple
                writer.writerow(p)
        if verbose: print('done.\n' + '-'*50)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--video', metavar='v', default='kmeans.mp4', 
                        help='Path to input video file (default: kmeans.mp4)',
                        dest='video')
    parser.add_argument('--data', metavar='d', default='data.csv',
                        help='Path to data file (default: data.csv)',
                        dest='data')
    parser.add_argument('--mode', metavar='m', default='prod',
                        help='Set to "test" to use less points and execute '\
                             'faster (default: prod)',
                        dest='mode')
    args = parser.parse_args()

    video_path = args.video
    data_path = args.data
    test_mode = True if args.mode == 'test' else False
    out_path = video_path[:video_path.index('.')] + '_heatmapped.mp4'
    print('-'*50)
    print('Video in: {}\nData file: {}\nOutput file:{}'.format(video_path, 
                                                               data_path, 
                                                               out_path))
    print('-'*50)

    heatmapper = ClickMapper(video_path, data_path, out_path, test_mode)
    heatmapper.apply_heatmap()

