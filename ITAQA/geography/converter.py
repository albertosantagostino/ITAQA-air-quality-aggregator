#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for geography-related conversions
"""

from ITAQA.geography.Italy import Province


def lookup_province_name(province_enum):
    """Given a Province enum, returns the province name"""
    if province_enum == Province.AL:
        return "Alessandria"
    elif province_enum == Province.AN:
        return "Ancona"
    elif province_enum == Province.AR:
        return "Arezzo"
    elif province_enum == Province.AP:
        return "Ascoli Piceno"
    elif province_enum == Province.AT:
        return "Asti"
    elif province_enum == Province.AV:
        return "Avellino"
    elif province_enum == Province.BT:
        return "Barletta-Andria-Trani"
    elif province_enum == Province.BL:
        return "Belluno"
    elif province_enum == Province.BN:
        return "Benevento"
    elif province_enum == Province.BG:
        return "Bergamo"
    elif province_enum == Province.BI:
        return "Biella"
    elif province_enum == Province.BS:
        return "Brescia"
    elif province_enum == Province.BR:
        return "Brindisi"
    elif province_enum == Province.CB:
        return "Campobasso"
    elif province_enum == Province.CE:
        return "Caserta"
    elif province_enum == Province.CZ:
        return "Catanzaro"
    elif province_enum == Province.CH:
        return "Chieti"
    elif province_enum == Province.CO:
        return "Como"
    elif province_enum == Province.CS:
        return "Cosenza"
    elif province_enum == Province.CR:
        return "Cremona"
    elif province_enum == Province.KR:
        return "Crotone"
    elif province_enum == Province.CN:
        return "Cuneo"
    elif province_enum == Province.FM:
        return "Fermo"
    elif province_enum == Province.FE:
        return "Ferrara"
    elif province_enum == Province.FG:
        return "Foggia"
    elif province_enum == Province.FC:
        return "Forlì-Cesena"
    elif province_enum == Province.FR:
        return "Frosinone"
    elif province_enum == Province.GR:
        return "Grosseto"
    elif province_enum == Province.IM:
        return "Imperia"
    elif province_enum == Province.IS:
        return "Isernia"
    elif province_enum == Province.SP:
        return "La Spezia"
    elif province_enum == Province.AQ:
        return "L'Aquila"
    elif province_enum == Province.LT:
        return "Latina"
    elif province_enum == Province.LE:
        return "Lecce"
    elif province_enum == Province.LC:
        return "Lecco"
    elif province_enum == Province.LI:
        return "Livorno"
    elif province_enum == Province.LO:
        return "Lodi"
    elif province_enum == Province.LU:
        return "Lucca"
    elif province_enum == Province.MC:
        return "Macerata"
    elif province_enum == Province.MN:
        return "Mantova"
    elif province_enum == Province.MS:
        return "Massa-Carrara"
    elif province_enum == Province.MT:
        return "Matera"
    elif province_enum == Province.MO:
        return "Modena"
    elif province_enum == Province.MB:
        return "Monza e Brianza"
    elif province_enum == Province.NO:
        return "Novara"
    elif province_enum == Province.NU:
        return "Nuoro"
    elif province_enum == Province.OR:
        return "Oristano"
    elif province_enum == Province.PD:
        return "Padova"
    elif province_enum == Province.PR:
        return "Parma"
    elif province_enum == Province.PV:
        return "Pavia"
    elif province_enum == Province.PG:
        return "Perugia"
    elif province_enum == Province.PU:
        return "Pesaro e Urbino"
    elif province_enum == Province.PE:
        return "Pescara"
    elif province_enum == Province.PC:
        return "Piacenza"
    elif province_enum == Province.PI:
        return "Pisa"
    elif province_enum == Province.PT:
        return "Pistoia"
    elif province_enum == Province.PZ:
        return "Potenza"
    elif province_enum == Province.PO:
        return "Prato"
    elif province_enum == Province.RA:
        return "Ravenna"
    elif province_enum == Province.RE:
        return "Reggio Emilia"
    elif province_enum == Province.RI:
        return "Rieti"
    elif province_enum == Province.RN:
        return "Rimini"
    elif province_enum == Province.RO:
        return "Rovigo"
    elif province_enum == Province.SA:
        return "Salerno"
    elif province_enum == Province.SS:
        return "Sassari"
    elif province_enum == Province.SV:
        return "Savona"
    elif province_enum == Province.SI:
        return "Siena"
    elif province_enum == Province.SO:
        return "Sondrio"
    elif province_enum == Province.SD:
        return "Sud Sardegna"
    elif province_enum == Province.TA:
        return "Taranto"
    elif province_enum == Province.TE:
        return "Teramo"
    elif province_enum == Province.TR:
        return "Terni"
    elif province_enum == Province.TV:
        return "Treviso"
    elif province_enum == Province.VA:
        return "Varese"
    elif province_enum == Province.VB:
        return "Verbano-Cusio-Ossola"
    elif province_enum == Province.VC:
        return "Vercelli"
    elif province_enum == Province.VR:
        return "Verona"
    elif province_enum == Province.VV:
        return "Vibo Valentia"
    elif province_enum == Province.VI:
        return "Vicenza"
    elif province_enum == Province.VT:
        return "Viterbo"
    elif province_enum == Province.BZ:
        return "Bolzano"
    elif province_enum == Province.TN:
        return "Trento"
    elif province_enum == Province.AG:
        return "Agrigento"
    elif province_enum == Province.CL:
        return "Caltanissetta"
    elif province_enum == Province.EN:
        return "Enna"
    elif province_enum == Province.RG:
        return "Ragusa"
    elif province_enum == Province.SR:
        return "Siracusa"
    elif province_enum == Province.TP:
        return "Trapani"
    elif province_enum == Province.BA:
        return "Bari"
    elif province_enum == Province.BO:
        return "Bologna"
    elif province_enum == Province.CA:
        return "Cagliari"
    elif province_enum == Province.CT:
        return "Catania"
    elif province_enum == Province.FI:
        return "Firenze"
    elif province_enum == Province.GE:
        return "Genova"
    elif province_enum == Province.ME:
        return "Messina"
    elif province_enum == Province.MI:
        return "Milano"
    elif province_enum == Province.NA:
        return "Napoli"
    elif province_enum == Province.PA:
        return "Palermo"
    elif province_enum == Province.RC:
        return "Reggio Calabria"
    elif province_enum == Province.RM:
        return "Roma"
    elif province_enum == Province.TO:
        return "Torino"
    elif province_enum == Province.VE:
        return "Venezia"
    elif province_enum == Province.UNSET:
        return None


def lookup_province_enum(province_name):
    """Given a province name, return the correspondent Province enum"""

    province_name = province_name.upper()

    if province_name == "ALESSANDRIA":
        return Province.AL
    elif province_name == "ANCONA":
        return Province.AN
    elif province_name == "AREZZO":
        return Province.AR
    elif province_name == "ASCOLI PICENO":
        return Province.AP
    elif province_name == "ASTI":
        return Province.AT
    elif province_name == "AVELLINO":
        return Province.AV
    elif province_name == "BARLETTA-ANDRIA-TRANI":
        return Province.BT
    elif province_name == "BELLUNO":
        return Province.BL
    elif province_name == "BENEVENTO":
        return Province.BN
    elif province_name == "BERGAMO":
        return Province.BG
    elif province_name == "BIELLA":
        return Province.BI
    elif province_name == "BRESCIA":
        return Province.BS
    elif province_name == "BRINDISI":
        return Province.BR
    elif province_name == "CAMPOBASSO":
        return Province.CB
    elif province_name == "CASERTA":
        return Province.CE
    elif province_name == "CATANZARO":
        return Province.CZ
    elif province_name == "CHIETI":
        return Province.CH
    elif province_name == "COMO":
        return Province.CO
    elif province_name == "COSENZA":
        return Province.CS
    elif province_name == "CREMONA":
        return Province.CR
    elif province_name == "CROTONE":
        return Province.KR
    elif province_name == "CUNEO":
        return Province.CN
    elif province_name == "FERMO":
        return Province.FM
    elif province_name == "FERRARA":
        return Province.FE
    elif province_name == "FOGGIA":
        return Province.FG
    elif province_name == "FORLÌ-CESENA":
        return Province.FC
    elif province_name == "FROSINONE":
        return Province.FR
    elif province_name == "GROSSETO":
        return Province.GR
    elif province_name == "IMPERIA":
        return Province.IM
    elif province_name == "ISERNIA":
        return Province.IS
    elif province_name == "LA SPEZIA":
        return Province.SP
    elif province_name == "L'AQUILA":
        return Province.AQ
    elif province_name == "LATINA":
        return Province.LT
    elif province_name == "LECCE":
        return Province.LE
    elif province_name == "LECCO":
        return Province.LC
    elif province_name == "LIVORNO":
        return Province.LI
    elif province_name == "LODI":
        return Province.LO
    elif province_name == "LUCCA":
        return Province.LU
    elif province_name == "MACERATA":
        return Province.MC
    elif province_name == "MANTOVA":
        return Province.MN
    elif province_name == "MASSA-CARRARA":
        return Province.MS
    elif province_name == "MATERA":
        return Province.MT
    elif province_name == "MODENA":
        return Province.MO
    elif province_name == "MONZA E BRIANZA":
        return Province.MB
    elif province_name == "NOVARA":
        return Province.NO
    elif province_name == "NUORO":
        return Province.NU
    elif province_name == "ORISTANO":
        return Province.OR
    elif province_name == "PADOVA":
        return Province.PD
    elif province_name == "PARMA":
        return Province.PR
    elif province_name == "PAVIA":
        return Province.PV
    elif province_name == "PERUGIA":
        return Province.PG
    elif province_name == "PESARO E URBINO":
        return Province.PU
    elif province_name == "PESCARA":
        return Province.PE
    elif province_name == "PIACENZA":
        return Province.PC
    elif province_name == "PISA":
        return Province.PI
    elif province_name == "PISTOIA":
        return Province.PT
    elif province_name == "POTENZA":
        return Province.PZ
    elif province_name == "PRATO":
        return Province.PO
    elif province_name == "RAVENNA":
        return Province.RA
    elif province_name == "REGGIO EMILIA":
        return Province.RE
    elif province_name == "RIETI":
        return Province.RI
    elif province_name == "RIMINI":
        return Province.RN
    elif province_name == "ROVIGO":
        return Province.RO
    elif province_name == "SALERNO":
        return Province.SA
    elif province_name == "SASSARI":
        return Province.SS
    elif province_name == "SAVONA":
        return Province.SV
    elif province_name == "SIENA":
        return Province.SI
    elif province_name == "SONDRIO":
        return Province.SO
    elif province_name == "SUD SARDEGNA":
        return Province.SD
    elif province_name == "TARANTO":
        return Province.TA
    elif province_name == "TERAMO":
        return Province.TE
    elif province_name == "TERNI":
        return Province.TR
    elif province_name == "TREVISO":
        return Province.TV
    elif province_name == "VARESE":
        return Province.VA
    elif province_name == "VERBANO-CUSIO-OSSOLA":
        return Province.VB
    elif province_name == "VERCELLI":
        return Province.VC
    elif province_name == "VERONA":
        return Province.VR
    elif province_name == "VIBO VALENTIA":
        return Province.VV
    elif province_name == "VICENZA":
        return Province.VI
    elif province_name == "VITERBO":
        return Province.VT
    elif province_name == "BOLZAN":
        return Province.BZ
    elif province_name == "TRENTO":
        return Province.TN
    elif province_name == "AGRIGENTO":
        return Province.AG
    elif province_name == "CALTANISSETTA":
        return Province.CL
    elif province_name == "ENNA":
        return Province.EN
    elif province_name == "RAGUSA":
        return Province.RG
    elif province_name == "SIRACUSA":
        return Province.SR
    elif province_name == "TRAPANI":
        return Province.TP
    elif province_name == "BARI":
        return Province.BA
    elif province_name == "BOLOGNA":
        return Province.BO
    elif province_name == "CAGLIARI":
        return Province.CA
    elif province_name == "CATANIA":
        return Province.CT
    elif province_name == "FIRENZE":
        return Province.FI
    elif province_name == "GENOVA":
        return Province.GE
    elif province_name == "MESSINA":
        return Province.ME
    elif province_name == "MILANO":
        return Province.MI
    elif province_name == "NAPOLI":
        return Province.NA
    elif province_name == "PALERMO":
        return Province.PA
    elif province_name == "REGGIO CALABRIA":
        return Province.RC
    elif province_name == "ROMA":
        return Province.RM
    elif province_name == "TORINO":
        return Province.TO
    elif province_name == "VENEZIA":
        return Province.VE
    else:
        return None
