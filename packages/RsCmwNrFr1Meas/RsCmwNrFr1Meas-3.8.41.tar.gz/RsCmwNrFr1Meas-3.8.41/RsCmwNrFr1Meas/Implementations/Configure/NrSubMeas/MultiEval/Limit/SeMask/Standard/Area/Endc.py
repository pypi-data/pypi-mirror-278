from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EndcCls:
	"""Endc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("endc", core, parent)

	def set(self, enable: bool, areaReduced=repcap.AreaReduced.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:AREA<nr>:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.standard.area.endc.set(enable = False, areaReduced = repcap.AreaReduced.Default) \n
		Configures the activation state of area number <no> of the standard emission mask for EN-DC. \n
			:param enable: OFF | ON OFF: disables the limit check for this area ON: enables the limit check for this area
			:param areaReduced: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
		"""
		param = Conversions.bool_to_str(enable)
		areaReduced_cmd_val = self._cmd_group.get_repcap_cmd_value(areaReduced, repcap.AreaReduced)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:AREA{areaReduced_cmd_val}:ENDC {param}')

	def get(self, areaReduced=repcap.AreaReduced.Default) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:AREA<nr>:ENDC \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.limit.seMask.standard.area.endc.get(areaReduced = repcap.AreaReduced.Default) \n
		Configures the activation state of area number <no> of the standard emission mask for EN-DC. \n
			:param areaReduced: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:return: enable: OFF | ON OFF: disables the limit check for this area ON: enables the limit check for this area"""
		areaReduced_cmd_val = self._cmd_group.get_repcap_cmd_value(areaReduced, repcap.AreaReduced)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:AREA{areaReduced_cmd_val}:ENDC?')
		return Conversions.str_to_bool(response)
