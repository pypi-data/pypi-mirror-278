from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcSpacingCls:
	"""AcSpacing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("acSpacing", core, parent)

	def set(self, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>:CAGGregation:ACSPacing \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.caggregation.acSpacing.set(sEGMent = repcap.SEGMent.Default) \n
		Adjusts the component carrier frequencies in segment <no>, so that the carriers are aggregated contiguously. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CAGGregation:ACSPacing')

	def set_with_opc(self, sEGMent=repcap.SEGMent.Default, opc_timeout_ms: int = -1) -> None:
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>:CAGGregation:ACSPacing \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.caggregation.acSpacing.set_with_opc(sEGMent = repcap.SEGMent.Default) \n
		Adjusts the component carrier frequencies in segment <no>, so that the carriers are aggregated contiguously. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwNrFr1Meas.utilities.opc_timeout_set() to set the timeout value. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CAGGregation:ACSPacing', opc_timeout_ms)
