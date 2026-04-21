from geometry_msgs.msg import Twist


class ROVReferenceInterface:
    """Publish Blue ROV body-velocity references to the existing ISMC input topic."""

    def __init__(self, node, topic: str = '/integral_sliding_mode_controller/reference', queue_size: int = 10):
        self._pub = node.create_publisher(Twist, topic, queue_size)
        self.topic = topic

    def command(self, surge=0.0, sway=0.0, heave=0.0, roll_rate=0.0, pitch_rate=0.0, yaw_rate=0.0):
        msg = Twist()
        msg.linear.x = float(surge)
        msg.linear.y = float(sway)
        msg.linear.z = float(heave)
        msg.angular.x = float(roll_rate)
        msg.angular.y = float(pitch_rate)
        msg.angular.z = float(yaw_rate)
        self._pub.publish(msg)

    def stop(self):
        self.command()
