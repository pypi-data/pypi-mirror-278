from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, sc_spacing: enums.SubCarrSpacing, dl_slots: int, dl_symbols: int, ul_slots: int, ul_symbols: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:ULDL:PATTern \n
		Snippet: driver.configure.nrSubMeas.ulDl.pattern.set(sc_spacing = enums.SubCarrSpacing.S15K, dl_slots = 1, dl_symbols = 1, ul_slots = 1, ul_symbols = 1) \n
		Configures the TDD UL-DL pattern for the <SCSpacing>. The ranges have dependencies, see 'TDD UL-DL configuration'. \n
			:param sc_spacing: S15K | S30K | S60K Subcarrier spacing for which the other settings apply.
			:param dl_slots: numeric Specifies 'nrofDownlinkSlots'. Range: 0 to 38
			:param dl_symbols: numeric Specifies 'nrofDownlinkSymbols'. Range: 0 to 14
			:param ul_slots: numeric Specifies 'nrofUplinkSlots'. Range: 1 to 40
			:param ul_symbols: numeric Specifies 'nrofUplinkSymbols'. Range: 0 to 14
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sc_spacing', sc_spacing, DataType.Enum, enums.SubCarrSpacing), ArgSingle('dl_slots', dl_slots, DataType.Integer), ArgSingle('dl_symbols', dl_symbols, DataType.Integer), ArgSingle('ul_slots', ul_slots, DataType.Integer), ArgSingle('ul_symbols', ul_symbols, DataType.Integer))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:ULDL:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Dl_Slots: int: numeric Specifies 'nrofDownlinkSlots'. Range: 0 to 38
			- Dl_Symbols: int: numeric Specifies 'nrofDownlinkSymbols'. Range: 0 to 14
			- Ul_Slots: int: numeric Specifies 'nrofUplinkSlots'. Range: 1 to 40
			- Ul_Symbols: int: numeric Specifies 'nrofUplinkSymbols'. Range: 0 to 14"""
		__meta_args_list = [
			ArgStruct.scalar_int('Dl_Slots'),
			ArgStruct.scalar_int('Dl_Symbols'),
			ArgStruct.scalar_int('Ul_Slots'),
			ArgStruct.scalar_int('Ul_Symbols')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dl_Slots: int = None
			self.Dl_Symbols: int = None
			self.Ul_Slots: int = None
			self.Ul_Symbols: int = None

	def get(self, sc_spacing: enums.SubCarrSpacing) -> GetStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:ULDL:PATTern \n
		Snippet: value: GetStruct = driver.configure.nrSubMeas.ulDl.pattern.get(sc_spacing = enums.SubCarrSpacing.S15K) \n
		Configures the TDD UL-DL pattern for the <SCSpacing>. The ranges have dependencies, see 'TDD UL-DL configuration'. \n
			:param sc_spacing: S15K | S30K | S60K Subcarrier spacing for which the other settings apply.
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.enum_scalar_to_str(sc_spacing, enums.SubCarrSpacing)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:ULDL:PATTern? {param}', self.__class__.GetStruct())
