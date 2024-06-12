from enum import Enum
from . import libros
from . import pedido
from . import envio
from . import factul
from . import mensaj
from . import devolu

class DocumentType(Enum):
    ABONO = ("Albarán o Factura de Abono", None)
    CAMPRE = ("Cambios de precio", None)
    ESTADO = ("Cambios de estado", None)  # noqa: F405
    LIBROS = ("Ficha del Libro", {
        "08": libros.v8.LibrosDoc,
        "09": libros.v9.LibrosDoc,
        "??": libros.v9.LibrosDoc
    })  # noqa: F405
    PEDIDO = ("Albarán de pedido del cliente", {
        "07": pedido.v7.PedidoDoc,
        "??": pedido.v7.PedidoDoc
    })
    ENVIO = ("Albarán de envío de distribuidora", {
        "08": envio.v8.EnvioDoc,
        "??": envio.v8.EnvioDoc,
    })
    FACTUL = ("Factura", {
        "01": factul.v1.FacturaDoc,
        "??": factul.v1.FacturaDoc,
    })
    MENSAJ = ("Mensaje", {
        "01": mensaj.v1.MensajeDoc,
        "??": mensaj.v1.MensajeDoc,
    })
    DEVOLU = ("Devoluciones", {
        "02": devolu.v2.DevolucionDoc,
        "??": devolu.v2.DevolucionDoc,
    })