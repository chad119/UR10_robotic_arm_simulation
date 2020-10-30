#!/usr/bin/env python
'''
This program is for impedance control
'''

import rospy
import math
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from std_msgs.msg import Float64

#Target force
Fd = 10

#time
t = 0.1

#coefficient (M is acceleration coefficient, B is velocity coefficient, K is displacement coefficient)
M = 0.95 
D = 0.0000001
K = 100

#global subs vars
x=0
y=0
z=0
tflist = []
force_in = 0

#sub function
#sub TCP position
def position(data):
    global x,y,z,tf_list
    tf_list = data.transforms
    x = tf_list[0].transform.translation.x
    y = tf_list[0].transform.translation.y
    z = tf_list[0].transform.translation.z
    x = round(x, 5)
    y = round(y, 5)
    z = round(z, 5)


#sub incoming force
def force(data):
    global force_in
    force_in = data.data

#pub function
def impedance_control_node():
    rospy.init_node('impedance_control_node', anonymous = True)
    
    sub_tf = rospy.Subscriber('/tf', TFMessage, position)
    sub_force = rospy.Subscriber('/TCP_Force', Float64, force)
    pub_script = rospy.Publisher('/ur_hardware_interface/script_command', String, queue_size=20)
    pub_fb = rospy.Publisher('/Feedback_Force', Float64, queue_size=10)
    
    rate = rospy.Rate(10)
    moving_signal = 0
    pre_dis = 0.35
    vel = 0
    acc = 0
    while not rospy.is_shutdown():
        if moving_signal==0:
            #initial position:[1.0,0.5,0.35]
            print "initial"
            while (x-1.0)**2!=0 and (y-0.5)**2!=0 and (z-0.35)**2!=0:              
                urscript = "movel(p[1.0,0.5,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)"
                pub_script.publish(urscript)
                rate.sleep()
            moving_signal=1
        else:
            print "backward!"
            posx_end = 1.0
            posy_end = 0.5
            while True:
                #move to position:[0.5,0.25,0.35]
                dis = (Fd - force_in - M*acc - D*vel)/float(K)
                z_pos = 0.35-dis
                #print "dis:",dis
                posx_end = posx_end-0.005
                posy_end = posy_end-0.0025
                urscript = "movel(p[%f,%f,%f,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)" %(posx_end,posy_end,z_pos)
                vel = dis/t
                acc = vel/t
                feedback_force = (M*acc + D*vel + K*dis)
                pub_fb.publish(feedback_force)
                pub_script.publish(urscript)
                rate.sleep()
                if round(posx_end,1)==0.5 and round(posy_end,2)==0.25:
                    print "ok_forward"
                    break
            posx_ini = 0.5
            posy_ini = 0.25
            while True:
                #move to position:[1.0,0.5,0.35]
                dis = (Fd - force_in - M*acc - D*vel)/float(K)
                z_pos = 0.35-dis
                #print "dis:",dis
                posx_ini = posx_ini+0.005
                posy_ini = posy_ini+0.0025
                urscript = "movel(p[%f,%f,%f,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)" %(posx_ini,posy_ini,z_pos)
                vel = dis/t
                acc = vel/t
                pub_script.publish(urscript)
                feedback_force = (M*acc + D*vel + K*dis)
                pub_fb.publish(feedback_force)
                rate.sleep()
                if round(posx_ini,1)==1.0 and round(posy_ini,1)==0.5:
                    print "OK_BACKWARD"
                    break
            

#end
if __name__ =='__main__':
    try:
        impedance_control_node()
    except rospy.ROSInterruptException:
        pass

