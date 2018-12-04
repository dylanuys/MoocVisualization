# MoocVisualization
Research project exploring how data visualizations can be used to improve both cognitive engagement for students and iterative content development for educators in massive open online courses. 

## Supporting Infrastucture (Proposed) 
### MOOC Feedback System
We propose a system for allowing students to provide feedback that instructors can use for both immediate action and iterative course improvement. The existence of the proposed system would facilitate the development of visualizations similar to what we explore here, the goals of which are to improve cognitive engagement of students and to provide educators with valuable insights to help them improve their content. 

#### Core Feature for Students
* If a student experiences confusion when watching a MOOC video, they can pause and click on the area of the screen associated with their confusion.
* i.e., each flag (click) corresponds to one (x,y,time) point in the video 
* In aggregate, these data points can be used to visualize what was generally confusing to students for a given video


#### Core Feature for Instructors
* The system will present the aggregate student confusion points (described above as (x,y,time) points) to the instructor in an easily-intepreted fashion. 
* There are a multitude of ways to do this, and an ideal tool would implement a number of visualizations to maximize how many inisights an instructor is able to make. 
* The visualization we explore involves two main components, described in detail in the next section:
    * A video annotated with the (x,y,time) confusion clicks in the form of a heatmap
    * A video player annotated with confusion click frequencies in the form of ticks and a histogram


## Visualization Components (Implemented) 
The main goal is to create a graphical tool where, for a given MOOC video, a viewer can easily identify time intervals wherein students expressed confusion and to subsequently identify areas on the screen at that time relevant to the confusion.

The dataset visualized is the collection of (x,y,time) student confusion clicks desribed in previous sections. There are two components of our visualization, described below, that communicate the data differently. 


### Heatmapped Video
The first component is a heatmap overlaid on the video, so this would require postprocessing with both the original video file and the collection of student clicks available on-hand. 
Each (x,y,time) confusion click is represented as a light blue point on the video. As these occur in clusters around the same areas in space-time, these blue points group together to form warmer colors, as shown in the gif below.



### Custom Video Player

          
          
### Together:

![The Big Picture](res/vis1.gif)


# Implementation Details
Our implementation involves mostly Python3, HTML5, CSS, Javascript. This section provides a high level overview of the different tasks that the code in this repository accomplishes. Please see the end of each section for notes on where to look for specific code relevant to these tasks. 

### Data Mocking
Because the system we proposed doesn't exist (yet), we had to generate data that resembles human clicks. For the sake of automating away the menial, we chose the following approach.

For simplicity, consider one possible point of confusion in a video. Let's say that we'd expect students to click on the point (x = 100 pixels, y = 100 pixels, time = 30s), because it has some fancy looking formula or something of the sort. 
Our goal in the mocking process is to then generate a group of points around (100,100) in space and around 30s in time. 
To accomplish this, we generate three Gaussian distributions - one for x, one for y and one for time.
* The x and y distributions are centered at 100, and the script gives them default standard deviations of 20
   * For cases where it makes more intuitive sense for the distributions to be "taller" or "wider" to cover a certain area of the screen, this default is overriden in a manual trial/error manner on a case by case basis. 
* The time distribution (actually in milliseconds in the script) is centered at 30,000 and has a default standard deviation of 1500ms.   
   * For cases where it makes more intuitive sense for the points to be more spread out over time, this default is overriden in the same way as the x and y standard deviations are. 
* Each distribution has a default sample size of 1000. This is very loosely based on the following assumptions:
   * Our visualization assumes the video and its corresponding click data is sampled from somewhere in the second half corresponding MOOC, after many of the lurkers and unsure students have stopped actively participating or dropped. 
   * Typical MOOCs enroll around 43,000 students
   * 6.5% of these students finish the course
   * With 2,795 students finishing the course, a very loose estimate would be to say around 1,000 students would express confusion at times where the instructor could have been more clear about something.
* With these three distributions generated for one given point of confusion, each point added to the video comes from sampling these distributions like this (taken from `heatmapper.py`):

```python
  # for each point of confusion,
  x_gaus = np.random.normal(x, x_std, num_points)
  y_gaus = np.random.normal(y, y_std, num_points)
  ms_gaus = np.random.normal(ms, ms_std, num_points)

  for i in range(num_points):
      point = (x_gaus[i], y_gaus[i], ms_gaus[i])
      self.heat_points.append(point)
```
   
*Relevant code*:
The `HeatMapper` class found in `heatmapper.py` generates this dataset in the `load_data()` method. Specifically, for every line in the input file (corresponding to a single point of potential confusion), `add_point_distribution()` is called to generate the x,y, and time distributions described above. Once the whole input file is processed, HeatMapper's `heat_points` attribute is populated as a list of (x,y,time) tuples. Read the next section to see how these are used. 

### Heatmapped Video
Overlaying a heatmap on a video is accomplished with the ![heatmappy](https://github.com/LumenResearch/heatmappy) Python library. 
The library accepts tuples with (x,y,millisecond) fields, so we simply feed in the datset described above.


### Custom Video Player
In order to display the frequency of clicks along the x-axis of our video, we also had to create a custom video player using HTML5, CSS



## Potential extensions
* Linkage of confusion points with class forum 
    * Allow students to create a class forum post associated with with a confusion click without leaving their current wepage
    * There could then exist a bidirectional relationship between forum posts and (x,y,time) points in the video, increasing the cohesiveness of the MOOC system as a whole.
          * This could also help short-circuit instructor intervention by facilitating student-student help
    
* In addition to the basic (x,y,time) attributes of each point of confusion, it may prove useful to allow students to also associate a "type" of confusion with a given click. Since our visualization uses only x,y and time, these are out of the scope of this project. Potential types could include the following:
    * General -- student is generally confused on the topic
    * Notation -- student doesn't understand the notation being used
    * Speech -- student didn't understand what the instructor said
          * This would be a case where x and y aren't relevant, which points towards the need for entirely different methods for visualization
          



