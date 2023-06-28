from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution


def generate_launch_description():
    serial_port_arg = DeclareLaunchArgument(
      'serial_port', default_value=TextSubstitution(text='/dev/ttyUSB0')
    )
    threshold_arg = DeclareLaunchArgument(
      'threshold', default_value=TextSubstitution(text='100')
    )
    weight_array_length_max_arg = DeclareLaunchArgument(
      'weight_array_length_max', default_value=TextSubstitution(text='2000')
    )

    return LaunchDescription([
        serial_port_arg,
        threshold_arg,
        weight_array_length_max_arg,
        Node(
            package='weigher',
            executable='weigher',
            name='weigher',
            parameters=[{
            'serial_port': LaunchConfiguration('serial_port'),
            'threshold': LaunchConfiguration('threshold'),
            'weight_array_length_max': LaunchConfiguration('weight_array_length_max'),
         }]
        )
    ])
