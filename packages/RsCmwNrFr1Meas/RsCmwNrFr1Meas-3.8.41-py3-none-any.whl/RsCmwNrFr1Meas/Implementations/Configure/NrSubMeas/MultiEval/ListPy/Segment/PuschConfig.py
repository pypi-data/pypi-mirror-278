from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschConfigCls:
	"""PuschConfig commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("puschConfig", core, parent)

	# noinspection PyTypeChecker
	class PuschConfigStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Mod_Scheme: enums.ModulationScheme: No parameter help available
			- Mapping_Type: enums.MappingType: No parameter help available
			- Nrb_Auto: bool: No parameter help available
			- No_Rb: int: No parameter help available
			- Start_Rb: int: No parameter help available
			- No_Symbols: int: No parameter help available
			- Start_Symbol: int: No parameter help available
			- Config_Type: enums.ConfigType: No parameter help available
			- Max_Length: enums.MaxLength: No parameter help available
			- Add_Position: int: No parameter help available
			- Lzero: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mod_Scheme', enums.ModulationScheme),
			ArgStruct.scalar_enum('Mapping_Type', enums.MappingType),
			ArgStruct.scalar_bool('Nrb_Auto'),
			ArgStruct.scalar_int('No_Rb'),
			ArgStruct.scalar_int('Start_Rb'),
			ArgStruct.scalar_int('No_Symbols'),
			ArgStruct.scalar_int('Start_Symbol'),
			ArgStruct.scalar_enum('Config_Type', enums.ConfigType),
			ArgStruct.scalar_enum('Max_Length', enums.MaxLength),
			ArgStruct.scalar_int('Add_Position'),
			ArgStruct.scalar_int('Lzero')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Scheme: enums.ModulationScheme = None
			self.Mapping_Type: enums.MappingType = None
			self.Nrb_Auto: bool = None
			self.No_Rb: int = None
			self.Start_Rb: int = None
			self.No_Symbols: int = None
			self.Start_Symbol: int = None
			self.Config_Type: enums.ConfigType = None
			self.Max_Length: enums.MaxLength = None
			self.Add_Position: int = None
			self.Lzero: int = None

	def set(self, structure: PuschConfigStruct, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:PUSChconfig \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.multiEval.listPy.segment.puschConfig.PuschConfigStruct() \n
		structure.Mod_Scheme: enums.ModulationScheme = enums.ModulationScheme.AUTO \n
		structure.Mapping_Type: enums.MappingType = enums.MappingType.A \n
		structure.Nrb_Auto: bool = False \n
		structure.No_Rb: int = 1 \n
		structure.Start_Rb: int = 1 \n
		structure.No_Symbols: int = 1 \n
		structure.Start_Symbol: int = 1 \n
		structure.Config_Type: enums.ConfigType = enums.ConfigType.T1 \n
		structure.Max_Length: enums.MaxLength = enums.MaxLength.DOUBle \n
		structure.Add_Position: int = 1 \n
		structure.Lzero: int = 1 \n
		driver.configure.nrSubMeas.multiEval.listPy.segment.puschConfig.set(structure, sEGMent = repcap.SEGMent.Default) \n
		No command help available \n
			:param structure: for set value, see the help for PuschConfigStruct structure arguments.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PUSChconfig', structure)

	def get(self, sEGMent=repcap.SEGMent.Default) -> PuschConfigStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:PUSChconfig \n
		Snippet: value: PuschConfigStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.puschConfig.get(sEGMent = repcap.SEGMent.Default) \n
		No command help available \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for PuschConfigStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PUSChconfig?', self.__class__.PuschConfigStruct())
