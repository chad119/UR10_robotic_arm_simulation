
#!/usr/bin/env python
'''
This program is for linear moving back and forth on xy-plane
'''

import rospy
import math
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage

#Threshold
t = 1e-9

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
            while (x-0.5)**2>=t and (y-0.25)**2>=t and (z-0.35)**2>=t:
                print "initial"
                
                urscript = "movel(p[0.5,0.25,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)"
                pub.publish(urscript)
                rate.sleep()
            moving_signal=1
        else:
            if (x-1.0)**2<=t and (y-0.5)**2<=t and (z-0.35)**2<=t:
                print "move backward!"
                #change
                #urscript = "speedl([-0.5,-0.25,0,0,0,0],0.5,0.5)"
                
                
                urscript = "movel(p[0.5,0.25,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)"
                pub.publish(urscript)
                rate.sleep()
                
       
            elif (x-0.5)**2<=t and (y-0.25)**2<=t and (z-0.35)**2<=t:
                print "move forward!"
                #change
                #urscript = "speedl([0.5,0.25,0,0,0,0],0.5,0.5)"
                urscript = "movel(p[1.0,0.5,0.35,2.220,-2.223,-0.002],a=1.2,v=0.25,t=0,r=0)"
                pub.publish(urscript)
                rate.sleep()
			
if __name__ =='__main__':
    try:
        move_node()
    except rospy.ROSInterruptException:
        pass
