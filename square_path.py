#!/usr/bin/env python
# ROS python API

'''
Goal : To make drone follow a square path

Step:

1) arm
2) set mode : px4-offboard, ardupilot-guided
3) take off from origin and reach desire altitude
4) Go to (10,10), as a starting point for square path

   go_to_launch()

5) Then starting followinng square path in order (10,10) -> (10,-10) ->(-10,-10) -> (-10,10) -> (10,10) and so on

    square_path_loop()

6) keep on follow square path until user terminate 

'''
import rospy

# 3D point & Stamped Pose msgs
from geometry_msgs.msg import *
# import all mavros messages and services
from mavros_msgs.msg import *
from mavros_msgs.srv import *
import math
from tf import transformations
import numpy
global state_of_drone
state_of_drone = 0


# Flight modes class
# Flight modes are activated using ROS services
class fcuModes:
    def __init__(self):
        pass

    def setTakeoff(self):
            rospy.wait_for_service('/mavros/cmd/takeoff')
            try:
                takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
                takeoffService(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
            except rospy.ServiceException, e:
                print "Service takeoff call failed: %s"%e

    def setArm(self):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(True)
        except rospy.ServiceException, e:
            print "Service arming call failed: %s"%e

    def setDisarm(self):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(False)
        except rospy.ServiceException, e:
            print "Service disarming call failed: %s"%e

    def setGUIDEDMode(self):
            rospy.wait_for_service('mavros/set_mode')
            try:
                flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
                flightModeService(custom_mode='GUIDED')
            except rospy.ServiceException, e:
                print "service set_mode call failed: %s. Offboard Mode could not be set."%e

    def setAutoLandMode(self):
            rospy.wait_for_service('/mavros/cmd/land')
            try:
                flightModeService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
                flightModeService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
            except rospy.ServiceException, e:
                print "service set_mode call failed: %s.  The vehicle cannot land"%e

# Controller class is for all callback function to store ros topic messages
class Controller:
    # initialization method
    def __init__(self):
        # Drone state
        self.state = State()
        # Instantiate a setpoints message
        self.sp = PositionTarget()
        # set the flag to use position setpoints and yaw angle
        self.sp.type_mask = int('010111111000', 2)
        # LOCAL_NED
        self.sp.coordinate_frame = 1



    def posCb(self,msg):

        global yaw, dist , local_pos 

        local_pos = Point()


        local_pos.x = msg.pose.position.x
        local_pos.y = msg.pose.position.y
        local_pos.z = msg.pose.position.z

        quaternion = [ msg.pose.orientation.x, msg.pose.orientation.y,
         msg.pose.orientation.z, msg.pose.orientation.w ]



        # transforming orientation from quaternion to euler
        euler = transformations.euler_from_quaternion(quaternion)
        #print(euler,"euler")

        # getting third element from 1D euler matrix
        yaw = euler[2] 
        print(yaw,"yaw")

        

    ## Drone State callback
    def stateCb(self, msg):
        self.state = msg

    


# Main function
def main():

    # initiate node
    rospy.init_node('setpoint_node', anonymous=True)

    # flight mode object
    modes = fcuModes()

    # controller object
    cnt = Controller()

    # ROS loop rate
    rate = rospy.Rate(20.0)

    # Subscribe to drone state
    rospy.Subscriber('mavros/state', State, cnt.stateCb)

    # Subscribe to drone's local position
    rospy.Subscriber('mavros/local_position/pose', PoseStamped, cnt.posCb)

    # Velocity publisher
    vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10)

    flag = 0
    global local_pos
    ALT_SP = 2

    global state_of_drone
    

    def adjust_yaw(x1 , y1):

        cnt = Controller()
        global yaw,dist,local_pos , yaw_error, state_of_drone

        desired_position = Point()
        desired_position.x = x1
        desired_position.y = y1


        print(yaw,"yaw_found")
        print("Hello")
        print(local_pos.x,"local_pos.x")
        print(local_pos.y,"local_pos.y")


        
        # angle of target
        steering_angle = math.atan2(desired_position.y-local_pos.y, desired_position.x-local_pos.x)
        print(steering_angle,"steering_angle")
        
        # angle to cover
        angle = steering_angle - yaw
        print(angle,"angle")
        
        yaw_precision = (math.pi / 180) *10  #+- 10 degree allowed
        print(yaw_precision ,"yaw_precision")

        

        
        yaw_error = math.fabs(angle) - yaw_precision
        

        print(yaw_error,"error")

        angular_vel = 0.2 * math.fabs(angle)/angle
        print(angular_vel,"angular_vel")

        dist = math.sqrt(math.pow(desired_position.y-local_pos.y,2)+
            (math.pow(desired_position.x-local_pos.x,2)))

        dist_precision = 0.3
        dist_error = dist-dist_precision
        print(dist_error , "dist_error")


        vel_msg = Twist()

        if yaw_error > 0:

            # angle adjustment using yaw
            vel_msg.angular.x=0
            vel_msg.angular.y=0
            vel_msg.angular.z = angular_vel

            vel_pub.publish(vel_msg)
            print("adjusting yaw")
            #print(error,"error_new")
            #print(yaw,"curr_yaw") 

        elif yaw_error <= 0:

            vel_msg.angular.x=0
            vel_msg.angular.y=0
            vel_msg.angular.z= 0

            vel_pub.publish(vel_msg)
            print("angle_reached")

            if dist_error > 0 :

                # calculate velocity as vector to move drone in its forward facing
                vel_msg.linear.x = 0.8*math.cos(yaw)
                vel_msg.linear.y = 0.8*math.sin(yaw)
                vel_msg.linear.z = 0

                vel_pub.publish(vel_msg)
                print("adjusting distance")

            elif dist_error <= 0:

                vel_msg.linear.x = 0
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                vel_pub.publish(vel_msg)

                print("distance reached")
                
                # go in square loop
                if state_of_drone == 4:
                    state_of_drone = 1
                else :
                    state_of_drone = state_of_drone +1
                main()
        


    

        

    # Make sure the drone is armed
    while not cnt.state.armed:
        modes.setArm()
        rate.sleep()

    print(cnt.state.mode)

    while cnt.state.mode != "GUIDED":
        modes.setGUIDEDMode()
        print(" guided mode set")


    # ROS main loop
    while not rospy.is_shutdown():

        print(" Ready for mission...")

        while(((math.floor(local_pos.z))<  ALT_SP) and flag == 0):
            modes.setTakeoff()
            print("taking off...")

            if (math.floor(local_pos.z)) == ALT_SP:
                flag=1
                print("Altitude reached")

        

        
        if state_of_drone ==0:
            print(state_of_drone,"state_of_drone")
            adjust_yaw(10,10)
        elif state_of_drone ==1:
            print(state_of_drone,"state_of_drone")
            adjust_yaw(-10,10)
        elif state_of_drone ==2:
            print(state_of_drone,"state_of_drone")
            adjust_yaw(-10,-10)
        elif state_of_drone ==3:
            print(state_of_drone,"state_of_drone")
            adjust_yaw(10,-10)
        elif state_of_drone ==4:
            print(state_of_drone,"state_of_drone")
            adjust_yaw(10,10)

        
    	rate.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass