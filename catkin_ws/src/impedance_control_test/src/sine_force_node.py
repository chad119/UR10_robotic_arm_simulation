#!/usr/bin/env python
'''
This program publish force = sine force, print the total_force = sine force+feedback_force and subscribe feedback force.
'''

import rospy
import math
from std_msgs.msg import Float64

#global variable
F_feedback = 0

#sub function
def feedback_force(data):
    global F_feedback
    F_feedback = data.data

#pub function
def sine_force_node():
    rospy.init_node('sine_force_node', anonymous = True)
    sub = rospy.Subscriber('/Feedback_Force', Float64, feedback_force)
    pub = rospy.Publisher('/TCP_Force', Float64, queue_size=10)
    rate = rospy.Rate(10)
    print "start!!!"
    t = 0
    while not rospy.is_shutdown():
        #sine-like force from 0~20N
        sine_force = 10+10*math.sin(t)
        force = sine_force+F_feedback
        print "**************************************"
        print "sineforce:",sine_force
        print "feedback :",F_feedback
        print "force    :",force
        pub.publish(sine_force)
        t = t + math.radians(1)
        rate.sleep()

if __name__ =='__main__':
    try:
        sine_force_node()
    except rospy.ROSInterruptException:
        pass


