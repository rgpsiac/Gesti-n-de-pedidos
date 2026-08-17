from typing import List
from abc import ABC, abstractmethod
from Back.models.dtos_tipoa import ClienteRequest, OrdenRequest, DetalleOrdenRequest
from Back.models.dtos_tipob import DTOBSheets

class BaseServiceSheetsLimpieza(ABC):
    def __init__(self, data: DTOBSheets):
        self.data = data

    def crear_cliente(self) -> ClienteRequest:
        nombre_cliente = self.data.nombre.strip().title()
        return ClienteRequest(nombre=nombre_cliente)

    def crear_orden(self) -> OrdenRequest:
        return OrdenRequest(
            id_cliente=0,
            tipo_pedido=self.data.tipo_pedido,
            fecha_pedido=self.data.fecha_registro,
            fecha_entrega=self.data.fecha_entrega,
            estatus="Pendiente"
        )

    @abstractmethod
    def crear_orden_detalles(self) -> List[DetalleOrdenRequest]:
        pass

class ServiceLimpiezaSheetsKits(BaseServiceSheetsLimpieza):
    def crear_orden_detalles(self):
        detalles = []
        if self.data.color_mandil_kit:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Kit",
                producto="Mandil",
                detalle=self.data.color_mandil_kit,
                cantidad=1,
                id_orden=0, #Temporal
                id_producto=0, #Temporal
                extra="No"
            ))
        if self.data.talla_guantes_kit:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Kit",
                producto="Guantes de plástico",
                detalle=self.data.talla_guantes_kit,
                cantidad=1,
                id_orden=0,
                id_producto=0,
                extra="No"
            ))
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Kit",
                producto="Guantes de nitrilo",
                detalle=self.data.talla_guantes_kit,
                cantidad=1,
                id_orden=0,
                id_producto=0,
                extra="No"
            ))
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Kit",
                producto="Cuchillo",
                detalle="Cuchillo",
                cantidad=1,
                id_orden=0,
                id_producto=0,
                extra="No"
            ))
        dtos_dict = self.data.model_dump()
        for llave, valor in dtos_dict.items():
            if valor:
                if isinstance(valor, int):
                    if llave.startswith("colm_pz_"):
                        producto = "Mandil"
                        detalle = llave.replace("colm_pz_",'').replace("_", ' ').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=valor,
                            id_orden=0,
                            id_producto=0,
                            extra="Sí"
                        ))
                    elif llave.startswith("pz_talla_guantesp_"):
                        producto = "Guantes de plástico"
                        detalle = llave.replace("pz_talla_guantesp_",'').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=valor,
                            id_orden=0,
                            id_producto=0,
                            extra="Sí"
                        ))
                    elif llave.startswith("pz_talla_guantesn_"):
                        producto = "Guantes de nitrilo"
                        detalle = llave.replace("pz_talla_guantesn_",'').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=valor,
                            id_orden=0,
                            id_producto=0,
                            extra="Sí"
                        ))
                    elif llave == "pz_cuchillos":
                        producto = "Cuchillo"
                        detalle = "Cuchillo"
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=valor,
                            id_orden=0,
                            id_producto=0,
                            extra="Sí"
                        ))
                elif isinstance(valor, str):
                    if llave.startswith("colm_pz_"):
                        cantidad = len(valor.split(','))
                        producto = "Mandil"
                        detalle = llave.replace("colm_pz_",'').replace("_",' ').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=cantidad,
                            extra="Sí",
                            id_orden=0,
                            id_producto=0
                        ))
                    elif llave.startswith("pz_talla_guantesp_"):
                        producto = "Guantes de plástico"
                        detalle = llave.replace("pz_talla_guantesp_",'').title()
                        cantidad = len(valor.split(","))
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=cantidad,
                            extra="Sí",
                            id_orden=0,
                            id_producto=0
                        ))
                    elif llave.startswith("pz_talla_guantesn_"):
                        producto = "Guantes de nitrilo"
                        detalle = llave.replace("pz_talla_guantesn_",'').title()
                        cantidad = len(valor.split(","))
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Kit",
                            producto=producto,
                            detalle=detalle,
                            cantidad=cantidad,
                            extra="Sí",
                            id_orden=0,
                            id_producto=0
                        ))
        if self.data.extra_bolsa_tote and "Sí" in self.data.extra_bolsa_tote:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Kit",
                producto="Bolsa",
                detalle="Tote",
                cantidad=1,
                id_orden=0,
                id_producto=0,
                extra="No"
            ))
        else:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Kit",
                producto="Bolsa",
                detalle="Reciclable",
                cantidad=1,
                id_orden=0,
                id_producto=0,
                extra="No"
            ))
        return detalles

