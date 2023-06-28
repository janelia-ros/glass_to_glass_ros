import rclpy
from rclpy.node import Node

from weigher_interfaces.msg import Weight, WeightArray
from weigher_interfaces.srv import Tare

from loadstar_sensors_interface import LoadstarSensorsInterface
import asyncio



class Weigher(Node):

    def __init__(self):
        node_name = 'weigher'
        super().__init__(node_name)

        self.get_logger().info('Initializing Weigher Node')

        # parameters
        self.declare_parameter('debug', False)
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('threshold', 100)
        self.declare_parameter('weight_array_length_max', 2000)

        # publishers
        self._pub_weight = self.create_publisher(Weight, f'/{node_name}/weight', 10)
        self._pub_weight_thresholded = self.create_publisher(Weight, f'/{node_name}/weight_thresholded', 10)
        self._pub_weight_array = self.create_publisher(WeightArray, f'/{node_name}/weight_array', 10)
        self._pub_weight_array_thresholded = self.create_publisher(WeightArray, f'/{node_name}/weight_array_thresholded', 10)

        # services
        self._srv_tare = self.create_service(Tare, f'/{node_name}/tare', self._tare_callback)
        self._taring = False

        # scale device
        debug = self.get_parameter('debug').get_parameter_value().bool_value
        self._dev = LoadstarSensorsInterface(debug=debug)

    async def start_getting_sensor_values(self):
        # parameters
        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        self._threshold = self.get_parameter('threshold').get_parameter_value().integer_value
        self._weight_array_length_max = self.get_parameter('weight_array_length_max').get_parameter_value().integer_value
        self._weight_array_length = 0
        self._weight_array = []
        self._weight_array_thresholded = []

        self.get_logger().info(f'start_getting_sensor_values on serial port: {serial_port}')

        await self._dev.open_high_speed_serial_connection(port=serial_port)
        self._dev.set_sensor_value_units('gram')
        self._dev.set_units_format('.1f')
        await self._dev.tare()
        self._dev.start_getting_sensor_values(self._sensor_value_callback)

    async def stop_getting_sensor_values(self):
        self.get_logger().info('stop_getting_sensor_values')

        await self._dev.stop_getting_sensor_values()

    async def _sensor_value_callback(self, sensor_value):
        if self._weight_array_length == self._weight_array_length_max:
            self._weight_array_length = 0

            weight_array_msg = WeightArray()
            weight_array_msg.array = self._weight_array
            self._pub_weight_array.publish(weight_array_msg)
            self._weight_array = []

            if len(self._weight_array_thresholded) > 0:
                weight_array_thresholded_msg = WeightArray()
                weight_array_thresholded_msg.array = self._weight_array_thresholded
                self._pub_weight_array_thresholded.publish(weight_array_thresholded_msg)
                self._weight_array_thresholded = []

        weight_msg = Weight()
        weight_msg.stamp = self.get_clock().now().to_msg()
        weight_msg.weight = sensor_value.magnitude
        self._pub_weight.publish(weight_msg)

        self._weight_array.append(weight_msg)
        self._weight_array_length += 1

        if sensor_value.magnitude >= self._threshold:
            self._pub_weight_thresholded.publish(weight_msg)
            self._weight_array_thresholded.append(weight_msg)

        await asyncio.sleep(0)

    async def _async_tare_callback(self):
        await self.stop_getting_sensor_values()
        await self._dev.tare()
        await self.start_getting_sensor_values()
        self._taring = False

    def _tare_callback(self, request, response):
        self.get_logger().info('tare_callback')
        response.stamp = self.get_clock().now().to_msg()
        response.success = False
        if not self._taring:
            self._taring = True
            self._tare_callback_task = asyncio.create_task(self._async_tare_callback())
            response.success = True
        return response

async def async_main():
    weigher = Weigher()

    await weigher.start_getting_sensor_values()

    while rclpy.ok():
        rclpy.spin_once(weigher, timeout_sec=0)
        await asyncio.sleep(1e-4)

    await weigher.stop_getting_sensor_values()

    weigher.destroy_node()

def main(args=None):
    rclpy.init(args=args)

    asyncio.run(async_main())

    rclpy.shutdown()


if __name__ == '__main__':
    main()
