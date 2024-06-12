from enum import Enum


# noinspection SpellCheckingInspection
class AllocatedSlots(Enum):
	"""1 Members, ALL ... ALL"""
	ALL = 0


# noinspection SpellCheckingInspection
class Band(Enum):
	"""57 Members, OB1 ... OB99"""
	OB1 = 0
	OB105 = 1
	OB12 = 2
	OB13 = 3
	OB14 = 4
	OB18 = 5
	OB2 = 6
	OB20 = 7
	OB24 = 8
	OB25 = 9
	OB255 = 10
	OB256 = 11
	OB26 = 12
	OB28 = 13
	OB3 = 14
	OB30 = 15
	OB34 = 16
	OB38 = 17
	OB39 = 18
	OB40 = 19
	OB41 = 20
	OB46 = 21
	OB47 = 22
	OB48 = 23
	OB5 = 24
	OB50 = 25
	OB51 = 26
	OB53 = 27
	OB65 = 28
	OB66 = 29
	OB7 = 30
	OB70 = 31
	OB71 = 32
	OB74 = 33
	OB75 = 34
	OB76 = 35
	OB77 = 36
	OB78 = 37
	OB79 = 38
	OB8 = 39
	OB80 = 40
	OB81 = 41
	OB82 = 42
	OB83 = 43
	OB84 = 44
	OB85 = 45
	OB86 = 46
	OB89 = 47
	OB90 = 48
	OB91 = 49
	OB92 = 50
	OB93 = 51
	OB94 = 52
	OB95 = 53
	OB97 = 54
	OB98 = 55
	OB99 = 56


# noinspection SpellCheckingInspection
class BandwidthPart(Enum):
	"""1 Members, BWP0 ... BWP0"""
	BWP0 = 0


# noinspection SpellCheckingInspection
class CarrierComponent(Enum):
	"""2 Members, CC1 ... CC2"""
	CC1 = 0
	CC2 = 1


# noinspection SpellCheckingInspection
class CarrierPosition(Enum):
	"""2 Members, LONR ... RONR"""
	LONR = 0
	RONR = 1


# noinspection SpellCheckingInspection
class ChannelBwidth(Enum):
	"""15 Members, B005 ... B100"""
	B005 = 0
	B010 = 1
	B015 = 2
	B020 = 3
	B025 = 4
	B030 = 5
	B035 = 6
	B040 = 7
	B045 = 8
	B050 = 9
	B060 = 10
	B070 = 11
	B080 = 12
	B090 = 13
	B100 = 14


# noinspection SpellCheckingInspection
class ChannelBwidthB(Enum):
	"""4 Members, B005 ... B020"""
	B005 = 0
	B010 = 1
	B015 = 2
	B020 = 3


# noinspection SpellCheckingInspection
class ChannelTypeA(Enum):
	"""2 Members, PUCCh ... PUSCh"""
	PUCCh = 0
	PUSCh = 1


# noinspection SpellCheckingInspection
class ChannelTypeB(Enum):
	"""4 Members, OFF ... PUSCh"""
	OFF = 0
	ON = 1
	PUCCh = 2
	PUSCh = 3


# noinspection SpellCheckingInspection
class CmwsConnector(Enum):
	"""48 Members, R11 ... RB8"""
	R11 = 0
	R12 = 1
	R13 = 2
	R14 = 3
	R15 = 4
	R16 = 5
	R17 = 6
	R18 = 7
	R21 = 8
	R22 = 9
	R23 = 10
	R24 = 11
	R25 = 12
	R26 = 13
	R27 = 14
	R28 = 15
	R31 = 16
	R32 = 17
	R33 = 18
	R34 = 19
	R35 = 20
	R36 = 21
	R37 = 22
	R38 = 23
	R41 = 24
	R42 = 25
	R43 = 26
	R44 = 27
	R45 = 28
	R46 = 29
	R47 = 30
	R48 = 31
	RA1 = 32
	RA2 = 33
	RA3 = 34
	RA4 = 35
	RA5 = 36
	RA6 = 37
	RA7 = 38
	RA8 = 39
	RB1 = 40
	RB2 = 41
	RB3 = 42
	RB4 = 43
	RB5 = 44
	RB6 = 45
	RB7 = 46
	RB8 = 47


