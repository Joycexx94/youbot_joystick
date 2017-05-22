#!/usr/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import std_srvs.srv

class TeleopTurtle:
    def __init__(self):
        # initialize note
        rospy.init_node('turtle_teleop_joy')
        # get parameters from youbot_joystick.launch
        self.linear_axis_x = rospy.get_param("axis_linear_x")
        self.linear_axis_y = rospy.get_param("axis_linear_y")
        self.angular_axis = rospy.get_param("axis_angular")
        self.linear_scale = rospy.get_param("scale_linear")
        self.angular_scale = rospy.get_param("scale_angular")
        self.robot_topic_name = rospy.get_param("robot_topic_name") 
        rospy.loginfo("Waiting")



        self.twist = None
        # initialize publisher
        self.twist_pub = rospy.Publisher(self.robot_topic_name, Twist,queue_size=1)
        # initialize subscriber
        rospy.Subscriber("joy", Joy, self.callback)
        rate = rospy.Rate(rospy.get_param('~hz', 20))

        # spin and publish velocity commands
        while not rospy.is_shutdown():
            rate.sleep()
            if self.twist:
                self.twist_pub.publish(self.twist)

    def callback(self,msg):
        twist = Twist()
        # e-stop: if both button B and button Y are pressed, send 0 velocity to the robot
        if (msg.buttons[3]==1 and msg.buttons[2]==1):
            twist.linear.x = 0
            twist.linear.y = 0
            twist.angular.z = 0
        else:
            # linear velocity and angular velocity controls
            twist.linear.x = (self.linear_scale + 1.9*msg.axes[3]) * msg.axes[self.linear_axis_x]
            twist.linear.y = (self.linear_scale + 1.9*msg.axes[3]) * msg.axes[self.linear_axis_y]
            twist.angular.z = self.angular_scale * msg.axes[self.angular_axis]
        self.twist=twist
if __name__ == "__main__": 
    TeleopTurtle()

