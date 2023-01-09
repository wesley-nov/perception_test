#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 
import cv2

bridge = CvBridge()
pub = rospy.Publisher('/bullseye_image', Image, queue_size=5)

# coordinates are a global variable in order to modularize the callback function
bullseye_location = rospy.get_param('bullseye/bullseye_location') 
coordinates = rospy.get_param('/' + bullseye_location)

def bullseyeCallback(image):

    cv_image = bridge.imgmsg_to_cv2(image, desired_encoding='passthrough')
    cv_image = cv2.circle(cv_image, (coordinates['x'], coordinates['y']), radius = 5, color=(255,0,0), thickness=6)
    # cv2.imwrite("/home/roboeyes/catkin_ws/test.jpg", cv_image)
    image = bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
    pub.publish(image)

def listener():

    rospy.init_node('bullseye', anonymous=True)

    rospy.Subscriber("/zed2/zed_node/rgb/image_rect_color", Image, bullseyeCallback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut down")

if __name__ == '__main__':
    print("Starting the node")
    listener()
