#!/usr/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class TeleopTest:
    def __init__(self):
        rospy.init_node('estop_test')
        self.linear_axis_x = rospy.get_param("axis_linear_x")
        self.linear_axis_y = rospy.get_param("axis_linear_y")
        self.angular_axis = rospy.get_param("axis_angular")
        self.linear_scale = rospy.get_param("scale_linear")
        self.robot_topic_name = 'cmd_vel' 
     
        self.twist = None
        self.twist_pub = rospy.Publisher(self.robot_topic_name, Twist,queue_size=1)
        rospy.Subscriber("joy", Joy, self.callback)
        rate = rospy.Rate(rospy.get_param('~hz', 10))

        while not rospy.is_shutdown():
            rate.sleep()
            if self.twist:
                self.twist_pub.publish(self.twist)

    def callback(self, msg):
        twist = Twist()
        if (msg.buttons[3]==1 and msg.buttons[2]==1):
            twist.linear.x = 0
            twist.linear.y = 0
            twist.angular.z = 0
        else:
            twist.angular.z = 3
        self.twist=twist
          
if __name__ == "__main__": 
    TeleopTest()
