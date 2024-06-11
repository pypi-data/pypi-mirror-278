from enum import StrEnum, auto, IntEnum

class ImplMissing(StrEnum):
    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None

class ReceivePay(ImplMissing):
    """
    Representa el tipo de pata de la operación, el cual puede ser Activo (Receive) o Pasivo (Pay).
    """

    RECEIVE = auto()
    PAY = auto()

class Product(ImplMissing):
    """
    Representa los tipos de productos que procesa el sistema.

    Los tipos soportados son: ``ICP``=Swap Cámara, ``CCS``=Cross Currency UF/CLP, ``BASIS``=Basis USD/CLP.
    """

    ICP = auto()
    CCS = auto()
    BASIS = auto()

class Bank(ImplMissing):
    """
    Listado de bancos locales validos para el sistema.
    """

    BICE = auto()
    ESTADO = auto()
    SECURITY = auto()
    SANTANDER = auto()
    FALABELLA = auto()
    INTERNACIONAL = auto()

class Tenors(IntEnum):
    """
    Listado de tenors estándar utilizados por la banca Chilena.

    Su convención de nombre indica la cantidad de meses (M) o años (Y) que su valor representa en días, en base 30/360.
    """
    M1 = 30
    M2 = 60
    M3 = 90
    M6 = 180
    M9 = 270
    Y1 = 360
    M18 = 540
    Y2 = 720
    Y3 = 1080
    Y4 = 1440
    Y5 = 1800
    Y6 = 2160
    Y7 = 2520
    Y8 = 2880
    Y9 = 3240
    Y10 = 3600
    Y12 = 4320
    Y15 = 5400
    Y20 = 7200
    Y25 = 9000
    Y30 = 10800