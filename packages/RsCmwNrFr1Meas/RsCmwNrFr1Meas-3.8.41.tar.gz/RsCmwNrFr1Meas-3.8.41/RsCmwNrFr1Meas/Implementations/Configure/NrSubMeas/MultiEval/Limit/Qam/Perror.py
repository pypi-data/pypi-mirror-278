from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PerrorCls:
	"""Perror commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("perror", core, parent)

	def set(self, rms: float or bool, peak: float or bool, qam=repcap.Qam.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:PERRor \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.qam.perror.set(rms = 1.0, peak = 1.0, qam = repcap.Qam.Default) \n
		Defines symmetric limits for the RMS and peak values of the phase error for QAM modulations. The limit check fails if the
		absolute value of the measured phase error exceeds the specified values. \n
			:param rms: (float or boolean) numeric | ON | OFF Range: 0 deg to 180 deg, Unit: deg ON | OFF enables or disables the limit check.
			:param peak: (float or boolean) numeric | ON | OFF Range: 0 deg to 180 deg, Unit: deg ON | OFF enables or disables the limit check.
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('rms', rms, DataType.FloatExt), ArgSingle('peak', peak, DataType.FloatExt))
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:PERRor {param}'.rstrip())

	# noinspection PyTypeChecker
	class PerrorStruct(StructBase):
		"""Response structure. Fields: \n
			- Rms: float or bool: numeric | ON | OFF Range: 0 deg to 180 deg, Unit: deg ON | OFF enables or disables the limit check.
			- Peak: float or bool: numeric | ON | OFF Range: 0 deg to 180 deg, Unit: deg ON | OFF enables or disables the limit check."""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Rms'),
			ArgStruct.scalar_float_ext('Peak')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rms: float or bool = None
			self.Peak: float or bool = None

	def get(self, qam=repcap.Qam.Default) -> PerrorStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:PERRor \n
		Snippet: value: PerrorStruct = driver.configure.nrSubMeas.multiEval.limit.qam.perror.get(qam = repcap.Qam.Default) \n
		Defines symmetric limits for the RMS and peak values of the phase error for QAM modulations. The limit check fails if the
		absolute value of the measured phase error exceeds the specified values. \n
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
			:return: structure: for return value, see the help for PerrorStruct structure arguments."""
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:PERRor?', self.__class__.PerrorStruct())
