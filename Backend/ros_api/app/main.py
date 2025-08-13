from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas
from .mappers import (
    map_relacion_persona_entidad, map_causa_no_vinculacion, map_tipo_operacion,
    persona_defaults_vinculacion, operacion_completa
)

app = FastAPI(title="ROS API", version="1.0.0")

# Lista de orígenes permitidos (puedes poner '*' pero no es lo más seguro)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],    # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],    # Permitir todas las cabeceras
)

# Crear tablas si no existen (para demo). En producción usa Alembic.
Base.metadata.create_all(bind=engine)


@app.post("/ros", response_model=schemas.ROSCreated, status_code=201)
def crear_reporte(ros: schemas.ROSIn, db: Session = Depends(get_db)):
    """
    Crea un reporte y guarda institución, persona y operación de forma transaccional.
    Reglas:
      - Institución: requiere nombre_entidad, tipo_entidad, codigo_entidad (NOT NULL).
      - Persona: 'vinculada_entidad' no puede ser NULL → por defecto True si no llega.
      - Operación: solo se inserta si llegan TODOS los campos obligatorios; si no, se omite.
    """
    # Validación extra de institución (por si vinieran strings vacíos)
    if not (ros.institucion_reportante.nombre_entidad
            and ros.institucion_reportante.tipo_entidad
            and ros.institucion_reportante.codigo_entidad):
        raise HTTPException(status_code=422, detail="Institución: nombre_entidad, tipo_entidad y codigo_entidad son obligatorios.")

    try:
        with db.begin():
            # 1) reporte_ros
            rep = models.ReporteROS(
                numero_reporte=ros.encabezado.numero_reporte.strip(),
                fecha_reporte=ros.encabezado.fecha_reporte,
                clase_reporte=ros.encabezado.clase_reporte,
                numero_reporte_anterior=ros.encabezado.numero_reporte_anterior or None
            )
            db.add(rep)
            db.flush()  # para obtener rep.id_reporte

            # 2) institucion_reportante
            inst = models.InstitucionReportante(
                id_reporte=rep.id_reporte,
                nombre_entidad=ros.institucion_reportante.nombre_entidad.strip(),
                tipo_entidad=ros.institucion_reportante.tipo_entidad.strip(),
                codigo_entidad=ros.institucion_reportante.codigo_entidad.strip(),
                sucursal_oficina=(ros.institucion_reportante.sucursal_presenta_operacion or None),
                codigo_sucursal=(ros.institucion_reportante.codigo_sucursal or None),
                nombre_sucursal=(ros.institucion_reportante.nombre_sucursal or None),
            )
            db.add(inst)

            # 3) persona_implicada (tu JSON actual trae 1 persona; si luego usas lista, haz un loop)
            p = ros.persona_implicada
            per = models.PersonaImplicada(
                id_reporte=rep.id_reporte,
                nombre_completo=p.nombre_completo_o_razon_social.strip(),
                numero_identificacion=p.numero_identificacion.strip(),

                direccion_domicilio=p.direccion_domicilio or None,
                departamento_domicilio=p.departamento_domicilio or None,
                municipio_domicilio=p.municipio_domicilio or None,
                telefono_domicilio=p.telefonos_domicilio or None,

                camara_comercio=p.camara_comercio or None,
                direccion_trabajo=p.direccion_trabajo or None,
                departamento_trabajo=p.departamento_trabajo or None,
                municipio_trabajo=p.municipio_trabajo or None,
                telefono_trabajo=p.telefonos_trabajo or None,

                correo_electronico=p.correo_electronico or None,
                actividad_economica=p.actividad_economica or None,
                ciiu=p.ciiu or None,
                fecha_vinculacion=p.fecha_vinculacion,

                relacion_entidad=map_relacion_persona_entidad(p.relacion_persona_entidad),
                vinculada_entidad=persona_defaults_vinculacion(p.vinculado_aun),
                causa_no_vinculacion=map_causa_no_vinculacion(p.causa_no_vinculacion),
                fecha_no_vinculacion=p.fecha_no_vinculacion,

                promedio_ingresos_mensuales=p.promedio_ingresos_mensuales,
                fecha_promedio_ingresos=p.fecha_promedio_ingresos
            )
            db.add(per)

            # 4) operacion_sospechosa (solo si viene completa)
            ops = ros.operacion_sospechosa
            if operacion_completa(ops):
                op = models.OperacionSospechosa(
                    id_reporte=rep.id_reporte,
                    valor_total=ops.valor_total_operacion,
                    tipo_operacion=map_tipo_operacion(ops.tipo_operacion) or
                                   _raise_422("tipo_operacion debe ser 'nacional' o 'internacional'"),
                    fecha_operacion_desde=ops.fecha_desde,
                    fecha_operacion_hasta=ops.fecha_hasta
                )
                db.add(op)
            # Si no viene completa, la omitimos (puedes cambiar esto a 422 si quieres forzarla)

        return {"id_reporte": rep.id_reporte, "message": "created"}

    except HTTPException:
        raise
    except Exception as ex:
        # Errores de integridad (checks, not nulls, etc.)
        raise HTTPException(status_code=400, detail=str(ex))


def _raise_422(msg: str):
    raise HTTPException(status_code=422, detail=msg)
