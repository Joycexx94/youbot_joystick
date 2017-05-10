#!/usr/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import std_srvs.srv

class TeleopTurtle:
		def __init__(self):
				rospy.init_node('turtle_teleop_joy')
				self.linear_axis_x = rospy.get_param("axis_linear_x")
				self.linear_axis_y = rospy.get_param("axis_linear_y")
				self.angular_axis = rospy.get_param("axis_angular")
				self.linear_scale = rospy.get_param("scale_linear")
				self.angular_scale = rospy.get_param("scale_angular")
				self.robot_topic_name = rospy.get_param("robot_topic_name") 
				rospy.loginfo("Waiting")


				#rospy.wait_for_service('base/switchOffMotors')

				self.twist = None
				self.twist_pub = rospy.Publisher(self.robot_topic_name, Twist,queue_size=1)
				rospy.Subscriber("joy", Joy, self.callback)
				rate = rospy.Rate(rospy.get_param('~hz', 20))

				while not rospy.is_shutdown():
						rate.sleep()
						if self.twist:
								self.twist_pub.publish(self.twist)

		def switch_off_motors(self):
				 rospy.wait_for_service('/base/switchOffMotors')
				 switch_off = rospy.ServiceProxy('/base/switchOffMotors', std_srvs.srv.Empty)
				 switch_off()

		def switch_on_motors(self):
				 rospy.wait_for_service('/base/switchOnMotors')
				 switch_on = rospy.ServiceProxy('/base/switchOnMotors', std_srvs.srv.Empty)
				 switch_on()

		def callback(self,msg):
				twist = Twist()
				twist.linear.x = (self.linear_scale + 1.9*msg.axes[3]) * msg.axes[self.linear_axis_x]
				twist.linear.y = (self.linear_scale + 1.9*msg.axes[3]) * msg.axes[self.linear_axis_y]
				twist.angular.z = self.angular_scale * msg.axes[self.angular_axis]
				self.twist=twist
				if (msg.buttons[3]==1 and msg.buttons[2]==1):
					twist.linear.x = 0
					twist.linear.y = 0
					twist.angular.z = 0
					#kill_base = rospy.ServiceProxy('base/switchOffMotors', std_srvs.srv.Empty)
					#kill_base()
					#self.switch_off_motors()
				if (msg.buttons[0]==1 and msg.buttons[1]==1):
					#turn_on_base = rospy.ServiceProxy('base/switchOnMotors', std_srvs.srv.Empty)
					#turn_on_base()
					#self.switch_on_motors()

if __name__ == "__main__": 
		TeleopTurtle()