# noinspection SpellCheckingInspection
class ConfigType(Enum):
	"""2 Members, T1 ... T2"""
	T1 = 0
	T2 = 1


# noinspection SpellCheckingInspection
class CyclicPrefix(Enum):
	"""2 Members, EXTended ... NORMal"""
	EXTended = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class DuplexModeB(Enum):
	"""2 Members, FDD ... TDD"""
	FDD = 0
	TDD = 1


# noinspection SpellCheckingInspection
class Generator(Enum):
	"""2 Members, DID ... PHY"""
	DID = 0
	PHY = 1


# noinspection SpellCheckingInspection
class Lagging(Enum):
	"""3 Members, MS05 ... OFF"""
	MS05 = 0
	MS25 = 1
	OFF = 2


# noinspection SpellCheckingInspection
class Leading(Enum):
	"""2 Members, MS25 ... OFF"""
	MS25 = 0
	OFF = 1


# noinspection SpellCheckingInspection
class ListMode(Enum):
	"""2 Members, ONCE ... SEGMent"""
	ONCE = 0
	SEGMent = 1


# noinspection SpellCheckingInspection
class LowHigh(Enum):
	"""2 Members, HIGH ... LOW"""
	HIGH = 0
	LOW = 1


# noinspection SpellCheckingInspection
class MappingType(Enum):
	"""2 Members, A ... B"""
	A = 0
	B = 1


# noinspection SpellCheckingInspection
class MaxLength(Enum):
	"""2 Members, DOUBle ... SINGle"""
	DOUBle = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class MeasFilter(Enum):
	"""2 Members, BANDpass ... GAUSs"""
	BANDpass = 0
	GAUSs = 1


# noinspection SpellCheckingInspection
class MeasurementMode(Enum):
	"""2 Members, MELMode ... NORMal"""
	MELMode = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class MeasureSlot(Enum):
	"""6 Members, ALL ... UDEF"""
	ALL = 0
	MS0 = 1
	MS1 = 2
	MS2 = 3
	MS3 = 4
	UDEF = 5


# noinspection SpellCheckingInspection
class MevLimit(Enum):
	"""2 Members, STD ... UDEF"""
	STD = 0
	UDEF = 1


# noinspection SpellCheckingInspection
class Modulation(Enum):
	"""6 Members, BPSK ... QPSK"""
	BPSK = 0
	BPWS = 1
	Q16 = 2
	Q256 = 3
	Q64 = 4
	QPSK = 5


# noinspection SpellCheckingInspection
class ModulationScheme(Enum):
	"""7 Members, AUTO ... QPSK"""
	AUTO = 0
	BPSK = 1
	BPWS = 2
	Q16 = 3
	Q256 = 4
	Q64 = 5
	QPSK = 6


# noinspection SpellCheckingInspection
class NbTrigger(Enum):
	"""4 Members, M010 ... M080"""
	M010 = 0
	M020 = 1
	M040 = 2
	M080 = 3


# noinspection SpellCheckingInspection
class NetworkSigVal(Enum):
	"""33 Members, NS01 ... NS35"""
	NS01 = 0
	NS02 = 1
	NS03 = 2
	NS04 = 3
	NS05 = 4
	NS06 = 5
	NS07 = 6
	NS08 = 7
	NS09 = 8
	NS10 = 9
	NS11 = 10
	NS12 = 11
	NS13 = 12
	NS14 = 13
	NS15 = 14
	NS16 = 15
	NS17 = 16
	NS18 = 17
	NS19 = 18
	NS20 = 19
	NS21 = 20
	NS22 = 21
	NS23 = 22
	NS24 = 23
	NS25 = 24
	NS26 = 25
	NS27 = 26
	NS28 = 27
	NS29 = 28
	NS30 = 29
	NS31 = 30
	NS32 = 31
	NS35 = 32


# noinspection SpellCheckingInspection
class ParameterSetMode(Enum):
	"""2 Members, GLOBal ... LIST"""
	GLOBal = 0
	LIST = 1


