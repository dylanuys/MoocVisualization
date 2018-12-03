# MoocVisualization
Research project exploring how data visualizations can be used to improve both cognitive engagement for students and iterative content development for educators in massive open online courses. 

## (Proposed) Supporting Infrastucture 
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


## (Implemented) Visualization Components

![Visualization Demo Gif](gif1.gif)


### Heatmapped Video

### Custom Video Player


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
          
