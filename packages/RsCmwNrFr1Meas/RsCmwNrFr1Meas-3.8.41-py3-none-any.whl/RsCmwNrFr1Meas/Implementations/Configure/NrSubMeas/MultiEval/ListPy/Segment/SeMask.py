from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeMaskCls:
	"""SeMask commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seMask", core, parent)

	def set(self, sem_statistics: int, se_enable: bool, obw_enable: bool, sem_enable: bool, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:SEMask \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.segment.seMask.set(sem_statistics = 1, se_enable = False, obw_enable = False, sem_enable = False, sEGMent = repcap.SEGMent.Default) \n
		Defines settings for spectrum emission measurements in list mode for segment <no>. \n
			:param sem_statistics: integer Statistical length in slots Range: 1 to 1000
			:param se_enable: OFF | ON Enable or disable the measurement of spectrum emission results. ON: Spectrum emission results are measured according to the other enable flags in this command. Results for which there is no explicit enable flag are also measured. OFF: No spectrum emission results at all are measured. The other enable flags in this command are ignored.
			:param obw_enable: OFF | ON Enable or disable measurement of occupied bandwidth.
			:param sem_enable: OFF | ON Enable or disable measurement of spectrum emission trace and margin results.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sem_statistics', sem_statistics, DataType.Integer), ArgSingle('se_enable', se_enable, DataType.Boolean), ArgSingle('obw_enable', obw_enable, DataType.Boolean), ArgSingle('sem_enable', sem_enable, DataType.Boolean))
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:SEMask {param}'.rstrip())

	# noinspection PyTypeChecker
	class SeMaskStruct(StructBase):
		"""Response structure. Fields: \n
			- Sem_Statistics: int: integer Statistical length in slots Range: 1 to 1000
			- Se_Enable: bool: OFF | ON Enable or disable the measurement of spectrum emission results. ON: Spectrum emission results are measured according to the other enable flags in this command. Results for which there is no explicit enable flag are also measured. OFF: No spectrum emission results at all are measured. The other enable flags in this command are ignored.
			- Obw_Enable: bool: OFF | ON Enable or disable measurement of occupied bandwidth.
			- Sem_Enable: bool: OFF | ON Enable or disable measurement of spectrum emission trace and margin results."""
		__meta_args_list = [
			ArgStruct.scalar_int('Sem_Statistics'),
			ArgStruct.scalar_bool('Se_Enable'),
			ArgStruct.scalar_bool('Obw_Enable'),
			ArgStruct.scalar_bool('Sem_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sem_Statistics: int = None
			self.Se_Enable: bool = None
			self.Obw_Enable: bool = None
			self.Sem_Enable: bool = None

	def get(self, sEGMent=repcap.SEGMent.Default) -> SeMaskStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:SEMask \n
		Snippet: value: SeMaskStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.seMask.get(sEGMent = repcap.SEGMent.Default) \n
		Defines settings for spectrum emission measurements in list mode for segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for SeMaskStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:SEMask?', self.__class__.SeMaskStruct())
