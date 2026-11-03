# PLAN NEUQUÉN — Tablero Ejecutivo de Métricas y KPIs HyS
> **Provincia del Neuquén — Administración Central (CUIT 30-99906894-0)**  
> Plan Integral de Prevención y Verosimilitud (Ley 24.557 / SRT)

🌐 **Sitio Web en Vivo (GitHub Pages):** [https://guidodragani75-byte.github.io/plan-neuquen/](https://guidodragani75-byte.github.io/plan-neuquen/)

---

## 📌 Descripción del Tablero
Tablero interactivo para el control y seguimiento de metas de inspección, relevamientos legales (**RGRL**, **RAR**, **SVCC**) y asignación de preventores técnicos sobre el padrón de 1.837 establecimientos provinciales (1.664 activos).

Inspirado en el diseño institucional y la arquitectura de métricas del [Portal Legajo HyS (IAPSER)](https://guidodragani75-byte.github.io/checklist-iapser/portal_legajo_hys.html).

### Estructura de Pestañas:
1. **Resumen General:** Semáforo de stock de visitas (44,8% de avance), 30 visitas vencidas sin realizar, 26 urgencias de noviembre 2026, cumplimiento documental RGRL/RAR/SVCC, cobertura de Zona Fría y saneamiento de bajas en SIMP. Cada tarjeta de KPI es interactiva y permite saltar directamente a la lista de casos correspondientes.
2. **Organismos:** Distribución y ranking de avance en los principales ministerios y entes (CPE, Salud, Policía, EPAS, Trabajo, etc.).
3. **Vencimientos & Cronograma:** Curva mensual de metas inspectivas (Noviembre 2026 a Mayo 2027) y matriz departamental.
4. **Preventores & Asignación:** Alerta de cuello de botella (921 sedes activas sin preventor asignado) y rendimiento por profesional matriculado.
5. **Vista de Casos & Sedes:** Padrón detallado de 1.664 establecimientos con filtrado instantáneo por cualquiera de las métricas KPI, búsqueda libre en tiempo real, filtros cruzados (organismo, preventor, departamento, zona fría), paginación dinámica, descarga a Excel/CSV y modal de ficha técnica completa.

---

## 🔄 Sincronización Automática con Google Sheets

El tablero se mantiene permanentemente sincronizado con la hoja oficial de Google Sheets:
`https://docs.google.com/spreadsheets/d/1kxkrqu1bqtADiMKyNOP5uib-5Wv_-dNEmDngJCAJAHk/edit?gid=192789465`

### 1. En tiempo real desde el navegador:
El usuario puede hacer clic en el botón **"Actualizar"** en el encabezado de la página para obtener en el acto los datos más recientes de Google Sheets.

### 2. Automatización diaria en GitHub Actions:
El repositorio cuenta con el flujo [`.github/workflows/update_data.yml`](.github/workflows/update_data.yml) que se ejecuta **todos los días a las 06:00 UTC (03:00 de Argentina)** o ante cualquier ejecución manual (*workflow dispatch*), descargando la planilla, recalculando métricas en `data/metrics_data.json` y actualizando el despliegue sin intervención manual.

### 3. Actualización manual por consola:
```bash
python scripts/update_metrics.py
```

---

## 🛠️ Tecnologías Utilizadas
* **Tipografías:** IBM Plex Sans & IBM Plex Mono
* **Iconografía:** FontAwesome 6
* **Visualizaciones:** Chart.js 4.4
* **Procesamiento de Datos:** Python (Scripts de cálculo estadístico y exportación JSON)
* **Despliegue y CI/CD:** GitHub Actions & GitHub Pages
