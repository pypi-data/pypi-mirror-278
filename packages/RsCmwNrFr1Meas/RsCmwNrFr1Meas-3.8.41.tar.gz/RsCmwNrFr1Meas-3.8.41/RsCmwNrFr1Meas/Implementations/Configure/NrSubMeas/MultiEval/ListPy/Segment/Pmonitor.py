from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PmonitorCls:
	"""Pmonitor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pmonitor", core, parent)

	def set(self, enable: bool, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:PMONitor \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.segment.pmonitor.set(enable = False, sEGMent = repcap.SEGMent.Default) \n
		Enables or disables the measurement of power monitor results for segment <no>. \n
			:param enable: OFF | ON
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		param = Conversions.bool_to_str(enable)
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PMONitor {param}')

	def get(self, sEGMent=repcap.SEGMent.Default) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:PMONitor \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.listPy.segment.pmonitor.get(sEGMent = repcap.SEGMent.Default) \n
		Enables or disables the measurement of power monitor results for segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: enable: OFF | ON"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PMONitor?')
		return Conversions.str_to_bool(response)
