from typing import Optional
from .schemas import PersonaImplicadaIn, OperacionSospechosaIn

def map_relacion_persona_entidad(valor: Optional[str]) -> Optional[str]:
    """
    cliente→C, empleado→E, accionista→A, otra→O, None→None
    """
    if not valor:
        return None
    v = valor.strip().lower()
    return {"cliente": "C", "empleado": "E", "accionista": "A", "otra": "O"}.get(v, None)

def map_causa_no_vinculacion(valor: Optional[str]) -> Optional[str]:
    """
    retiro_voluntario→R, decision_institucion→D, suspension→S
    """
    if not valor:
        return None
    v = valor.strip().lower()
    return {"retiro_voluntario": "R", "decision_institucion": "D", "suspension": "S"}.get(v, None)

def map_tipo_operacion(valor: Optional[str]) -> Optional[str]:
    """
    nacional→N, internacional→I
    """
    if not valor:
        return None
    v = valor.strip().lower()
    return {"nacional": "N", "internacional": "I"}.get(v, None)

def persona_defaults_vinculacion(vinculado_aun: Optional[bool]) -> bool:
    """
    La tabla exige NOT NULL en vinculada_entidad; si no llega, asumimos True.
    Ajusta la política si prefieres rechazar cuando sea None.
    """
    return True if vinculado_aun is None else bool(vinculado_aun)

def operacion_completa(ops: OperacionSospechosaIn) -> bool:
    """
    La tabla operacion_sospechosa tiene todos los campos NOT NULL.
    Solo insertamos si viene todo completo y consistente.
    """
    return (
        ops.valor_total_operacion is not None and
        ops.tipo_operacion is not None and
        ops.fecha_desde is not None and
        ops.fecha_hasta is not None
    )
