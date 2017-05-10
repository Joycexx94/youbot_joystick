#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def publisher():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('cmd_vel_publisher')
    rate = rospy.Rate(10) 
    twist = Twist()
    n = 0
    while not rospy.is_shutdown():
        if n = 0:
            twist.linear.y = 1
            n = 1
        else:
            twist.linear.y = -1
            n = 0
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
