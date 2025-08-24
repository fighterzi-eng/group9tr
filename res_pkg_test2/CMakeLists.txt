cmake_minimum_required(VERSION 3.0.2)
project(res_pkg_test2)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

add_service_files(
  FILES
  order.srv
  start.srv
  # add more .srv files here if needed
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime rospy std_msgs
)
