from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date

# ---- Pydantic Schemas: input del POST /ros ----

class EncabezadoIn(BaseModel):
    numero_reporte: str = Field(min_length=1, max_length=20)
    fecha_reporte: date
    clase_reporte: str = Field(pattern=r"^[ICA]$")
    numero_reporte_anterior: Optional[str] = Field(default=None, max_length=20)

    @field_validator("numero_reporte_anterior")
    @classmethod
    def blank_to_none(cls, v):
        return v or None


class InstitucionReportanteIn(BaseModel):
    nombre_entidad: str = Field(min_length=1, max_length=150)
    tipo_entidad: str = Field(min_length=1, max_length=100)
    codigo_entidad: str = Field(min_length=1, max_length=20)
    sucursal_presenta_operacion: Optional[str] = Field(default=None, max_length=150)
    codigo_sucursal: Optional[str] = Field(default=None, max_length=20)
    nombre_sucursal: Optional[str] = Field(default=None, max_length=100)

    @field_validator("sucursal_presenta_operacion", "codigo_sucursal", "nombre_sucursal")
    @classmethod
    def blank_to_none(cls, v):
        return v or None


class PersonaImplicadaIn(BaseModel):
    nombre_completo_o_razon_social: str = Field(min_length=1, max_length=150)
    numero_identificacion: str = Field(min_length=1, max_length=40)

    direccion_domicilio: Optional[str] = Field(default=None, max_length=150)
    departamento_domicilio: Optional[str] = Field(default=None, max_length=100)
    municipio_domicilio: Optional[str] = Field(default=None, max_length=100)
    telefonos_domicilio: Optional[str] = Field(default=None, max_length=20)

    camara_comercio: Optional[str] = Field(default=None, max_length=50)
    direccion_trabajo: Optional[str] = Field(default=None, max_length=150)
    departamento_trabajo: Optional[str] = Field(default=None, max_length=100)
    municipio_trabajo: Optional[str] = Field(default=None, max_length=100)
    telefonos_trabajo: Optional[str] = Field(default=None, max_length=20)

    correo_electronico: Optional[EmailStr] = None

    actividad_economica: Optional[str] = Field(default=None, max_length=150)
    ciiu: Optional[str] = Field(default=None, max_length=10)
    fecha_vinculacion: Optional[date] = None

    relacion_persona_entidad: Optional[str] = Field(default=None)  # cliente/empleado/accionista/otra/None
    relacion_persona_entidad_otra: Optional[str] = None

    vinculado_aun: Optional[bool] = None   # True/False/None
    causa_no_vinculacion: Optional[str] = Field(default=None)  # retiro_voluntario/decision_institucion/suspension
    fecha_no_vinculacion: Optional[date] = None

    promedio_ingresos_mensuales: Optional[float] = None
    fecha_promedio_ingresos: Optional[date] = None

    @field_validator(
        "direccion_domicilio", "departamento_domicilio", "municipio_domicilio", "telefonos_domicilio",
        "camara_comercio", "direccion_trabajo", "departamento_trabajo", "municipio_trabajo",
        "telefonos_trabajo", "actividad_economica", "ciiu", "relacion_persona_entidad",
        "relacion_persona_entidad_otra", "causa_no_vinculacion"
    )
    @classmethod
    def blank_to_none(cls, v):
        return v or None


class OperacionSospechosaIn(BaseModel):
    valor_total_operacion: Optional[float] = None
    tipo_operacion: Optional[str] = Field(default=None)  # nacional/internacional
    fecha_desde: Optional[date] = None
    fecha_hasta: Optional[date] = None


class ROSIn(BaseModel):
    encabezado: EncabezadoIn
    institucion_reportante: InstitucionReportanteIn
    persona_implicada: PersonaImplicadaIn
    operacion_sospechosa: OperacionSospechosaIn


# ---- Respuestas mínimas ----
class ROSCreated(BaseModel):
    id_reporte: int
    message: str = "created"
