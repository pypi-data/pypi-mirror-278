from datetime import datetime
from bson import ObjectId
from typing import Annotated, Optional
from arbitro_typing.data_types import Bank, Product, ReceivePay, Tenors
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Operation(BaseModel):
    """Clase básica para las operaciones del arbitro bancario.
    Atributos:

        deal_number: ``str``. Nombre de la operación. Campo opcional. Valor por defecto = None
        product: ``Product``. Tipo de producto de la operación.
        receive_pay: ``ReceivePay``. Tipo de pata de la operación. 
        counterparty: ``Bank``. Contraparte bancaria de la operación.
        amount: ``int``. Nominal de la operación, su moneda se infiere del tipo de operación.
        maturity: ``Tenors``. Plazo para el vencimiento de la operación.
        rate: ``float``. Tasa de interés de la operación.
        client: ``Bank``. Banco al que le pertenece esta pata de la operación.
        exchange_rate: ``float``. Tasa de cambio de la operación. Es necesario para los CCS y BASIS. Campo opcional. Valor por defecto = None
    """
    deal_number: Optional[str] = Field(default=None)
    product: Product
    receive_pay: ReceivePay
    counterparty: Bank
    amount: int
    maturity: Tenors
    rate: float
    client: Bank
    exchange_rate: Optional[float] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
    )

class OperationDaily(Operation):
    """Clase para las operaciones de la colección Daily. Hereda desde Operation.
    Atributos:

        id: ``PyObjectId``. Identificador de MongoDB. Campo opcional. Valor por defecto = None
        client_confirmed_status: ``bool``. Campo de confirmación de que los datos de esta pata de la operación son correctos. Campo opcional. Valor por defecto = False
        confirmed_status: ``bool``. Campo de confirmación de que ambas patas de la operación están correctas, dado de alta de forma automática por el sistema. Campo opcional. Valor por defecto = False
        operation_pair: ``PyObjectId``. Identificador del par de la operación, perteneciente a su contraparte. Campo opcional. Valor por defecto = None
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    client_confirmed_status: Optional[bool] = Field(default=False)
    confirmed_status: Optional[bool] = Field(default=False)
    operation_pair: Optional[PyObjectId] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
    )

class UpdateOperation(BaseModel):
    """Clase para la actualización de operaciones del arbitro bancario. Se utiliza en los métodos PUT de la API REST.
    Atributos:

        deal_number: ``str``. Nombre de la operación. Campo opcional. Valor por defecto = None
        product: ``Product``. Tipo de producto de la operación. Campo opcional. Valor por defecto = None
        receive_pay: ``ReceivePay``. Tipo de pata de la operación.  Campo opcional. Valor por defecto = None
        counterparty: ``Bank``. Contraparte bancaria de la operación. Campo opcional. Valor por defecto = None
        amount: ``int``. Nominal de la operación, su moneda se infiere del tipo de operación. Campo opcional. Valor por defecto = None
        maturity: ``Tenors``. Plazo para el vencimiento de la operación. Campo opcional. Valor por defecto = None
        rate: ``float``. Tasa de interés de la operación. Campo opcional. Valor por defecto = None
        client: ``Bank``. Banco al que le pertenece esta pata de la operación. Campo opcional. Valor por defecto = None
        exchange_rate: ``float``. Tasa de cambio de la operación. Es necesario para los CCS y BASIS. Campo opcional. Valor por defecto = None
        client_confirmed_status: ``bool``. Campo de confirmación de que los datos de esta pata de la operación son correctos. Campo opcional. Valor por defecto = False
        confirmed_status: ``bool``. Campo de confirmación de que ambas patas de la operación están correctas, dado de alta de forma automática por el sistema. Campo opcional. Valor por defecto = False
        operation_pair: ``PyObjectId``. Identificador del par de la operación, perteneciente a su contraparte. Campo opcional. Valor por defecto = None
    """
    deal_number: Optional[str] = None
    client: Optional[Bank] = None
    product: Optional[Product] = None
    receive_pay: Optional[ReceivePay] = None
    counterparty: Optional[Bank] = None
    amount: Optional[int] = None
    maturity: Optional[Tenors] = None
    rate: Optional[float] = None
    exchange_rate: Optional[float] = None
    client_confirmed_status: Optional[bool] = None
    confirmed_status: Optional[bool] = None
    operation_pair: Optional[PyObjectId] = None
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
    )

class OperationHistorical(BaseModel):
    """Clase para las operaciones de la colección histórica de cada cliente. Se caracteriza por guardar la información de ambas patas de la operación.
    Atributos:

        id: ``PyObjectId``. Identificador de MongoDB. Campo opcional. Valor por defecto = None
        trade_date: ``datetime``. Fecha de trading, concretamente la fecha en que se inserto la operación en el sistema.
        current: ``bool``. Indica si la operación se encuentra o no vigente, según las propiedades de sus patas.
        pay_leg: ``Operation``. Contiene la información de la pata que paga (pasiva) de la operación.
        receive_leg: ``Operation``. Contiene la información de la pata que recibe (activa) de la operación.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    trade_date: datetime
    current: bool
    pay_leg: Operation
    receive_leg: Operation