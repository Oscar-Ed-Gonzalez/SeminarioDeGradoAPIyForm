// index.js
(() => {
    "use strict";

    const API_URL = "http://127.0.0.1:8000/ros";

    const $ = id => document.getElementById(id);

    // ==== Construcción del JSON ====
    function buildPayload() {
        return {
            encabezado: {
                numero_reporte: $("numero_reporte").value.trim(),
                fecha_reporte: $("fecha_reporte").value || null,
                clase_reporte: document.querySelector('input[name="clase_reporte"]:checked')?.value || null,
                numero_reporte_anterior: $("numero_reporte_anterior").value.trim()
            },
            institucion_reportante: {
                nombre_entidad: $("nombre_entidad").value.trim(),
                tipo_entidad: $("tipo_entidad").value.trim(),
                codigo_entidad: $("codigo_entidad").value.trim(),
                sucursal_presenta_operacion: $("sucursal_presenta_operacion").value.trim(),
                codigo_sucursal: $("codigo_sucursal").value.trim(),
                nombre_sucursal: $("nombre_sucursal").value.trim()
            },
            persona_implicada: {
                nombre_completo_o_razon_social: $("nombre_completo_o_razon_social").value.trim(),
                numero_identificacion: $("numero_identificacion").value.trim(),
                direccion_domicilio: $("direccion_domicilio").value.trim(),
                departamento_domicilio: $("departamento_domicilio").value.trim(),
                municipio_domicilio: $("municipio_domicilio").value.trim(),
                telefonos_domicilio: $("telefonos_domicilio").value.trim(),
                camara_comercio: $("camara_comercio").value.trim(),
                direccion_trabajo: $("direccion_trabajo").value.trim(),
                departamento_trabajo: $("departamento_trabajo").value.trim(),
                municipio_trabajo: $("municipio_trabajo").value.trim(),
                telefonos_trabajo: $("telefonos_trabajo").value.trim(),
                correo_electronico: $("correo_electronico").value.trim(),
                actividad_economica: $("actividad_economica").value.trim(),
                ciiu: $("ciiu").value.trim(),
                fecha_vinculacion: $("fecha_vinculacion").value || null,
                relacion_persona_entidad: document.querySelector('input[name="relacion_persona_entidad"]:checked')?.value || null,
                relacion_persona_entidad_otra: $("relacion_persona_entidad_otra")?.value.trim() || null,
                vinculado_aun: document.querySelector('input[name="vinculado_aun"]:checked')?.value || null,
                causa_no_vinculacion: document.querySelector('input[name="causa_no_vinculacion"]:checked')?.value || null,
                fecha_no_vinculacion: $("fecha_no_vinculacion").value || null,
                promedio_ingresos_mensuales: Number($("promedio_ingresos_mensuales").value) || null,
                fecha_promedio_ingresos: $("fecha_promedio_ingresos").value || null
            },

            operacion_sospechosa: {
                valor_total_operacion: Number($("valor_total_operacion").value) || null,
                tipo_operacion: document.querySelector('input[name="tipo_operacion"]:checked')?.value || null,
                fecha_desde: $("fecha_desde_operacion").value || null,
                fecha_hasta: $("fecha_hasta_operacion").value || null
            }
        };
    }

    // ==== Validaciones  ====
    function validatePayload(payload) {
        const errors = [];

        // Encabezado
        if (!payload.encabezado.numero_reporte)
            errors.push("Número de reporte es obligatorio");
        if (!payload.encabezado.fecha_reporte)
            errors.push("Fecha de reporte es obligatoria");
        if (!payload.encabezado.clase_reporte)
            errors.push("Clase de reporte es obligatoria");

        // Institución
        if (!payload.institucion_reportante.nombre_entidad)
            errors.push("Nombre de la entidad es obligatorio");
        if (!payload.institucion_reportante.tipo_entidad)
            errors.push("Tipo de entidad es obligatorio");
        if (!payload.institucion_reportante.codigo_entidad)
            errors.push("Código de entidad es obligatorio");

        // Persona implicada
        if (!payload.persona_implicada.nombre_completo_o_razon_social)
            errors.push("Nombre completo o razón social es obligatorio");
        if (!payload.persona_implicada.numero_identificacion)
            errors.push("Número de identificación es obligatorio");
        if (!payload.persona_implicada.correo_electronico)
            errors.push("Correo electronico es obligatorio");
        return errors;
    }


    // ==== Envío a la API ====
    async function sendPayload(payload) {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        console.log(JSON.stringify(payload))
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${await response.text()}`);
        }
        return response.json().catch(() => ({}));
    }

    // ==== Evento principal ====
    window.addEventListener("DOMContentLoaded", () => {
        const btnGuardar = $("btn_guardar");

        btnGuardar.addEventListener("click", async (e) => {
            e.preventDefault();

            const payload = buildPayload();
            const errors = validatePayload(payload);

            if (errors.length > 0) {
                alert("Corrige los siguientes errores:\n- " + errors.join("\n- "));
                return;
            }

            btnGuardar.disabled = true;
            btnGuardar.textContent = "Guardando...";

            try {
                const result = await sendPayload(payload);
                alert("Reporte guardado correctamente");
                console.log("Respuesta API:", result);
            } catch (err) {
                alert("Error al guardar el reporte: " + err.message);
                console.error(err);
            } finally {
                btnGuardar.disabled = false;
                btnGuardar.textContent = "Enviar";
            }
        });
    });

})();
