#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
from actionlib_msgs.msg import GoalID
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Header, String
from geometry_msgs.msg import Point, Quaternion
from location.srv import *


class Navigation:
    pub = None  # type: rospy.Publisher

    def start(self):

        def navigation_callback(message):
            # type: (String) -> None
            print(message.data)
            rospy.wait_for_service("location/request")
            request = rospy.ServiceProxy('location/request', Request_Location)
            response = request(message.data)
            print(response)
            client = actionlib.SimpleActionClient("/move_base", MoveBaseAction)
            client.wait_for_server()
            goal = MoveBaseGoal()
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.pose = response.location.pose
            client.send_goal(goal)
            client.wait_for_result()
            if client.get_state() == GoalStatus.SUCCEEDED:
                print("SUCCEEDED")
            if client.get_state() == GoalStatus.ABORTED:
                print("ABORTED")

        rospy.init_node('navigation', anonymous=False)
        rospy.Subscriber("/navigation/start", String, navigation_callback)
        rospy.spin()


if __name__ == "__main__":
    Navigation().start()
