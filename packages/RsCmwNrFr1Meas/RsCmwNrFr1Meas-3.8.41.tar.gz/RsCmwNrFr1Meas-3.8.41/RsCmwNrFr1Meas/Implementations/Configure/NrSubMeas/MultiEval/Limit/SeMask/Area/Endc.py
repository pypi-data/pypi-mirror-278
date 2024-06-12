from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EndcCls:
	"""Endc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("endc", core, parent)

	def set(self, enable: bool, frequency_start: float, frequency_end: float, level: float, rbw: enums.RbwA, area=repcap.Area.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA<nr>:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.area.endc.set(enable = False, frequency_start = 1.0, frequency_end = 1.0, level = 1.0, rbw = enums.RbwA.K030, area = repcap.Area.Default) \n
		Defines general requirements for area number <no> of the user-defined emission mask for EN-DC. The activation state, the
		area borders, an upper limit and the resolution bandwidth must be specified. \n
			:param enable: OFF | ON OFF: Disables the check of these requirements. ON: Enables the check of these requirements.
			:param frequency_start: numeric Start frequency of the area, relative to the edges of the aggregated channel bandwidth. Range: 0 MHz to 120 MHz, Unit: Hz
			:param frequency_end: numeric Stop frequency of the area, relative to the edges of the aggregated channel bandwidth. Range: 0 MHz to 125 MHz, Unit: Hz
			:param level: numeric Upper limit for the area Range: -256 dBm to 256 dBm, Unit: dBm
			:param rbw: K030 | PC1 | M1 Resolution bandwidth to be used for the area. K030: 30 kHz PC1: 1 % of aggregated channel bandwidth M1: 1 MHz
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('frequency_start', frequency_start, DataType.Float), ArgSingle('frequency_end', frequency_end, DataType.Float), ArgSingle('level', level, DataType.Float), ArgSingle('rbw', rbw, DataType.Enum, enums.RbwA))
		area_cmd_val = self._cmd_group.get_repcap_cmd_value(area, repcap.Area)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA{area_cmd_val}:ENDC {param}'.rstrip())

	# noinspection PyTypeChecker
	class EndcStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON OFF: Disables the check of these requirements. ON: Enables the check of these requirements.
			- Frequency_Start: float: numeric Start frequency of the area, relative to the edges of the aggregated channel bandwidth. Range: 0 MHz to 120 MHz, Unit: Hz
			- Frequency_End: float: numeric Stop frequency of the area, relative to the edges of the aggregated channel bandwidth. Range: 0 MHz to 125 MHz, Unit: Hz
			- Level: float: numeric Upper limit for the area Range: -256 dBm to 256 dBm, Unit: dBm
			- Rbw: enums.RbwA: K030 | PC1 | M1 Resolution bandwidth to be used for the area. K030: 30 kHz PC1: 1 % of aggregated channel bandwidth M1: 1 MHz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Frequency_Start'),
			ArgStruct.scalar_float('Frequency_End'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_enum('Rbw', enums.RbwA)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Frequency_Start: float = None
			self.Frequency_End: float = None
			self.Level: float = None
			self.Rbw: enums.RbwA = None

	def get(self, area=repcap.Area.Default) -> EndcStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA<nr>:ENDC \n
		Snippet: value: EndcStruct = driver.configure.nrSubMeas.multiEval.limit.seMask.area.endc.get(area = repcap.Area.Default) \n
		Defines general requirements for area number <no> of the user-defined emission mask for EN-DC. The activation state, the
		area borders, an upper limit and the resolution bandwidth must be specified. \n
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:return: structure: for return value, see the help for EndcStruct structure arguments."""
		area_cmd_val = self._cmd_group.get_repcap_cmd_value(area, repcap.Area)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA{area_cmd_val}:ENDC?', self.__class__.EndcStruct())
