from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcSpacingCls:
	"""AcSpacing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("acSpacing", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CAGGregation:ACSPacing \n
		Snippet: driver.configure.nrSubMeas.caggregation.acSpacing.set() \n
		Adjusts the component carrier frequencies, so that the carriers are aggregated contiguously, with nominal channel spacing. \n
		"""
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CAGGregation:ACSPacing')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CAGGregation:ACSPacing \n
		Snippet: driver.configure.nrSubMeas.caggregation.acSpacing.set_with_opc() \n
		Adjusts the component carrier frequencies, so that the carriers are aggregated contiguously, with nominal channel spacing. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwNrFr1Meas.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:NRSub:MEASurement<Instance>:CAGGregation:ACSPacing', opc_timeout_ms)
