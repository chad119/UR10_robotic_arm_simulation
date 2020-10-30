#!/usr/bin/env python
'''
This program is for linear moving back and forth on xy-plane
'''

import rospy
import math
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage

#Threshold
t = 1e-5

#global var from Sub
x=0
y=0
z=0
tf_list = []

#Sub function
def jointstate(data):
    '''
    topic: /tf
    message type: TFMessage
    '''
    global x,y,z,tf_list
    tf_list = data.transforms
    x = tf_list[0].transform.translation.x
    y = tf_list[0].transform.translation.y
    z = tf_list[0].transform.translation.z
    x = round(x, 5)
    y = round(y, 5)
    z = round(z, 5)

#Pub function
def move_node():
    rospy.init_node('move_node', anonymous = True)
    sub = rospy.Subscriber('/tf', TFMessage, jointstate)
    pub = rospy.Publisher('ur_hardware_interface/script_command', String, queue_size=20)

    rate = rospy.Rate(10)
    print "start!!!"
    moving_signal = 0
    while not rospy.is_shutdown():
        if moving_signal==0:
            print "initial"
            while (x-1.0)**2!=0 and (y-0.5)**2!=0 and (z-0.35)**2!=0:
                urscript = "movel(p[1.0,0.5,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)"
                pub.publish(urscript)
                rate.sleep()
            moving_signal=1
        else:
            print "backward!"
            posx_end = 1.0
            posy_end = 0.5
            while True:
                posx_end = posx_end-0.005
                posy_end = posy_end-0.0025
                urscript = "movel(p[%f,%f,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)" %(posx_end,posy_end)
                pub.publish(urscript)
                rate.sleep()
                if round(posx_end,1)==0.5 and round(posy_end,2)==0.25:
                    print "ok_forward"
                    break

            posx_ini = 0.5
            posy_ini = 0.25
            print "forward!"
            while True:
                posx_ini = posx_ini+0.005
                posy_ini = posy_ini+0.0025
                urscript = "movel(p[%f,%f,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)" %(posx_ini,posy_ini)
                pub.publish(urscript)
                rate.sleep()
                if round(posx_ini,1)==1.0 and round(posy_ini,1)==0.5:
                    print "OK_BACKWARD"
                    break
	    
if __name__ =='__main__':
    try:
        move_node()
    except rospy.ROSInterruptException:
        pass
