from robomaster.action import Action
from time import sleep


class Arm:
    def __init__(self, RoboMaster) -> None:
        self.robomaster = RoboMaster
        self.robot = self.robomaster.robot
        try:
            self.gripper = RoboMaster.gripper
        except:
            self.gripper = RoboMaster.gripper = Gripper(RoboMaster)

    # Robotic Arm
    def move(self, x, z, blocking: bool = True) -> Action:
        # TODO: test that min and max values are correct
        """
        Moves the robotic arm to a set position.
        The Origin (starting point) is the current position of the arm.
        Minimum X is -100° and Maximum X is +100°.
        Minimum Z is -100° and Maximum Z is +100°.
        args:
        x (float): X position of the arm in degrees. Defaults to 0.0.
        z (float): Z position of the arm in degrees. Defaults to 0.0.
        blocking (bool): Block until action is complete. Defaults to False.
        """
        if not blocking:
            return self.robot.robotic_arm.move(x=x, y=z)
        else:
            return self.robot.robotic_arm.move(x=x, y=z).wait_for_completed()

    def moveTo(self, x, z, blocking: bool = True) -> Action:
        # TODO:test that min and max values are correct
        """
        Moves the robotic arm to a set position.
        The Origin (starting point) is the coordinate at initialisation (start up).
        Minimum X is -200° and Maximum X is +200°.
        Miinimum Z is -200° and Maximum Z is +200°.
        args:
        x (float): X position of the arm in degrees. Defaults to 0.0.
        z (float): Z position of the arm in degrees. Defaults to 0.0.
        blocking (bool): Block until action is complete. Defaults to False.
        """
        if not blocking:
            return self.robot.robotic_arm.moveto(x=x, y=z)
        else:
            return self.robot.robotic_arm.moveto(x=x, y=z).wait_for_completed()

    def recenter(self, blocking: bool = True) -> Action:
        """
        Recenters the robotic arm to its starting position.
        """
        if not blocking:
            return self.robot.robotic_arm.recenter()
        else:
            return self.robot.robotic_arm.recenter().wait_for_completed()

    def pickup(self) -> None:
        # TODO: Test this method
        """
        Pick up an object.
        """
        self.moveTo(x=0, z=50)
        self.gripper.open()
        sleep(1.5)
        self.move(x=175, z=-250)
        self.moveTo(x=175, z=-200)
        self.gripper.close()
        sleep(1.5)
        self.gripper.pause()
        sleep(0.1)
        self.moveTo(0,50)

    def drop(self) -> None:
        # TODO: Test this method
        """
        Drop / place an object.
        """
        self.move(x=175, z=-250)
        self.moveTo(x=175, z=-200)
        self.gripper.open()
        sleep(1.5)
        self.moveTo(x=0, z=50)


class Gripper:
    def __init__(self, RoboMaster) -> None:
        self.robomaster = RoboMaster
        self.robot = self.robomaster.robot

    def open(self, power: int = 50) -> bool:
        """
        Opens the gripper.
        Minimum power is 1 and maximum power is 100.
        args:
        power (int): Power of the gripper motor. Defaults to 50.
        """
        return self.robot.gripper.open(power=power)

    def close(self, power: int = 50) -> bool:
        """
        Closes the gripper.
        Minimum power is 1 and maximum power is 100.
        args:
        power (int): Power of the gripper motor. Defaults to 50.
        """
        return self.robot.gripper.close(power=power)

    def pause(self) -> bool:
        """
        Stops the gripper motor.
        """
        return self.robot.gripper.pause()

    def stop(self) -> bool:
        """
        Stops the gripper motor.
        """
        return self.pause()
