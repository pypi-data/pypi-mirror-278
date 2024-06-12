from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SgenerationCls:
	"""Sgeneration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sgeneration", core, parent)

	def set(self, generator: enums.Generator, dmrs_id: int, scid: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:SGENeration \n
		Snippet: driver.configure.nrSubMeas.multiEval.dmrs.sgeneration.set(generator = enums.Generator.DID, dmrs_id = 1, scid = 1) \n
		No command help available \n
			:param generator: No help available
			:param dmrs_id: No help available
			:param scid: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('generator', generator, DataType.Enum, enums.Generator), ArgSingle('dmrs_id', dmrs_id, DataType.Integer), ArgSingle('scid', scid, DataType.Integer))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:SGENeration {param}'.rstrip())

	# noinspection PyTypeChecker
	class SgenerationStruct(StructBase):
		"""Response structure. Fields: \n
			- Generator: enums.Generator: No parameter help available
			- Dmrs_Id: int: No parameter help available
			- Scid: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Generator', enums.Generator),
			ArgStruct.scalar_int('Dmrs_Id'),
			ArgStruct.scalar_int('Scid')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Generator: enums.Generator = None
			self.Dmrs_Id: int = None
			self.Scid: int = None

	def get(self) -> SgenerationStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:SGENeration \n
		Snippet: value: SgenerationStruct = driver.configure.nrSubMeas.multiEval.dmrs.sgeneration.get() \n
		No command help available \n
			:return: structure: for return value, see the help for SgenerationStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:SGENeration?', self.__class__.SgenerationStruct())