class ServiceLimpiezaSheetsCombos(BaseServiceSheetsLimpieza):
    def crear_orden_detalles(self):
        dtos_dict = self.data.model_dump()
        detalles = []
        for llave, valor in dtos_dict.items():
            if valor:
                if isinstance(valor, str):
                    if llave.startswith("colm_combo_"):
                        producto = "Mandil"
                        detalle = llave.replace("colm_combo_",'').replace("_",' ').title()
                        kits = valor.split(",")
                        for kit in kits:
                            k = kit.strip()
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto=producto,
                                detalle=detalle,
                                cantidad=1,
                                extra="No",
                                pertenencia=k,
                                id_orden=0,
                                id_producto=0
                            ))
                    if llave.startswith("combo_talla_guantesp_"):
                        producto = "Guantes de plástico"
                        detalle = llave.replace("combo_talla_guantesp_",'').title()
                        kits = valor.split(",")
                        for kit in kits:
                            k = kit.strip()
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto=producto,
                                detalle=detalle,
                                cantidad=1,
                                extra="No",
                                pertenencia=k,
                                id_orden=0,
                                id_producto=0
                            ))
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto="Guantes de nitrilo",
                                detalle=detalle,
                                cantidad=1,
                                extra="No",
                                pertenencia=k,
                                id_orden=0,
                                id_producto=0
                            ))
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto="Cuchillo",
                                detalle="Cuchillo",
                                cantidad=1,
                                extra="No",
                                pertenencia=k,
                                id_orden=0,
                                id_producto=0
                            ))
                    if self.data.pregunta_pz_extra != None:
                        if llave.startswith("colm_pz_"):
                            producto = "Mandil"
                            detalle = llave.replace("colm_pz_","").replace("_", ' ').title()
                            piezas = valor.split(",")
                            for pieza in piezas:
                                p = pieza.strip()
                                detalles.append(DetalleOrdenRequest(
                                    tipo_pedido="Combo",
                                    producto=producto,
                                    detalle=detalle,
                                    cantidad=1,
                                    extra="Sí",
                                    pertenencia=f"Extra {p}",
                                    id_orden=0,
                                    id_producto=0
                                ))
                        if llave.startswith("pz_talla_guantesp_"):
                            producto = "Guantes de plástico"
                            detalle = llave.replace("pz_talla_guantesp_",'').title()
                            piezas = valor.split(",")
                            for pieza in piezas:
                                p = pieza.strip()
                                detalles.append(DetalleOrdenRequest(
                                    tipo_pedido="Combo",
                                    producto=producto,
                                    detalle=detalle,
                                    cantidad=1,
                                    extra="Sí",
                                    pertenencia=f"Extra {p}",
                                    id_orden=0,
                                    id_producto=0
                                ))
                        if llave.startswith("pz_talla_guantesn_"):
                            producto = "Guantes de nitrilo"
                            detalle = llave.replace("pz_talla_guantesn_",'').title()
                            piezas = valor.split(",")
                            for pieza in piezas:
                                p = pieza.strip()
                                detalles.append(DetalleOrdenRequest(
                                    tipo_pedido="Combo",
                                    producto=producto,
                                    detalle=detalle,
                                    cantidad=1,
                                    extra="Sí",
                                    pertenencia=f"Extra {p}",
                                    id_orden=0,
                                    id_producto=0
                                ))
                if isinstance(valor, int):
                    if self.data.pregunta_pz_extra != None:
                        if llave.startswith("colm_pz_"):
                            producto = "Mandil"
                            detalle = llave.replace("colm_pz_","").replace("_", ' ').title()
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto=producto,
                                detalle=detalle,
                                cantidad=valor,
                                extra="Sí",
                                pertenencia="Extra",
                                id_orden=0,
                                id_producto=0
                            ))
                        if llave.startswith("pz_talla_guantesp_"):
                            producto = "Guantes de plástico"
                            detalle = llave.replace("pz_talla_guantesp_",'').title()
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto=producto,
                                detalle=detalle,
                                cantidad=valor,
                                extra="Sí",
                                pertenencia="Extra",
                                id_orden=0,
                                id_producto=0
                            ))
                        if llave.startswith("pz_talla_guantesn_"):
                            producto = "Guantes de nitrilo"
                            detalle = llave.replace("pz_talla_guantesn_",'').title()
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto=producto,
                                detalle=detalle,
                                cantidad=valor,
                                extra="Sí",
                                pertenencia="Extra",
                                id_orden=0,
                                id_producto=0
                            ))
                        if llave.startswith("pz_cuchillos"):
                            detalles.append(DetalleOrdenRequest(
                                tipo_pedido="Combo",
                                producto="Cuchillo",
                                detalle="Cuchilo",
                                cantidad=valor,
                                pertenencia="Extra",
                                id_orden=0,
                                id_producto=0
                            ))
        if self.data.pregunta_kit_extra and "Sí" in self.data.pregunta_kit_extra:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Combo",
                producto="Mandil",
                detalle=self.data.col_kit_extra,
                cantidad=1,
                extra="Sí",
                pertenencia=f"Kit {self.data.numero_kits+1}",
                id_orden=0,
                id_producto=0
            ))
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Combo",
                producto="Guantes de plástico",
                detalle=self.data.talla_guantes_kit_extra,
                cantidad=1,
                extra="Sí",
                pertenencia=f"Kit {self.data.numero_kits+1}",
                id_orden=0,
                id_producto=0
            ))
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Combo",
                producto="Guantes de nitrilo",
                detalle=self.data.talla_guantes_kit_extra,
                cantidad=1,
                extra="Sí",
                pertenencia=f"Kit {self.data.numero_kits+1}",
                id_orden=0,
                id_producto=0
            ))
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Combo",
                producto="Cuchillo",
                detalle="Cuchillo",
                cantidad=1,
                extra="Sí",
                pertenencia=f"Kit {self.data.numero_kits+1}",
                id_orden=0,
                id_producto=0
            ))
        if self.data.extra_bolsa_tote and "Sí" in self.data.extra_bolsa_tote:
            if "una Tote en total" in self.data.extra_bolsa_tote:
                detalles.append(DetalleOrdenRequest(
                    tipo_pedido="Combo",
                    producto="Bolsa",
                    detalle="Tote",
                    cantidad=1,
                    extra="No",
                    pertenencia="Kit 1",
                    id_orden=0,
                    id_producto=0
                ))
            elif "una Tote para cada" in self.data.extra_bolsa_tote:
                cantidad_kits = self.data.numero_kits
                cantidad_kits_extra = 1 if self.data.pregunta_kit_extra and "Sí" in self.data.pregunta_kit_extra else 0
                for i in range(1, cantidad_kits+cantidad_kits_extra+1):
                    detalles.append(DetalleOrdenRequest(
                        tipo_pedido="Combo",
                        producto="Bolsa",
                        detalle="Tote",
                        cantidad=1,
                        extra="No",
                        pertenencia=f"Kit {i}",
                        id_orden=0,
                        id_producto=0
                    ))
        else:
            cantidad_kits = self.data.numero_kits
            cantidad_kits_extra = 1 if self.data.pregunta_kit_extra and "Sí" in self.data.pregunta_kit_extra else 0
            for i in range(1, cantidad_kits+cantidad_kits_extra+1):
                detalles.append(DetalleOrdenRequest(
                    tipo_pedido="Combo",
                    producto="Bolsa",
                    detalle="Reciclable",
                    cantidad=1,
                    extra="No",
                    pertenencia=f"Kit {i}",
                    id_orden=0,
                    id_producto=0
                ))
        return detalles

