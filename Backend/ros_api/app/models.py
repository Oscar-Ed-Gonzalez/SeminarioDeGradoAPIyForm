from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, CheckConstraint, Numeric, CHAR, Boolean
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


class ReporteROS(Base):
    __tablename__ = "reporte_ros"

    id_reporte: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_reporte: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_reporte: Mapped[Date] = mapped_column(Date, nullable=False)
    clase_reporte: Mapped[str] = mapped_column(CHAR(1), nullable=False)  # I, C, A
    numero_reporte_anterior: Mapped[str | None] = mapped_column(String(20), nullable=True)

    institucion: Mapped["InstitucionReportante"] = relationship(
        back_populates="reporte", uselist=False, cascade="all, delete-orphan"
    )
    personas: Mapped[list["PersonaImplicada"]] = relationship(
        back_populates="reporte", cascade="all, delete-orphan"
    )
    operacion: Mapped["OperacionSospechosa"] = relationship(
        back_populates="reporte", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("clase_reporte in ('I','C','A')", name="ck_clase_reporte"),
    )


class InstitucionReportante(Base):
    __tablename__ = "institucion_reportante"

    id_institucion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_reporte: Mapped[int] = mapped_column(ForeignKey("reporte_ros.id_reporte"), nullable=False)

    nombre_entidad: Mapped[str] = mapped_column(String(150), nullable=False)
    tipo_entidad: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_entidad: Mapped[str] = mapped_column(String(20), nullable=False)
    sucursal_oficina: Mapped[str | None] = mapped_column(String(150))
    codigo_sucursal: Mapped[str | None] = mapped_column(String(20))
    nombre_sucursal: Mapped[str | None] = mapped_column(String(100))

    reporte: Mapped[ReporteROS] = relationship(back_populates="institucion")


class PersonaImplicada(Base):
    __tablename__ = "persona_implicada"

    id_persona: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_reporte: Mapped[int] = mapped_column(ForeignKey("reporte_ros.id_reporte"), nullable=False)

    nombre_completo: Mapped[str] = mapped_column(String(150), nullable=False)
    numero_identificacion: Mapped[str] = mapped_column(String(40), nullable=False)

    direccion_domicilio: Mapped[str | None] = mapped_column(String(150))
    departamento_domicilio: Mapped[str | None] = mapped_column(String(100))
    municipio_domicilio: Mapped[str | None] = mapped_column(String(100))
    telefono_domicilio: Mapped[str | None] = mapped_column(String(20))

    camara_comercio: Mapped[str | None] = mapped_column(String(50))
    direccion_trabajo: Mapped[str | None] = mapped_column(String(150))
    departamento_trabajo: Mapped[str | None] = mapped_column(String(100))
    municipio_trabajo: Mapped[str | None] = mapped_column(String(100))
    telefono_trabajo: Mapped[str | None] = mapped_column(String(20))

    correo_electronico: Mapped[str | None] = mapped_column(String(254))

    actividad_economica: Mapped[str | None] = mapped_column(String(150))
    ciiu: Mapped[str | None] = mapped_column(String(10))
    fecha_vinculacion: Mapped[Date | None] = mapped_column(Date)

    relacion_entidad: Mapped[str | None] = mapped_column(CHAR(1))  # C/E/A/O
    vinculada_entidad: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    causa_no_vinculacion: Mapped[str | None] = mapped_column(CHAR(1))  # R/D/S
    fecha_no_vinculacion: Mapped[Date | None] = mapped_column(Date)

    promedio_ingresos_mensuales: Mapped[Numeric | None] = mapped_column(Numeric(18, 2))
    fecha_promedio_ingresos: Mapped[Date | None] = mapped_column(Date)

    reporte: Mapped[ReporteROS] = relationship(back_populates="personas")

    __table_args__ = (
        CheckConstraint("relacion_entidad in ('C','E','A','O') or relacion_entidad is null",
                        name="ck_relacion_entidad"),
        CheckConstraint("causa_no_vinculacion in ('R','D','S') or causa_no_vinculacion is null",
                        name="ck_causa_no_vinc"),
    )


class OperacionSospechosa(Base):
    __tablename__ = "operacion_sospechosa"

    id_operacion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_reporte: Mapped[int] = mapped_column(ForeignKey("reporte_ros.id_reporte"), nullable=False)

    valor_total: Mapped[Numeric] = mapped_column(Numeric(18, 2), nullable=False)
    tipo_operacion: Mapped[str] = mapped_column(CHAR(1), nullable=False)  # N/I
    fecha_operacion_desde: Mapped[Date] = mapped_column(Date, nullable=False)
    fecha_operacion_hasta: Mapped[Date] = mapped_column(Date, nullable=False)

    reporte: Mapped[ReporteROS] = relationship(back_populates="operacion")

    __table_args__ = (
        CheckConstraint("tipo_operacion in ('N','I')", name="ck_tipo_operacion"),
    )
