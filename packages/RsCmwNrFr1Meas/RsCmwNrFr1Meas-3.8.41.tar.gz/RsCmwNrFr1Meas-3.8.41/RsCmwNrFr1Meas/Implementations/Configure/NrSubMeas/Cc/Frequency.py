from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, analyzer_freq: float, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:FREQuency \n
		Snippet: driver.configure.nrSubMeas.cc.frequency.set(analyzer_freq = 1.0, carrierComponent = repcap.CarrierComponent.Default) \n
		Selects the center frequency of carrier <no>. Without carrier aggregation, you can omit CC<no>. Using the unit CH, the
		frequency can be set via the channel number. The allowed channel number range depends on the operating band, see
		'Frequency bands'. For the supported frequency range, see 'Frequency ranges'. \n
			:param analyzer_freq: numeric Unit: Hz
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
		"""
		param = Conversions.decimal_value_to_str(analyzer_freq)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:FREQuency {param}')

	def get(self, carrierComponent=repcap.CarrierComponent.Default) -> float:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:FREQuency \n
		Snippet: value: float = driver.configure.nrSubMeas.cc.frequency.get(carrierComponent = repcap.CarrierComponent.Default) \n
		Selects the center frequency of carrier <no>. Without carrier aggregation, you can omit CC<no>. Using the unit CH, the
		frequency can be set via the channel number. The allowed channel number range depends on the operating band, see
		'Frequency bands'. For the supported frequency range, see 'Frequency ranges'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: analyzer_freq: numeric Unit: Hz"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
