from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Low: List[float]: float EVM value for low EVM window position. Unit: %
			- High: List[float]: float EVM value for high EVM window position. Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Low', DataType.FloatList, None, False, True, 1),
			ArgStruct('High', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Low: List[float] = None
			self.High: List[float] = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:EVMagnitude:PEAK:MAXimum \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.evMagnitude.peak.maximum.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the values of the EVM peak bar graphs for the OFDM symbols in the measured slot, for carrier <no>. The results of
		the current, average and maximum bar graphs can be retrieved. There is one pair of EVM values per OFDM symbol, returned
		in the following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also 'View EVM'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:EVMagnitude:PEAK:MAXimum?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:EVMagnitude:PEAK:MAXimum \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.evMagnitude.peak.maximum.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the values of the EVM peak bar graphs for the OFDM symbols in the measured slot, for carrier <no>. The results of
		the current, average and maximum bar graphs can be retrieved. There is one pair of EVM values per OFDM symbol, returned
		in the following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also 'View EVM'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:EVMagnitude:PEAK:MAXimum?', self.__class__.ResultData())
