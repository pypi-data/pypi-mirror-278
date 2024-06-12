from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdistanceCls:
	"""Fdistance commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdistance", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Left: float: No parameter help available
			- Right: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left'),
			ArgStruct.scalar_float('Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left: float = None
			self.Right: float = None

	def get(self, sEGMent=repcap.SEGMent.Default) -> GetStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:FDIStance \n
		Snippet: value: GetStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.fdistance.get(sEGMent = repcap.SEGMent.Default) \n
		No command help available \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:FDIStance?', self.__class__.GetStruct())
