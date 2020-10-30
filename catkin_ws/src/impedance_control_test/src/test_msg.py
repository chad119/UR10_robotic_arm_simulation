#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import String
import tf2_ros
#from geometry_msgs import Vector3 
from tf2_msgs.msg import TFMessage


x=0
y=0
z=0
yo = []
#Sub function
def jointstate(data):
    '''
    global elbow, shoulder_lift, shoulder_pan, wrist1, wrist2, wrist3
    elbow = data.position[0]
    shoulder_lift = data.position[1]
    shoulder_pan = data.position[2]
    wrist1 = data.position[3]
    wrist2 = data.position[4]
    wrist3 = data.position[5]
    elbow = round(elbow, 5)
    shoulder_lift = round(shoulder_lift, 5)
    shoulder_pan = round(shoulder_pan, 5)
    wrist1 = round(wrist1, 5)
    wrist2 = round(wrist2, 5)
    wrist3 = round(wrist3, 5)
    '''
    global x,y,z,yo
    '''
    x = data.transforms.transform.translation.x
    y = data.transforms.transform.translation.y
    z = data.transforms.transform.translation.z
    x = round(x, 5)
    y = round(y, 5)
    z = round(z, 5)
    '''
    yo = data.transforms
    x = yo[0].transform.translation.x


def test():
    rospy.init_node('test', anonymous = True)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    sub = rospy.Subscriber('/tf', TFMessage, jointstate)
    rate = rospy.Rate(10)
    print "start!!!"
    
    while not rospy.is_shutdown():
        '''
        print "x:",x
        print "y:",y
        print "z:",z
        '''
        

        #print yo
        print "x:",x


if __name__ =='__main__':
    try:
        test()
    except rospy.ROSInterruptException:
        pass



    
