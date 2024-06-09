"""Utils for Dialer Simulator app."""

import re

from mobly.controllers import android_device


DIALER_PACKAGE_NAME = 'com.google.android.dialer'


class Error(android_device.Error):
  """Error when an operation of this utilities fails."""


class DialerSimulator:
  """Class for Dialer Simulator app.

  The Dialer Simulator is used only on dogfood version.
  """

  def __init__(self, device: android_device.AndroidDevice) -> None:
    self._device = device
    self._verify_dialer_version()

  def _verify_dialer_version(self) -> None:
    """Verifies that dialer app whether is dogfood version.

    Raises:
      Error: Dialer is not installed or not dogfood version.
    """
    output = self._device.adb.shell(
        ['dumpsys', 'package', DIALER_PACKAGE_NAME, '|', 'grep', '-E',
         '"versionName=(.+)"', '||', 'echo  ']).decode('utf-8').strip()
    version = re.findall(r'versionName=(.+)', output)
    if not version:
      raise Error(self._device, 'Dialer app is not installed.')
    self._device.log.debug('Dialer Simulator Version: %s', version)
    if 'dogfood' not in version[0]:
      raise Error(
          self._device,
          f'Dialer app is not dogfood version: {version}')

  def execute_command(self, *cmd_args: str) -> None:
    """Executes a command.

    Args:
      *cmd_args: Arguments for the command.
    """
    command = ['am', 'broadcast', '-n',
               ('com.google.android.dialer/com.android.dialer.simulator.'
                'impl.SimulatorBroadcastReceiver_Receiver')] + list(cmd_args)
    self._device.adb.shell(command)

  def make_incoming_call(self) -> None:
    """Makes an incoming call."""
    self.stop_dialer()
    self.execute_command(
        '--es', 'command', 'IncomingCall', '--es', 'number', '1234567890',
        '--ei', 'presentation', '1', '--es', 'cnap', 'SomeCnap')

  def make_outgoing_call(self) -> None:
    """Makes an outgoing call."""
    self.stop_dialer()
    self.execute_command(
        '--es', 'command', 'OutgoingCall', '--es', 'number', '1234567890',
        '--ei', 'presentation', '1', '--es', 'cnap', 'SomeCnap')

  def stop_dialer(self) -> None:
    """Stops Dialer app."""
    self._device.adb.shell(['am', 'force-stop', DIALER_PACKAGE_NAME])
