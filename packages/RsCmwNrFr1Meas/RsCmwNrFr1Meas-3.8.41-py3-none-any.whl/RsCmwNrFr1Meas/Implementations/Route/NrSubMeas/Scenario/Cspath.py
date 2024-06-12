from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CspathCls:
	"""Cspath commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cspath", core, parent)

	def set(self, master: str, carrier: str = None) -> None:
		"""SCPI: ROUTe:NRSub:MEASurement<Instance>:SCENario:CSPath \n
		Snippet: driver.route.nrSubMeas.scenario.cspath.set(master = 'abc', carrier = 'abc') \n
		No command help available \n
			:param master: No help available
			:param carrier: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('master', master, DataType.String), ArgSingle('carrier', carrier, DataType.String, None, is_optional=True))
		self._core.io.write(f'ROUTe:NRSub:MEASurement<Instance>:SCENario:CSPath {param}'.rstrip())

	# noinspection PyTypeChecker
	class CspathStruct(StructBase):
		"""Response structure. Fields: \n
			- Master: str: No parameter help available
			- Carrier: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Master'),
			ArgStruct.scalar_str('Carrier')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Master: str = None
			self.Carrier: str = None

	def get(self) -> CspathStruct:
		"""SCPI: ROUTe:NRSub:MEASurement<Instance>:SCENario:CSPath \n
		Snippet: value: CspathStruct = driver.route.nrSubMeas.scenario.cspath.get() \n
		No command help available \n
			:return: structure: for return value, see the help for CspathStruct structure arguments."""
		return self._core.io.query_struct(f'ROUTe:NRSub:MEASurement<Instance>:SCENario:CSPath?', self.__class__.CspathStruct())
