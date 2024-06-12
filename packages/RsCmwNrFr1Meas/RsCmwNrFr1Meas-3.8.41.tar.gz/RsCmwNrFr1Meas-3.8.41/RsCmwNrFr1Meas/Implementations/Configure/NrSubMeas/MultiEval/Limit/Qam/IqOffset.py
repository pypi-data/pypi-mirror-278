from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqOffsetCls:
	"""IqOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqOffset", core, parent)

	def set(self, enable: bool, offset_0: float, offset_1: float, offset_2: float, offset_3: float, qam=repcap.Qam.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:IQOFfset \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.qam.iqOffset.set(enable = False, offset_0 = 1.0, offset_1 = 1.0, offset_2 = 1.0, offset_3 = 1.0, qam = repcap.Qam.Default) \n
		Defines upper limits for the I/Q origin offset (QAM modulations) . Four different I/Q origin offset limits can be set for
		four TX power ranges. \n
			:param enable: OFF | ON OFF: disables the limit check ON: enables the limit check
			:param offset_0: numeric I/Q origin offset limit for TX power 10 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			:param offset_1: numeric I/Q origin offset limit for TX power 0 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			:param offset_2: numeric I/Q origin offset limit for TX power -30 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			:param offset_3: numeric I/Q origin offset limit for TX power -40 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('offset_0', offset_0, DataType.Float), ArgSingle('offset_1', offset_1, DataType.Float), ArgSingle('offset_2', offset_2, DataType.Float), ArgSingle('offset_3', offset_3, DataType.Float))
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:IQOFfset {param}'.rstrip())

	# noinspection PyTypeChecker
	class IqOffsetStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON OFF: disables the limit check ON: enables the limit check
			- Offset_0: float: numeric I/Q origin offset limit for TX power 10 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			- Offset_1: float: numeric I/Q origin offset limit for TX power 0 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			- Offset_2: float: numeric I/Q origin offset limit for TX power -30 dBm Range: -256 dBc to 256 dBc, Unit: dBc
			- Offset_3: float: numeric I/Q origin offset limit for TX power -40 dBm Range: -256 dBc to 256 dBc, Unit: dBc"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Offset_0'),
			ArgStruct.scalar_float('Offset_1'),
			ArgStruct.scalar_float('Offset_2'),
			ArgStruct.scalar_float('Offset_3')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Offset_0: float = None
			self.Offset_1: float = None
			self.Offset_2: float = None
			self.Offset_3: float = None

	def get(self, qam=repcap.Qam.Default) -> IqOffsetStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:IQOFfset \n
		Snippet: value: IqOffsetStruct = driver.configure.nrSubMeas.multiEval.limit.qam.iqOffset.get(qam = repcap.Qam.Default) \n
		Defines upper limits for the I/Q origin offset (QAM modulations) . Four different I/Q origin offset limits can be set for
		four TX power ranges. \n
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
			:return: structure: for return value, see the help for IqOffsetStruct structure arguments."""
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:IQOFfset?', self.__class__.IqOffsetStruct())
