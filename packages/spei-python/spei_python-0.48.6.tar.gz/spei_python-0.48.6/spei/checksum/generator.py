from datetime import datetime
from decimal import Decimal
from typing import Any, List

from spei.resources import Orden


class ChecksumGenerator(object):
    def format_data(self):
        raise NotImplementedError

    def split_amount(self, amount):
        amount_as_cents = int(Decimal(str(amount)) * 100)
        high = 0
        low = amount_as_cents
        tens_of_millons = amount_as_cents // 10**9
        if tens_of_millons:
            high = tens_of_millons
            low = amount_as_cents - (tens_of_millons * 10**9)
        return high, low

    def _fecha_to_bytearray(self, fecha_operacion: int) -> bytearray:
        fecha_operacion = datetime.strptime(str(fecha_operacion), '%Y%m%d')

        day = int.to_bytes(int(fecha_operacion.day), 1, 'big')
        month = int.to_bytes(int(fecha_operacion.month), 1, 'big')
        year = int.to_bytes(int(fecha_operacion.year), 2, 'big')
        return day + month + year

    def _clave_to_bytearray(self, clave: str) -> bytearray:
        if not clave:
            clave = ''
        return int.to_bytes(int(clave), 4, 'big')

    def _monto_to_bytearray(self, amount: int) -> bytearray:
        high, low = self.split_amount(amount)
        high = int.to_bytes(int(high), 4, 'big')
        low = int.to_bytes(int(low), 4, 'big')
        return high + low

    def _to_byte_array(
        self,
        value: str,  # noqa: WPS110
        add_zero_byte: bool = False,
    ) -> bytearray:
        encoded = value.encode('utf-8')
        bytes_ = bytearray(encoded)
        if add_zero_byte:
            bytes_.append(0)
        return bytes_

    def _list_to_bytes(self, message_data: List[Any]) -> bytes:
        res = bytearray()
        for field in message_data:
            for element in field:
                res.append(element)
        return bytes(res)


class ChecksumGeneratorRemittance(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ord, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_ben, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_participante_ord, add_zero_byte=True),  # noqa: E501
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorDefault(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorOrigin(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ord, add_zero_byte=True),
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorBeneficiary(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ben, add_zero_byte=True),
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorOriginAndBeneficiary(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ord, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_ben, add_zero_byte=True),
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorBeneficiaryAndAdditionalBeneficiary(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ben, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_ben_2, add_zero_byte=True),
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorIndirectToParticipant(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ord, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_participante_ord, add_zero_byte=True),  # noqa: E501
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorIndirect(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ord, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_ben, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_participante_ord, add_zero_byte=True),  # noqa: E501
        )
        return self._list_to_bytes(message_data)


class ChecksumGeneratorEveryField(ChecksumGenerator):
    def format_data(self, orden: Orden):
        message_data = (
            self._fecha_to_bytearray(orden.op_fecha_oper),
            self._clave_to_bytearray(orden.op_ins_clave_ord),
            self._clave_to_bytearray(orden.op_ins_clave_ben),
            self._to_byte_array(orden.op_cve_rastreo, add_zero_byte=True),
            self._monto_to_bytearray(orden.op_monto),
            self._to_byte_array(orden.op_cuenta_ord, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_ben, add_zero_byte=True),
            self._to_byte_array(orden.op_cuenta_ben_2, add_zero_byte=True),
        )
        return self._list_to_bytes(message_data)