# noinspection SpellCheckingInspection
class Periodicity(Enum):
	"""9 Members, MS05 ... MS5"""
	MS05 = 0
	MS1 = 1
	MS10 = 2
	MS125 = 3
	MS2 = 4
	MS25 = 5
	MS3 = 6
	MS4 = 7
	MS5 = 8


# noinspection SpellCheckingInspection
class PhaseComp(Enum):
	"""3 Members, CAF ... UDEF"""
	CAF = 0
	OFF = 1
	UDEF = 2


# noinspection SpellCheckingInspection
class PucchFormat(Enum):
	"""7 Members, F1 ... F3"""
	F1 = 0
	F1A = 1
	F1B = 2
	F2 = 3
	F2A = 4
	F2B = 5
	F3 = 6


# noinspection SpellCheckingInspection
class RbwA(Enum):
	"""3 Members, K030 ... PC1"""
	K030 = 0
	M1 = 1
	PC1 = 2


# noinspection SpellCheckingInspection
class RbwB(Enum):
	"""6 Members, K030 ... PC2"""
	K030 = 0
	K100 = 1
	K400 = 2
	M1 = 3
	PC1 = 4
	PC2 = 5


# noinspection SpellCheckingInspection
class RbwC(Enum):
	"""3 Members, K030 ... M1"""
	K030 = 0
	K400 = 1
	M1 = 2


# noinspection SpellCheckingInspection
class Repeat(Enum):
	"""2 Members, CONTinuous ... SINGleshot"""
	CONTinuous = 0
	SINGleshot = 1


# noinspection SpellCheckingInspection
class ResourceState(Enum):
	"""8 Members, ACTive ... RUN"""
	ACTive = 0
	ADJusted = 1
	INValid = 2
	OFF = 3
	PENDing = 4
	QUEued = 5
	RDY = 6
	RUN = 7


# noinspection SpellCheckingInspection
class ResultStatus2(Enum):
	"""10 Members, DC ... ULEU"""
	DC = 0
	INV = 1
	NAV = 2
	NCAP = 3
	OFF = 4
	OFL = 5
	OK = 6
	UFL = 7
	ULEL = 8
	ULEU = 9


# noinspection SpellCheckingInspection
class RetriggerFlag(Enum):
	"""4 Members, IFPNarrowband ... ON"""
	IFPNarrowband = 0
	IFPower = 1
	OFF = 2
	ON = 3


