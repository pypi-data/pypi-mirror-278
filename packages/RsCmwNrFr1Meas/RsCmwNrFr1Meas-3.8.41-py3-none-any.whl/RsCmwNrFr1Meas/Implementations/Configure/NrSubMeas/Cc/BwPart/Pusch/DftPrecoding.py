from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DftPrecodingCls:
	"""DftPrecoding commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dftPrecoding", core, parent)

	def set(self, bwp: enums.BandwidthPart, dft_precoding: bool, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:BWPart:PUSCh:DFTPrecoding \n
		Snippet: driver.configure.nrSubMeas.cc.bwPart.pusch.dftPrecoding.set(bwp = enums.BandwidthPart.BWP0, dft_precoding = False, carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies whether the <BWP> on carrier <no> uses a transform precoding function. \n
			:param bwp: BWP0
			:param dft_precoding: OFF | ON OFF: No transform precoding. ON: With transform precoding.
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bwp', bwp, DataType.Enum, enums.BandwidthPart), ArgSingle('dft_precoding', dft_precoding, DataType.Boolean))
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:BWPart:PUSCh:DFTPrecoding {param}'.rstrip())

	def get(self, bwp: enums.BandwidthPart, carrierComponent=repcap.CarrierComponent.Default) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:BWPart:PUSCh:DFTPrecoding \n
		Snippet: value: bool = driver.configure.nrSubMeas.cc.bwPart.pusch.dftPrecoding.get(bwp = enums.BandwidthPart.BWP0, carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies whether the <BWP> on carrier <no> uses a transform precoding function. \n
			:param bwp: BWP0
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: dft_precoding: OFF | ON OFF: No transform precoding. ON: With transform precoding."""
		param = Conversions.enum_scalar_to_str(bwp, enums.BandwidthPart)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:BWPart:PUSCh:DFTPrecoding? {param}')
		return Conversions.str_to_bool(response)
