import logging
from enum import Enum

import pyvisa


class ControlMode(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class Axis(Enum):
    X = "1"
    Y = "2"
    Z = "3"


class NewportESA:
    """

    """
    def __init__(self) -> None:
        """

        """
        self.dev = None

    def connect(self, gpib_address: str, timeout: int = 3000) -> None:
        """

        :param gpib_address:
        :type gpib_address: str
        :param timeout: timeout period in units of milliseconds (ms)
        :type timeout: int
        """
        rm = pyvisa.ResourceManager()
        self.dev = rm.open_resource(resource_name=gpib_address)
        self.dev.read_termination = "\n"
        self.dev.write_termination = "\r\n"
        self.dev.timeout = timeout

        self.set_control_mode(mode=ControlMode.REMOTE)  # enforce REMOTE mode when connected

    def tear(self) -> None:
        """

        """
        self.set_control_mode(mode=ControlMode.LOCAL)  # enforce LOCAL mode before closing connection
        logging.info(self.get_control_mode())
        self.dev.close()

    def identify(self) -> str:
        """

        :return:
        :rtype: str
        """
        esa_id: str = self.dev.query("*IDN?")
        return esa_id

    def clear_status(self) -> None:
        """
        This command clears the Status Byte Register and Standard
        Event Status Register. The *CLS command also removes the
        error from the error buffer. The *CLS command is mainly used to
        clear the bit(s) that generated a request for serial or parallel poll.
        The Message Available (bit 4) of the status byte is not affected.

        The *CLS command will clear the error buffer.

        :return: None
        """
        self.dev.write("*CLS")

    def get_error_buffer(self) -> str:
        """
        This command returns the error message in the error buffer for
        the most current command. The ESA-C checks the syntax and
        data range for each command entered and updates the error
        message in the error buffer. When an error occurs, bit 4 or bit 5
        of the Standard Event Status Register will be set. The Status Byte
        Register will be updated, and <SRQ> will be issued if the corresponding
        enable bits are set. The *CLS command will clear the
        error buffer.

        :return:
        """
        buffer: str = self.dev.query("*ERR?")
        return buffer

    def is_operation_complete(self) -> str:
        """
        '*OPC?' : is the operation complete query command

        This query generates a response when all pending operations
        have been completed. The Message Available bit (bit 4) of the
        Status Byte Register will also be set because a response is
        generated. A pending operation is any command (such as V, DV,
        etc) which causes the actuators to move. The STOP command
        will terminate all pending operations. By enabling bit 4 of the
        Service Request Enable Register, the *OPC? command can cause
        the generation of a GPIB <SRQ>. The *OPC command and *OPC?
        query operate differently in how they signal an operation
        complete to the remote host. The *OPC? generates a message
        (1<NL>) when all operations are complete, which also sets the
        MAV bit (BIT 4) in the Status Byte Register. The *OPC command
        sets the OPC bit (bit 0) of the Standard Event Status Register
        when all pending operations are completed.

        The device will only respond once all pending operations are
        complete; therefore, a try except clause is used to handle
        exceptions (ex. a timeout exception).

        :return: An unsigned integer with the value '1'. The response
            is only generated when all pending operations are complete.
        :rtype: str
        """
        try:
            rsp: str = self.dev.query("*OPC?")
            return rsp
        except Exception as e:
            logging.exception(e)

    def set_control_mode(self, mode: ControlMode) -> None:
        """

        :param mode:
        :type mode: ControlMode
        :return: None
        """
        self.dev.write(f"{mode.value}")

    def get_control_mode(self) -> ControlMode:
        """

        :return:
        :rtype: ControlMode
        """
        return ControlMode(self.dev.query("MODE?"))

    def move_relative(self, axis: Axis, voltage: float) -> None:
        """

        :param axis:
        :type axis: Axis
        :param voltage: signed voltage relative move value
        :type voltage: float
        :return: None
        """
        self.dev.write(f"DV{axis.value} {voltage}")  # relative move

    def move_absolute(self, axis: Axis, voltage: float) -> None:
        """
        To set the voltages of all three axes to a specified value <number>.
        If the <number> is out of the voltage range, the command
        will not be executed. When this command is executed, the ESA-C
        will be in the REMOTE mode regardless of the current mode.
        This command can be executed under immediate motion or
        velocity control conditions. For velocity control motion (VEL),
        all three axes have to have the same voltage change rate.

        :param axis:
        :type axis: Axis
        :param voltage: unsigned voltage absolute move value with range from
            10.00 to 160.00 volts
        :type voltage: float
        :return: None
        """
        self.dev.write(f"V{axis.value} {voltage}")  # absolute move

    def get_axis_voltage(self, axis: Axis) -> str:
        """
        Get the present voltage for the requested axis. The ESA-C must be in
        ControlMode.REMOTE to return the value set via GPIB. When in ControlMode.LOCAL,
        the voltage reading is determined by the knob on the front panel of the
        instrument.

        Note: when a voltage change command (V or DV) is issued in IMMEDIATE mode
        just before an R1? command, the value received may not represent a stable
        value. Sending several consecutive R1? commands will ensure that the correct
        value is read.

        :param axis:
        :type axis: Axis
        :return:
        :rtype: str
        """
        return self.dev.query(f"R{axis.value}?")  # leading space character in ESA-C response for unknown reason

    def stop_motion(self, axis: Axis) -> None:
        """
        This command stops the motion of the axis initiated by any
        command via the GPIB port. It holds the position where the
        STOP1 command takes effect.

        :param axis:
        :type axis: Axis
        :return: None
        """
        self.dev.write(f"STOP{axis.value}")

    def set_velocity(self, axis: Axis, velocity: float) -> None:
        """
        This command sets the approximate rate of change in voltage
        (volts per second) of the axis if <number> is within the
        range from 0.05 to 10.0. After this command is executed, the
        motion of the axis will be under velocity control. If the
        <number> is greater than 10.0 or a non-numeric character is
        entered, then the <number> is not valid and the motion reverts
        to Immediate.

        :param axis:
        :type axis: Axis
        :param velocity: only values ranging from 0.05 to 10.0 are valid
        :type velocity: ControlMode
        :return: None
        """
        self.dev.write(f"VEL{axis.value} {velocity}")

    def get_velocity(self, axis: Axis) -> str:
        """
        This command requests the current rate of change value in
        volts per second of the axis as previously set via the GPIB
        port.

        :return:
        :rtype: str
        """
        return self.dev.query(f"VEL{axis.value}?")