# noinspection SpellCheckingInspection
class RxConnector(Enum):
	"""154 Members, I11I ... RH8"""
	I11I = 0
	I13I = 1
	I15I = 2
	I17I = 3
	I21I = 4
	I23I = 5
	I25I = 6
	I27I = 7
	I31I = 8
	I33I = 9
	I35I = 10
	I37I = 11
	I41I = 12
	I43I = 13
	I45I = 14
	I47I = 15
	IF1 = 16
	IF2 = 17
	IF3 = 18
	IQ1I = 19
	IQ3I = 20
	IQ5I = 21
	IQ7I = 22
	R11 = 23
	R11C = 24
	R12 = 25
	R12C = 26
	R12I = 27
	R13 = 28
	R13C = 29
	R14 = 30
	R14C = 31
	R14I = 32
	R15 = 33
	R16 = 34
	R17 = 35
	R18 = 36
	R21 = 37
	R21C = 38
	R22 = 39
	R22C = 40
	R22I = 41
	R23 = 42
	R23C = 43
	R24 = 44
	R24C = 45
	R24I = 46
	R25 = 47
	R26 = 48
	R27 = 49
	R28 = 50
	R31 = 51
	R31C = 52
	R32 = 53
	R32C = 54
	R32I = 55
	R33 = 56
	R33C = 57
	R34 = 58
	R34C = 59
	R34I = 60
	R35 = 61
	R36 = 62
	R37 = 63
	R38 = 64
	R41 = 65
	R41C = 66
	R42 = 67
	R42C = 68
	R42I = 69
	R43 = 70
	R43C = 71
	R44 = 72
	R44C = 73
	R44I = 74
	R45 = 75
	R46 = 76
	R47 = 77
	R48 = 78
	RA1 = 79
	RA2 = 80
	RA3 = 81
	RA4 = 82
	RA5 = 83
	RA6 = 84
	RA7 = 85
	RA8 = 86
	RB1 = 87
	RB2 = 88
	RB3 = 89
	RB4 = 90
	RB5 = 91
	RB6 = 92
	RB7 = 93
	RB8 = 94
	RC1 = 95
	RC2 = 96
	RC3 = 97
	RC4 = 98
	RC5 = 99
	RC6 = 100
	RC7 = 101
	RC8 = 102
	RD1 = 103
	RD2 = 104
	RD3 = 105
	RD4 = 106
	RD5 = 107
	RD6 = 108
	RD7 = 109
	RD8 = 110
	RE1 = 111
	RE2 = 112
	RE3 = 113
	RE4 = 114
	RE5 = 115
	RE6 = 116
	RE7 = 117
	RE8 = 118
	RF1 = 119
	RF1C = 120
	RF2 = 121
	RF2C = 122
	RF2I = 123
	RF3 = 124
	RF3C = 125
	RF4 = 126
	RF4C = 127
	RF4I = 128
	RF5 = 129
	RF5C = 130
	RF6 = 131
	RF6C = 132
	RF7 = 133
	RF8 = 134
	RFAC = 135
	RFBC = 136
	RFBI = 137
	RG1 = 138
	RG2 = 139
	RG3 = 140
	RG4 = 141
	RG5 = 142
	RG6 = 143
	RG7 = 144
	RG8 = 145
	RH1 = 146
	RH2 = 147
	RH3 = 148
	RH4 = 149
	RH5 = 150
	RH6 = 151
	RH7 = 152
	RH8 = 153


# noinspection SpellCheckingInspection
class RxConverter(Enum):
	"""40 Members, IRX1 ... RX44"""
	IRX1 = 0
	IRX11 = 1
	IRX12 = 2
	IRX13 = 3
	IRX14 = 4
	IRX2 = 5
	IRX21 = 6
	IRX22 = 7
	IRX23 = 8
	IRX24 = 9
	IRX3 = 10
	IRX31 = 11
	IRX32 = 12
	IRX33 = 13
	IRX34 = 14
	IRX4 = 15
	IRX41 = 16
	IRX42 = 17
	IRX43 = 18
	IRX44 = 19
	RX1 = 20
	RX11 = 21
	RX12 = 22
	RX13 = 23
	RX14 = 24
	RX2 = 25
	RX21 = 26
	RX22 = 27
	RX23 = 28
	RX24 = 29
	RX3 = 30
	RX31 = 31
	RX32 = 32
	RX33 = 33
	RX34 = 34
	RX4 = 35
	RX41 = 36
	RX42 = 37
	RX43 = 38
	RX44 = 39


# noinspection SpellCheckingInspection
class Scenario(Enum):
	"""4 Members, CSPath ... SALone"""
	CSPath = 0
	MAPRotocol = 1
	NAV = 2
	SALone = 3


# noinspection SpellCheckingInspection
class SignalSlope(Enum):
	"""2 Members, FEDGe ... REDGe"""
	FEDGe = 0
	REDGe = 1


# noinspection SpellCheckingInspection
class StopCondition(Enum):
	"""2 Members, NONE ... SLFail"""
	NONE = 0
	SLFail = 1


# noinspection SpellCheckingInspection
class SubCarrSpacing(Enum):
	"""3 Members, S15K ... S60K"""
	S15K = 0
	S30K = 1
	S60K = 2


# noinspection SpellCheckingInspection
class SyncMode(Enum):
	"""4 Members, ENHanced ... NSSLot"""
	ENHanced = 0
	ESSLot = 1
	NORMal = 2
	NSSLot = 3


# noinspection SpellCheckingInspection
class TimeMask(Enum):
	"""3 Members, GOO ... SBLanking"""
	GOO = 0
	PPSRs = 1
	SBLanking = 2
