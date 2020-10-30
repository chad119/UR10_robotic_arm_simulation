# UR10_robotic_arm_simulation
## self_project

In this project, I simulate UR10 robotic on URsim, ur_Gazebo and RVIZ to test impedance control and test moveit.
- **Part0 Before everything...**
1. Prepare **Ubuntu** and **ROS**.
2. Go to this [URsim](https://www.universal-robots.com/download/?option=77050#section41511) website to install simulator.
3. ```roscore```
4. [Download File](https://drive.google.com/file/d/1AuNgwq2Hneshwn6qzMy3e9v8-j8I9Aeq/view?usp=sharing) and ```catkin_make``` file.
- **Part 1 UR10 moving test**  
  - In this part, I use UR10 to move on xy plane along with a line.  
    1. Open UR10 simulator
    2. Go to check your IP (Use ```ip addr show```)
    3. ```roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=<YOUR IP>```
    4. ```roslaunch ur_gazebo ur10_impedance_control.launch```
    5. ```rosrun impedance_control_test moving_node.py```
- **Part 2 UR10 impedance control simulation**  
  - In this part, I set a virtual surface that have a sine-like surface. We will apply impedance control when UR10 move according to the surface and keep the TCP (tool center point) have 10N force.
    1. Open UR10 simulator
    2. ```roslaunch ur_robot_driver ur10_bringup.launch robot_ip:=<YOUR IP>```
    3. ```roslaunch ur_gazebo ur10_impedance_control.launch```
    4. ```rosrun impedance_control_test sine_force_node.py``` This will apply a virtual sine-like force to the UR10 to simulate the sine-like surface and the data we can read is:  
    ```
    sineforce: current sine force
    feedback: robot move according to the sine force and make another force
    force: TCP current force
    ```
    5. ```rosrun impedance_control_test impedance_control_node.py``` This will start to apply the impedance control according to the sineforce (0~20N) and keep force at TCP as 10N.
  - In my test result (by tuning the parameter), it can control between 9.91 N ~ 10.089 N  
- **Part 3 UR10 moveit test**  
  - In this part, I attached Kinect_V2 to the UR10 at TCP in Gazebo and collect data to make octomap IN RVIZ. Then, use the UR10 to do collision avoidance by Moveit in the world which I design and to achieve our desired position.
    1. ```roslaunch ur10_moveit_config ur10_octomap_demo.launch```
      - if you didn't see octomap please press add in RVIZ and find the pointcloud2 and check it subscribe to the right topic then restart
    2. ```rosrun ur10_moveit_config run_to_goal.py```
      - since it is run to designated position, if you want to go to another position please check if it is feasible or not.
    
