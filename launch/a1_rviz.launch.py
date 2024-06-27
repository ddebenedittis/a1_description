import os

from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    
    package_share_path = FindPackageShare('a1_description')

    xacro_file_path = PathJoinSubstitution([
        package_share_path,
        LaunchConfiguration('xacro_file_path', default=os.path.join('xacro', 'robot.xacro'))
    ])
    
    config_file_path = PathJoinSubstitution([
        package_share_path,
        LaunchConfiguration('config_file_path', default=os.path.join('launch', 'check_joint.rviz'))
    ])

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # ======================================================================== #

    return LaunchDescription([
        # A GUI to manipulate the joint state values
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        
        # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'robot_description': ParameterValue(Command(['xacro', ' ' ,xacro_file_path]), value_type=str)}
            ],
        ),
        
        # Launch RViz
        Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', config_file_path],
        )
    ])


# <launch>

#     <arg name="user_debug" default="false"/>
    
#     <param name="robot_description" command="$(find xacro)/xacro --inorder '$(find a1_description)/xacro/robot.xacro'
#             DEBUG:=$(arg user_debug)"/>

#     <!-- for higher robot_state_publisher average rate-->
#     <!-- <param name="rate" value="1000"/> -->

#     <!-- send fake joint values -->
#     <node pkg="joint_state_publisher" type="joint_state_publisher" name="joint_state_publisher">
#         <param name="use_gui" value="TRUE"/>
#     </node>

#     <node pkg="robot_state_publisher" type="robot_state_publisher" name="robot_state_publisher">
#         <param name="publish_frequency" type="double" value="1000.0"/>
#     </node>

#     <node pkg="rviz" type="rviz" name="rviz" respawn="false" output="screen"
#         args="-d $(find a1_description)/launch/check_joint.rviz"/>

# </launch>
