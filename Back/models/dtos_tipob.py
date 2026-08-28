from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date


class DTOBSheets(BaseModel):
    fecha_registro: str|None = Field(alias='Marca temporal')
    nombre: str|None = Field(alias='Escribe tu nombre (1 nombre y 1 apellido)')
    telefono: int|None = Field(alias='Ingresa tu número de celular (sin espacios)')
    tipo_pedido: str|None = Field(alias='¿Qué pedirás?')

    color_mandil_kit_plus: str|None = Field(alias='Color del mandil - Kit plus', default=None)
    talla_guantes_kit_plus: str|None = Field(alias='Tamaño de guantes (hule y nitrilo) - Kit plus', default=None)

    color_mandil_kit_basico: str|None = Field(alias='Color del mandil - Kit básico', default=None)
    talla_guantes_kit_basico: str|None = Field(alias='Tamaño de guantes (nitrilo) - Kit básico', default=None)
    ecobolsa_kit_basico: str|None = Field(alias='¿Deseas ecobolsa con tu pedido? - Kit básico', default=None)

    numero_kits_cowmpadres: int|None = Field(alias='Número de kits - cowmpadres', default=0)
    colm_combo_cowmpadres_amarillo_mango: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Amarillo mango]', default=0)
    colm_combo_cowmpadres_rojo: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Rojo]', default=0)
    colm_combo_cowmpadres_vino: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Vino]', default=0)
    colm_combo_cowmpadres_blanco: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Blanco]', default=0)
    colm_combo_cowmpadres_negro: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Negro]', default=0)
    colm_combo_cowmpadres_azul_pastel: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Azul pastel]', default=0)
    colm_combo_cowmpadres_azul_rey: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Azul rey]', default=0)
    colm_combo_cowmpadres_azul_marino: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Azul marino]', default=0)
    colm_combo_cowmpadres_morado: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Morado]', default=0)
    colm_combo_cowmpadres_lila: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Lila]',default=0)
    colm_combo_cowmpadres_turquesa: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Turquesa]', default=0)
    colm_combo_cowmpadres_rosa_pastel: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Rosa pastel]', default=0)
    colm_combo_cowmpadres_rosa_barbie: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Rosa barbie]', default=0)
    colm_combo_cowmpadres_verde_bandera: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Verde bandera]', default=0)
    colm_combo_cowmpadres_verde_militar: int|str|None = Field(alias='Color de mandiles - Cowmpadres [Verde militar]', default=0)
    combo_cowmpadres_talla_guantesp_chicos: int|str|None = Field(alias='Talla de guantes de plástico - Cowmpadres [Chicos]', default=0)
    combo_cowmpadres_talla_guantesp_medianos: int|str|None = Field(alias='Talla de guantes de plástico - Cowmpadres [Medianos]', default=0)
    combo_cowmpadres_talla_guantesp_grandes: int|str|None = Field(alias='Talla de guantes de plástico - Cowmpadres [Grandes]', default=0)
    pregunta_kit_plus_extra: str|None = Field(alias='¿Quieres agregar un kit plus extra?', default=None)
    col_kit_plus_extra: str|None = Field(alias='Color del mandil - Kextra plus', default=None)
    talla_guantes_kit_plus_extra: str|None = Field(alias='Tamaño de guantes (hule y nitrilo) - Kextra plus', default=None)

    numero_kits_amigoats: str|None|int = Field(alias='Número de kits - amigoats', default=None)
    colm_combo_amigoats_amarillo_mango: str|int|None = Field(alias='Color de mandiles - amigoats [Amarillo mango]', default=None)
    colm_combo_amigoats_rojo: int|str|None = Field(alias='Color de mandiles - amigoats [Rojo]', default=None)
    colm_combo_amigoats_vino: int|str|None = Field(alias='Color de mandiles - amigoats [Vino]', default=None)
    colm_combo_amigoats_blanco: int|str|None = Field(alias='Color de mandiles - amigoats [Blanco]', default=None)
    colm_combo_amigoats_negro: int|str|None = Field(alias='Color de mandiles - amigoats [Negro]', default=None)
    colm_combo_amigoats_azul_pastel: str|int|None = Field(alias='Color de mandiles - amigoats [Azul pastel]', default=None)
    colm_combo_amigoats_azul_rey: str|int|None = Field(alias='Color de mandiles - amigoats [Azul rey]', default=None)
    colm_combo_amigoats_azul_marino: str|int|None = Field(alias='Color de mandiles - amigoats [Azul marino]', default=None)
    colm_combo_amigoats_morado: str|int|None = Field(alias='Color de mandiles - amigoats [Morado]', default=None)
    colm_combo_amigoats_lila: str|int|None = Field(default=None, alias='Color de mandiles - amigoats [Lila]')
    colm_combo_amigoats_turquesa: int|str|None = Field(alias='Color de mandiles - amigoats [Turquesa]', default=None)
    colm_combo_amigoats_rosa_pastel: int|str|None = Field(alias='Color de mandiles - amigoats [Rosa pastel]', default=None)
    colm_combo_amigoats_rosa_barbie: str|int|None = Field(alias='Color de mandiles - amigoats [Rosa barbie]', default=None)
    colm_combo_amigoats_verde_bandera: str|int|None = Field(alias='Color de mandiles - amigoats [Verde bandera]', default=None)
    colm_combo_amigoats_verde_militar: int|str|None = Field(alias='Color de mandiles - amigoats [Verde militar]', default=None)
    combo_amigoats_talla_guantesn_chicos: int|str|None = Field(alias='Talla de guantes de nitrilo - amigoats [Chicos]', default=None)
    combo_amigoats_talla_guantesn_medianos: int|str|None = Field(alias='Talla de guantes de nitrilo - amigoats [Medianos]', default=None)
    combo_amigoats_talla_guantesn_grandes: int|str|None = Field(alias='Talla de guantes de nitrilo - amigoats [Grandes]', default=None)
    pregunta_kit_basico_extra: int|str|None = Field(alias='¿Quieres agregar un kit básico extra?', default=None)
    pregunta_ecobolsas_combos_amigoats: str|int|None = Field(alias='¿Deseas ecobolsas para tus Kits básicos?', default=None)
    col_kit_basico_extra: str|int|None = Field(alias='Color del mandil - Kextra básico', default=None)
    talla_guantes_kit_basico_extra: str|int|None = Field(alias='Tamaño de guantes (nitrilo) - Kextra básico', default=None)


    pregunta_pz_extra: str|None = Field(alias='¿Quieres agregar piezas sueltas (extras)?', default=None)

    colm_pz_amarillo_mango: int|str|None = Field(alias='Mandil (color) - Pieza [Amarillo mango]', default=0)
    colm_pz_rojo: int|str|None = Field(alias='Mandil (color) - Pieza [Rojo]', default=0)
    colm_pz_vino: int|str|None = Field(alias='Mandil (color) - Pieza [Vino]', default=0)
    colm_pz_blanco: int|str|None = Field(alias='Mandil (color) - Pieza [Blanco]', default=0)
    colm_pz_negro: int|str|None = Field(alias='Mandil (color) - Pieza [Negro]', default=0)
    colm_pz_azul_pastel: int|str|None = Field(alias='Mandil (color) - Pieza [Azul pastel]', default=0)
    colm_pz_azul_rey: int|str|None = Field(alias='Mandil (color) - Pieza [Azul rey]', default=0)
    colm_pz_azul_marino: int|str|None = Field(alias='Mandil (color) - Pieza [Azul marino]', default=0)
    colm_pz_morado: int|str|None = Field(alias='Mandil (color) - Pieza [Morado]', default=0)
    colm_pz_lila: int|str|None = Field(alias='Mandil (color) - Pieza [Lila]', default=0)
    colm_pz_turquesa: int|str|None = Field(alias='Mandil (color) - Pieza [Turquesa]', default=0)
    colm_pz_rosa_pastel: int|str|None = Field(alias='Mandil (color) - Pieza [Rosa pastel]', default=0)
    colm_pz_rosa_barbie: int|str|None = Field(alias='Mandil (color) - Pieza [Rosa barbie]', default=0)
    colm_pz_verde_bandera: int|str|None = Field(alias='Mandil (color) - Pieza [Verde bandera]', default=0)
    colm_pz_verde_militar: int|str|None = Field(alias='Mandil (color) - Pieza [Verde militar]', default=0)
    pz_talla_guantesp_chicos: int|str|None = Field(alias='Guantes de plástico (talla) - Pieza [Chicos]', default=0)
    pz_talla_guantesp_medianos: int|str|None = Field(alias='Guantes de plástico (talla) - Pieza [Medianos]', default=0)
    pz_talla_guantesp_grandes: int|str|None = Field(alias='Guantes de plástico (talla) - Pieza [Grandes]', default=0)
    pz_talla_guantesn_chicos: int|str|None = Field(alias='Guantes de nitrilo (talla) - Pieza [Chicos]', default=0)
    pz_talla_guantesn_medianos: int|str|None = Field(alias='Guantes de nitrilo (talla) - Pieza [Medianos]', default=0)
    pz_talla_guantesn_grandes: int|str|None = Field(alias='Guantes de nitrilo (talla) - Pieza [Grandes]', default=0)
    pz_cuchillos: int|str|None = Field(alias='Cuchillos - Pieza', default=0)

    especial_bolsa_tote: int|None = Field(alias='Tote bag - Especial', default=0)

    extra_bolsa_tote: str|None = Field(alias='¿Quieres recibir tu pedido en una tote bag?', default=None)
    fecha_entrega: str|None = Field(alias='Fechas', default=None)

    @field_validator("numero_kits_cowmpadres","numero_kits_amigoats","especial_bolsa_tote", mode='before')
    @classmethod
    def validar_celdas(cls, valor_original):
        if isinstance(valor_original, str) and valor_original.strip() == "":
            return 0
        return valor_original

class DTOBInventarios(BaseModel):
    producto: str = Field(alias="Producto")
    detalle: str = Field(alias="Detalle")
    cantidad: int = Field(alias="Cantidad", default=0)
    costo_unitario: float = Field(alias="Costo Unitario", default=0.0)
    fecha_registro: date|str = Field(alias="Fecha de registro",default=None)