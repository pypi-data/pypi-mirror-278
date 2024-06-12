from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxBwidthCls:
	"""TxBwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("txBwidth", core, parent)

	# noinspection PyTypeChecker
	def get_sc_spacing(self) -> enums.SubCarrSpacing:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CCALl:TXBWidth:SCSPacing \n
		Snippet: value: enums.SubCarrSpacing = driver.configure.nrSubMeas.ccall.txBwidth.get_sc_spacing() \n
		Selects the subcarrier spacing for the measurement, for all carriers. \n
			:return: used_scs: S15K | S30K | S60K
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:CCALl:TXBWidth:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.SubCarrSpacing)

	def set_sc_spacing(self, used_scs: enums.SubCarrSpacing) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CCALl:TXBWidth:SCSPacing \n
		Snippet: driver.configure.nrSubMeas.ccall.txBwidth.set_sc_spacing(used_scs = enums.SubCarrSpacing.S15K) \n
		Selects the subcarrier spacing for the measurement, for all carriers. \n
			:param used_scs: S15K | S30K | S60K
		"""
		param = Conversions.enum_scalar_to_str(used_scs, enums.SubCarrSpacing)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CCALl:TXBWidth:SCSPacing {param}')
