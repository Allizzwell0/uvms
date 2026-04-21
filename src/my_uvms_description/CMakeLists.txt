cmake_minimum_required(VERSION 3.8)
project(my_uvms_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY description config launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