class ServiceLimpiezaSheetsPiezas(BaseServiceSheetsLimpieza):
    def crear_orden_detalles(self):
        pidio_mandil =  False
        detalles = []
        dtos_dict = self.data.model_dump()
        for llave, valor in dtos_dict.items():
            if valor:
                if isinstance(valor, str):
                    if llave.startswith("colm_pz_"):
                        pidio_mandil = True
                        producto = "Mandil"
                        detalle = llave.replace("colm_pz_",'').replace("_",' ').title()
                        piezas = len(valor.split(","))
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto=producto,
                            detalle=detalle,
                            cantidad=piezas,
                            pertenencia="Individual",
                            extra="No",
                            id_orden=0,
                            id_producto=0
                            ))
                    if llave.startswith("pz_talla_guantesp_"):
                        producto = "Guantes de plástico"
                        detalle = llave.replace("pz_talla_guantesp_",'').title()
                        piezas = len(valor.split(","))
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto=producto,
                            detalle=detalle,
                            cantidad=piezas,
                            extra="No",
                            pertenencia="Individual",
                            id_orden=0,
                            id_producto=0
                        ))
                    if llave.startswith("pz_talla_guantesn_"):
                        producto = "Guantes de nitrilo"
                        detalle = llave.replace("pz_talla_guantesn_",'').title()
                        piezas = len(valor.split(","))
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto=producto,
                            detalle=detalle,
                            cantidad=piezas,
                            extra="No",
                            pertenencia="Individual",
                            id_orden=0,
                            id_producto=0
                        ))
                if isinstance(valor, int):
                    if llave.startswith("colm_pz_"):
                        pidio_mandil = True
                        detalle = llave.replace("colm_pz_",'').replace("_",' ').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto="Mandil",
                            detalle=detalle,
                            cantidad=valor,
                            extra="No",
                            pertenencia="Individual",
                            id_orden=0,
                            id_producto=0
                        ))
                    if llave.startswith("pz_talla_guantesp_"):
                        detalle = llave.replace("pz_talla_guantesp_",'').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto="Guantes de plástico",
                            detalle=detalle,
                            cantidad=valor,
                            extra="No",
                            pertenencia="Individual",
                            id_orden=0,
                            id_producto=0
                        ))
                    if llave.startswith("pz_talla_guantesn_"):
                        detalle = llave.replace("pz_talla_guantesn_",'').title()
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto="Guantes de nitrilo",
                            detalle=detalle,
                            cantidad=valor,
                            extra="No",
                            pertenencia="Individual",
                            id_orden=0,
                            id_producto=0
                        ))
                    if llave.startswith("pz_cuchillos"):
                        detalles.append(DetalleOrdenRequest(
                            tipo_pedido="Piezas Individuales",
                            producto="Cuchillo",
                            detalle="Cuchillo",
                            cantidad=valor,
                            extra="No",
                            pertenencia="Individual",
                            id_orden=0,
                            id_producto=0
                        ))
        if self.data.extra_bolsa_tote and "Sí" in self.data.extra_bolsa_tote:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Piezas Individuales",
                producto="Bolsa",
                detalle="Tote",
                cantidad=1,
                extra="No",
                pertenencia="Individual",
                id_orden=0,
                id_producto=0
            ))
        elif pidio_mandil:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Piezas Individuales",
                producto="Bolsa",
                detalle="Reciclable",
                cantidad=1,
                extra="No",
                pertenencia="Individual",
                id_orden=0,
                id_producto=0
            ))
        return detalles

class ServiceLimpiezaSheetsEspecial(BaseServiceSheetsLimpieza):
    def crear_orden_detalles(self):
        detalles = []
        if self.data.especial_bolsa_tote != None:
            detalles.append(DetalleOrdenRequest(
                tipo_pedido="Piezas Individuales",
                producto="Bolsa",
                detalle="Tote",
                cantidad=self.data.especial_bolsa_tote,
                extra="No",
                pertenencia="Individual",
                id_orden=0,
                id_producto=0
            ))
        return detalles

class FactoryLimpiezaSheets:
    @staticmethod
    def llamar_servicio(data: DTOBSheets) -> BaseServiceSheetsLimpieza:
        if data.tipo_pedido == "Kit":
            return ServiceLimpiezaSheetsKits(data=data)
        elif data.tipo_pedido == "Combo":
            return ServiceLimpiezaSheetsCombos(data=data)
        elif data.tipo_pedido == "Piezas individuales":
            return ServiceLimpiezaSheetsPiezas(data=data)
        elif data.tipo_pedido == "Tote bag":
            return ServiceLimpiezaSheetsEspecial(data=data)
        else:
            raise ValueError(f"Tipo de dato desconocido: {data.tipo_pedido}")