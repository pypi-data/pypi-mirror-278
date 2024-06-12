from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TaPositionCls:
	"""TaPosition commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("taPosition", core, parent)

	def set(self, position: int, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:TAPosition \n
		Snippet: driver.configure.nrSubMeas.cc.taPosition.set(position = 1, carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies the 'dmrs-TypeA-Position' for carrier <no>. \n
			:param position: numeric Number of the first DM-RS symbol for mapping type A. Range: 2 to 3
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
		"""
		param = Conversions.decimal_value_to_str(position)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:TAPosition {param}')

	def get(self, carrierComponent=repcap.CarrierComponent.Default) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:TAPosition \n
		Snippet: value: int = driver.configure.nrSubMeas.cc.taPosition.get(carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies the 'dmrs-TypeA-Position' for carrier <no>. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: position: numeric Number of the first DM-RS symbol for mapping type A. Range: 2 to 3"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:TAPosition?')
		return Conversions.str_to_int(response)
