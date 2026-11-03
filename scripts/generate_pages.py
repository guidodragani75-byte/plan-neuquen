import json
import os

data_path = r'c:\Users\cript\OneDrive\Escritorio\Antigravity\NQN\data\metrics_data.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper function to generate rows
def gen_org_rows(orgs):
    rows = []
    for o in orgs:
        venc_b = f'<span class="badge badge-alert">{o["vencidas"]}</span>' if o["vencidas"] > 0 else '<span style="color:#A0B0A4;">0</span>'
        urg_b = f'<span class="badge badge-warn">{o["urgentes_nov"]}</span>' if o["urgentes_nov"] > 0 else '<span style="color:#A0B0A4;">0</span>'
        rows.append(f'''
        <tr>
          <td><strong>{o['organismo']}</strong></td>
          <td class="num">{o['total']}</td>
          <td class="num" style="color:var(--primary); font-weight:600;">{o['visitados']}</td>
          <td class="num">{o['pendientes']}</td>
          <td>
            <div class="table-progress-wrap">
              <div class="table-progress-bg">
                <div class="table-progress-bar" style="width:{o['pct_avance']}%;"></div>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:600;">{o['pct_avance']}%</span>
            </div>
          </td>
          <td class="num">{venc_b}</td>
          <td class="num">{urg_b}</td>
          <td class="num">{o['rgrl_pct']}%</td>
          <td class="num">{o['rar_pct']}%</td>
        </tr>''')
    return "".join(rows)

def gen_dept_rows(depts):
    rows = []
    for d in depts:
        rows.append(f'''
        <tr>
          <td><strong>{d['departamento']}</strong></td>
          <td class="num">{d['total']}</td>
          <td class="num" style="color:var(--primary); font-weight:600;">{d['visitados']}</td>
          <td class="num">{d['pendientes']}</td>
          <td>
            <div class="table-progress-wrap">
              <div class="table-progress-bg">
                <div class="table-progress-bar" style="width:{d['pct_avance']}%;"></div>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:600;">{d['pct_avance']}%</span>
            </div>
          </td>
        </tr>''')
    return "".join(rows)

def gen_prev_rows(prevs):
    rows = []
    for p in prevs:
        rows.append(f'''
        <tr>
          <td><strong>{p['preventor']}</strong></td>
          <td class="num">{p['asignados']}</td>
          <td class="num" style="color:var(--primary); font-weight:600;">{p['visitados']}</td>
          <td class="num">{p['pendientes']}</td>
          <td>
            <div class="table-progress-wrap">
              <div class="table-progress-bg">
                <div class="table-progress-bar" style="width:{p['pct_completado']}%;"></div>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:600;">{p['pct_completado']}%</span>
            </div>
          </td>
        </tr>''')
    return "".join(rows)

org_html = gen_org_rows(data['organismos'])
dept_html = gen_dept_rows(data['departamentos'])
prev_html = gen_prev_rows(data['preventores'])

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PLAN NEUQUÉN — Tablero Ejecutivo de Métricas y KPIs HyS</title>
  
  <!-- Tipografía IBM Plex y FontAwesome -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <!-- Chart.js para visualizaciones -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

  <style>
    :root {
      --primary: #0F5132;
      --primary-dark: #0A3622;
      --primary-light: #D1E7DD;
      --primary-accent: #198754;
      --rail-bg: #112217;
      --bg: #F5F7F5;
      --card-bg: #FFFFFF;
      --border-table: #D5DCD5;
      --border-subtle: #E3E8E3;
      --text-main: #1C241E;
      --text-muted: #5C665E;
      --alert: #DC2626;
      --alert-bg: #FEE2E2;
      --alert-text: #991B1B;
      --warn: #D97706;
      --warn-bg: #FEF3C7;
      --warn-text: #92400E;
      --info: #2563EB;
      --info-bg: #DBEAFE;
      --info-text: #1E40AF;
      --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'IBM Plex Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
    }

    /* Header Institucional */
    .header-bar {
      background: var(--rail-bg);
      color: #FFFFFF;
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--primary-accent);
      flex-wrap: wrap;
      gap: 16px;
    }

    .header-title-group {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .header-badge {
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.25);
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      font-family: var(--font-mono);
      letter-spacing: 0.5px;
      border-radius: 3px;
      color: #A3E635;
    }

    .header-title { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }
    .header-subtitle { font-size: 12px; color: #A0B0A4; margin-top: 2px; }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 14px;
      font-family: var(--font-mono);
      font-size: 12px;
    }

    .sync-status {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 6px 12px;
      border-radius: 3px;
      color: #C3D0C6;
      font-size: 11px;
    }

    .sync-btn {
      background: var(--primary-accent);
      color: #FFFFFF;
      border: none;
      padding: 7px 14px;
      font-size: 11px;
      font-weight: 600;
      font-family: var(--font-mono);
      border-radius: 3px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: background 0.2s;
    }

    .sync-btn:hover { background: #157347; }
    .sync-btn.loading i { animation: spin 1s infinite linear; }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Barra de Navegación por Pestañas */
    .tabs-nav {
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-table);
      padding: 0 32px;
      display: flex;
      gap: 8px;
      overflow-x: auto;
    }

    .tab-btn {
      padding: 14px 20px;
      background: none;
      border: none;
      border-bottom: 3px solid transparent;
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .tab-btn:hover { color: var(--primary); background: #F8FAF8; }
    .tab-btn.active { color: var(--primary); border-bottom-color: var(--primary); background: #FFFFFF; }

    .tab-counter {
      background: #E8ECE8;
      color: #404B42;
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 10px;
      font-family: var(--font-mono);
    }

    .tab-btn.active .tab-counter { background: var(--primary-light); color: var(--primary-dark); }

    /* Contenedor Principal */
    .container { max-width: 1440px; margin: 0 auto; padding: 24px 32px 48px; }
    .tab-pane { display: none; animation: fadeIn 0.2s ease-in-out; }
    .tab-pane.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

    /* Grilla de KPIs */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .kpi-card {
      background: var(--card-bg);
      border: 1px solid var(--border-table);
      padding: 18px 20px;
      border-radius: 4px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .kpi-card.alert-border { border-left: 4px solid var(--alert); }
    .kpi-card.warn-border { border-left: 4px solid var(--warn); }
    .kpi-card.success-border { border-left: 4px solid var(--primary-accent); }
    .kpi-card.info-border { border-left: 4px solid var(--info); }

    .kpi-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .kpi-label {
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
    }

    .kpi-icon { font-size: 14px; color: var(--text-muted); }
    .kpi-val {
      font-size: 28px;
      font-weight: 700;
      font-family: var(--font-mono);
      display: flex;
      align-items: baseline;
      gap: 6px;
    }

    .kpi-val .unit { font-size: 14px; font-weight: 500; color: var(--text-muted); }
    .kpi-sub {
      font-size: 12px;
      font-weight: 500;
      margin-top: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .micro-bar-bg {
      height: 5px;
      background: #E3E8E3;
      border-radius: 2px;
      overflow: hidden;
      margin-top: 10px;
    }

    .micro-bar-fill { height: 5px; border-radius: 2px; transition: width 0.4s ease; }

    /* Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 600;
      font-family: var(--font-mono);
      border-radius: 3px;
    }

    .badge-alert { background: var(--alert-bg); color: var(--alert-text); }
    .badge-warn { background: var(--warn-bg); color: var(--warn-text); }
    .badge-success { background: var(--primary-light); color: var(--primary-dark); }
    .badge-info { background: var(--info-bg); color: var(--info-text); }

    /* Paneles / Tablas */
    .panel {
      background: var(--card-bg);
      border: 1px solid var(--border-table);
      border-radius: 4px;
      padding: 20px 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .panel-title { font-size: 15px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
    .panel-subtitle { font-size: 12px; color: var(--text-muted); }

    .charts-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }

    @media (max-width: 992px) { .charts-row { grid-template-columns: 1fr; } }
    .chart-container { position: relative; height: 280px; width: 100%; }

    /* Tablas de Métricas */
    .metric-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .metric-table th {
      background: #F8FAF8;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
      padding: 10px 14px;
      text-align: left;
      border-bottom: 2px solid var(--border-table);
    }

    .metric-table td { padding: 11px 14px; border-bottom: 1px solid var(--border-subtle); }
    .metric-table tr:hover { background-color: #F8FAF8; }
    .metric-table .num { font-family: var(--font-mono); font-weight: 500; text-align: right; }
    .metric-table th.num { text-align: right; }

    .table-progress-wrap { display: flex; align-items: center; gap: 8px; width: 140px; }
    .table-progress-bg { flex: 1; height: 6px; background: #E3E8E3; border-radius: 3px; overflow: hidden; }
    .table-progress-bar { height: 6px; border-radius: 3px; background: var(--primary); }

    .alert-banner {
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      border-left: 4px solid var(--warn);
      padding: 14px 18px;
      border-radius: 4px;
      margin-bottom: 24px;
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }

    .alert-banner i { color: var(--warn); font-size: 18px; margin-top: 2px; }
    .alert-banner-content h4 { font-size: 13px; font-weight: 700; color: #92400E; }
    .alert-banner-content p { font-size: 12px; color: #78350F; margin-top: 3px; }
  </style>
</head>
<body>

  <!-- Encabezado Institucional -->
  <header class="header-bar">
    <div class="header-title-group">
      <div class="header-badge"><i class="fa-solid fa-shield-halved"></i> PLAN NEUQUÉN</div>
      <div>
        <h1 class="header-title">Tablero Ejecutivo de Métricas y KPIs HyS</h1>
        <div class="header-subtitle">Provincia del Neuquén — Administración Central | CUIT 30-99906894-0</div>
      </div>
    </div>
    <div class="header-controls">
      <div id="sync-status" class="sync-status">
        <i class="fa-solid fa-circle" style="color:#A3E635;font-size:9px;"></i>
        <span id="sync-text">Sincronizado con Sheets</span>
      </div>
      <button id="btn-sync" class="sync-btn" onclick="syncWithGoogleSheets()">
        <i class="fa-solid fa-arrows-rotate"></i> Actualizar
      </button>
    </div>
  </header>

  <!-- Pestañas de Navegación -->
  <nav class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('resumen', this)">
      <i class="fa-solid fa-chart-pie"></i> Resumen General
    </button>
    <button class="tab-btn" onclick="switchTab('organismos', this)">
      <i class="fa-solid fa-building-columns"></i> Organismos <span class="tab-counter" id="tab-counter-org">__TOTAL_ORGANISMOS__</span>
    </button>
    <button class="tab-btn" onclick="switchTab('vencimientos', this)">
      <i class="fa-solid fa-calendar-check"></i> Vencimientos & Cronograma <span class="tab-counter" id="tab-counter-crono">__TOTAL_CRITICAS__</span>
    </button>
    <button class="tab-btn" onclick="switchTab('preventores', this)">
      <i class="fa-solid fa-user-shield"></i> Preventores & Asignación <span class="tab-counter" id="tab-counter-prev">__TOTAL_PREVENTORES__</span>
    </button>
  </nav>

  <div class="container">

    <!-- ==================== PESTAÑA 1: RESUMEN GENERAL ==================== -->
    <div id="tab-resumen" class="tab-pane active">
      
      <div class="alert-banner">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <div class="alert-banner-content">
          <h4>Vencimientos Críticos y Asignaciones al 02/11/2026</h4>
          <p>Se registran <strong id="alert-vencidas">__VENCIDAS_CRITICAS__ visitas vencidas sin realizar</strong> y <strong id="alert-urgentes">__URGENTES_NOV26__ por vencer este mes</strong>. Asimismo, el <strong id="alert-sin-prev-pct">__SIN_PREVENTOR_PCT__% (__SIN_PREVENTOR__ sedes)</strong> de los establecimientos activos aún no cuenta con preventor asignado en la planilla.</p>
        </div>
      </div>

      <!-- Fila 1 de KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card success-border">
          <div class="kpi-header">
            <span class="kpi-label">Stock de Visitas Efectivas</span>
            <i class="fa-solid fa-check-double kpi-icon"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-visitados">__VISITADOS__</span> <span class="unit">/ <span id="kpi-total-activos">__TOTAL_ACTIVOS__</span></span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--primary); font-weight:600;"><span id="kpi-pct-avance">__PCT_AVANCE__</span>% del Plan Activo</span>
            <span class="badge badge-success">En Curso</span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-visitados" class="micro-bar-fill" style="width:__PCT_AVANCE__%; background:var(--primary);"></div>
          </div>
        </div>

        <div class="kpi-card alert-border">
          <div class="kpi-header">
            <span class="kpi-label">Visitas Vencidas s/Realizar</span>
            <i class="fa-solid fa-circle-exclamation kpi-icon" style="color:var(--alert);"></i>
          </div>
          <div class="kpi-val" style="color:var(--alert);">
            <span id="kpi-vencidas">__VENCIDAS_CRITICAS__</span> <span class="unit" style="color:var(--alert);">sedes</span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--alert); font-weight:600;">Plazo legal superado</span>
            <span class="badge badge-alert">Prioridad 1</span>
          </div>
          <div class="micro-bar-bg">
            <div class="micro-bar-fill" style="width:100%; background:var(--alert);"></div>
          </div>
        </div>

        <div class="kpi-card warn-border">
          <div class="kpi-header">
            <span class="kpi-label">Vencen en Noviembre 2026</span>
            <i class="fa-solid fa-clock-rotate-left kpi-icon" style="color:var(--warn);"></i>
          </div>
          <div class="kpi-val" style="color:var(--warn);">
            <span id="kpi-urgentes">__URGENTES_NOV26__</span> <span class="unit" style="color:var(--warn);">sedes</span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--warn); font-weight:600;">20 corresponden al CPE</span>
            <span class="badge badge-warn">Este Mes</span>
          </div>
          <div class="micro-bar-bg">
            <div class="micro-bar-fill" style="width:100%; background:var(--warn);"></div>
          </div>
        </div>

        <div class="kpi-card info-border">
          <div class="kpi-header">
            <span class="kpi-label">Cronograma Dic '26 - May '27</span>
            <i class="fa-solid fa-calendar-days kpi-icon" style="color:var(--info);"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-futuras">__FUTURAS_PROGRAMADAS__</span> <span class="unit">sedes</span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--text-muted);">Pico: ~160 visitas/mes</span>
            <span class="badge badge-info">Programadas</span>
          </div>
          <div class="micro-bar-bg">
            <div class="micro-bar-fill" style="width:100%; background:var(--info);"></div>
          </div>
        </div>
      </div>

      <!-- Fila 2 de KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Cumplimiento RGRL</span>
            <i class="fa-solid fa-file-shield kpi-icon"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-rgrl-si">__RGRL_SI__</span> <span class="unit">/ <span id="kpi-rgrl-tot">__TOTAL_ACTIVOS__</span></span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--primary);"><span id="kpi-rgrl-pct">__RGRL_PCT__</span>% cargados en SRT</span>
            <span class="badge badge-alert"><span id="kpi-rgrl-venc">__RGRL_VENCIDOS_PEND__</span> vencidos pend.</span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-rgrl" class="micro-bar-fill" style="width:__RGRL_PCT__%; background:var(--primary);"></div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Relevamiento RAR (Riesgos)</span>
            <i class="fa-solid fa-triangle-exclamation kpi-icon"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-rar-si">__RAR_SI__</span> <span class="unit">/ <span id="kpi-rar-tot">__TOTAL_ACTIVOS__</span></span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--primary);"><span id="kpi-rar-pct">__RAR_PCT__</span>% sedes con RAR</span>
            <span class="badge badge-info">15.472 expuestos</span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-rar" class="micro-bar-fill" style="width:__RAR_PCT__%; background:#0284C7;"></div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Vigilancia Cancerígenos (SVCC)</span>
            <i class="fa-solid fa-biohazard kpi-icon"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-svcc-si">__SVCC_SI__</span> <span class="unit">sedes</span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--text-muted);"><span id="kpi-svcc-pct">__SVCC_PCT__</span>% del padrón</span>
            <span class="badge badge-warn">Monitoreo</span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-svcc" class="micro-bar-fill" style="width:__SVCC_PCT__%; background:#D97706;"></div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Sedes en Zona Fría</span>
            <i class="fa-solid fa-snowflake kpi-icon" style="color:#0284C7;"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-zf-vis">__ZONA_FRIA_VIS__</span> <span class="unit">/ <span id="kpi-zf-tot">__ZONA_FRIA_TOTAL__</span></span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--primary);"><span id="kpi-zf-pct">__ZONA_FRIA_PCT__</span>% visitadas</span>
            <span class="badge badge-info"><span id="kpi-zf-pend">__ZONA_FRIA_PEND__</span> pendientes</span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-zf" class="micro-bar-fill" style="width:__ZONA_FRIA_PCT__%; background:#0284C7;"></div>
          </div>
        </div>
      </div>

      <!-- Gráficos Principales -->
      <div class="charts-row">
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title"><i class="fa-solid fa-chart-line"></i> Curva Histórica de Visitas Realizadas</div>
              <div class="panel-subtitle">Evolución mensual de inspecciones efectivas</div>
            </div>
            <span class="badge badge-success"><span id="badge-vis-hist">__VISITADOS__</span> visitas</span>
          </div>
          <div class="chart-container">
            <canvas id="chartHistorico"></canvas>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title"><i class="fa-solid fa-chart-pie"></i> Estado de Relevamientos Normativos</div>
              <div class="panel-subtitle">Proporción de cumplimiento RGRL, RAR y SVCC</div>
            </div>
            <span class="badge badge-info"><span id="badge-tot-activos">__TOTAL_ACTIVOS__</span> Sedes</span>
          </div>
          <div class="chart-container">
            <canvas id="chartNormativas"></canvas>
          </div>
        </div>
      </div>

      <!-- Bajas y Contactabilidad -->
      <div class="panel">
        <div class="panel-header">
          <div>
            <div class="panel-title"><i class="fa-solid fa-clipboard-check"></i> Saneamiento Administrativo & Bajas en SIMP</div>
            <div class="panel-subtitle">Establecimientos no computados en el plan activo (Total: <span id="tot-bajas">__TOTAL_BAJAS__</span> bajas)</div>
          </div>
          <span class="badge badge-warn"><span id="badge-bajas">__TOTAL_BAJAS__</span> Bajas Registradas</span>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
          <div style="background:#F8FAF8; padding:14px; border:1px solid var(--border-subtle); border-radius:4px;">
            <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:var(--text-muted)">Trámites Críticos en SIMP</div>
            <div style="font-size:18px; font-weight:700; font-family:var(--font-mono); margin-top:4px;">13 pedidos de baja/alta</div>
            <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">7 bajas y 6 pedidos de alta pendientes de validación en SIMP.</div>
          </div>
          <div style="background:#F8FAF8; padding:14px; border:1px solid var(--border-subtle); border-radius:4px;">
            <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:var(--text-muted)">Cobertura de Contactabilidad</div>
            <div style="font-size:18px; font-weight:700; font-family:var(--font-mono); margin-top:4px;">
              <span id="pct-ref">__HAS_REF_PCT__</span>% Referentes | <span id="pct-tel">__HAS_TEL_PCT__</span>% Teléfonos
            </div>
            <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">
              <span id="sin-tel-count">__SIN_TEL__</span> establecimientos sin número de contacto directo.
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ==================== PESTAÑA 2: ORGANISMOS ==================== -->
    <div id="tab-organismos" class="tab-pane">
      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title"><i class="fa-solid fa-sitemap"></i> Métricas por Organismo Gubernamental</h2>
            <div class="panel-subtitle">Desglose de avance inspectivo, cumplimiento legal y criticidades por ministerio y ente</div>
          </div>
          <span class="badge badge-success"><span id="tot-act-org">__TOTAL_ACTIVOS__</span> Establecimientos Activos</span>
        </div>

        <div class="chart-container" style="height:320px; margin-bottom:24px;">
          <canvas id="chartOrganismos"></canvas>
        </div>

        <div style="overflow-x:auto;">
          <table class="metric-table">
            <thead>
              <tr>
                <th>Organismo</th>
                <th class="num">Total Activos</th>
                <th class="num">Visitados</th>
                <th class="num">Pendientes</th>
                <th>% Avance</th>
                <th class="num">Vencidas</th>
                <th class="num">Urg. Nov</th>
                <th class="num">% RGRL</th>
                <th class="num">% RAR</th>
              </tr>
            </thead>
            <tbody id="tbody-organismos">
              __ORGANISMOS_ROWS__
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ==================== PESTAÑA 3: VENCIMIENTOS Y CRONOGRAMA ==================== -->
    <div id="tab-vencimientos" class="tab-pane">
      
      <div class="kpi-grid">
        <div class="kpi-card alert-border">
          <div class="kpi-header">
            <span class="kpi-label">Total Vencidas al 02/11</span>
            <i class="fa-solid fa-ban kpi-icon" style="color:var(--alert);"></i>
          </div>
          <div class="kpi-val" style="color:var(--alert);" id="crono-kpi-vencidas">__VENCIDAS_CRITICAS__</div>
          <div class="kpi-sub">
            <span>Superaron plazo de verosimilitud</span>
            <span class="badge badge-alert">Urgente</span>
          </div>
        </div>

        <div class="kpi-card warn-border">
          <div class="kpi-header">
            <span class="kpi-label">Urgencia Noviembre 2026</span>
            <i class="fa-solid fa-hourglass-half kpi-icon" style="color:var(--warn);"></i>
          </div>
          <div class="kpi-val" style="color:var(--warn);" id="crono-kpi-urgentes">__URGENTES_NOV26__</div>
          <div class="kpi-sub">
            <span>Vencen en los próximos 28 días</span>
            <span class="badge badge-warn">Este Mes</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Carga Diciembre 2026</span>
            <i class="fa-solid fa-calendar-day kpi-icon"></i>
          </div>
          <div class="kpi-val">160</div>
          <div class="kpi-sub">
            <span>Meta de cierre de año</span>
            <span class="badge badge-info">Programada</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Primer Semestre 2027</span>
            <i class="fa-solid fa-forward kpi-icon"></i>
          </div>
          <div class="kpi-val">702</div>
          <div class="kpi-sub">
            <span>Enero a Mayo 2027</span>
            <span class="badge badge-success">Plan 2027</span>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title"><i class="fa-solid fa-timeline"></i> Cronograma de Vencimientos de Visitas</h2>
            <div class="panel-subtitle">Cantidad de establecimientos que alcanzan su fecha límite mes a mes</div>
          </div>
          <span class="badge badge-info">Total Pendientes: <span id="tot-pend-crono">__PENDIENTES__</span></span>
        </div>
        <div class="chart-container" style="height:320px;">
          <canvas id="chartCronograma"></canvas>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title"><i class="fa-solid fa-map-location-dot"></i> Distribución Departamental de Pendientes</h2>
            <div class="panel-subtitle">Avance de visitas según departamento provincial</div>
          </div>
        </div>
        <div style="overflow-x:auto;">
          <table class="metric-table">
            <thead>
              <tr>
                <th>Departamento</th>
                <th class="num">Total Activos</th>
                <th class="num">Visitados</th>
                <th class="num">Pendientes</th>
                <th>% Cumplimiento</th>
              </tr>
            </thead>
            <tbody id="tbody-departamentos">
              __DEPARTAMENTOS_ROWS__
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ==================== PESTAÑA 4: PREVENTORES ==================== -->
    <div id="tab-preventores" class="tab-pane">
      
      <div class="alert-banner">
        <i class="fa-solid fa-user-xmark"></i>
        <div class="alert-banner-content">
          <h4>Cuello de Botella en Asignación Técnica</h4>
          <p>Actualmente <strong id="alert-prev-sin">__SIN_PREVENTOR__ establecimientos activos (__SIN_PREVENTOR_PCT__%)</strong> no tienen un profesional asignado en la planilla. Las 743 visitas realizadas fueron cubiertas por solo 12 preventores.</p>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card alert-border">
          <div class="kpi-header">
            <span class="kpi-label">Sedes sin Preventor Asignado</span>
            <i class="fa-solid fa-triangle-exclamation kpi-icon" style="color:var(--alert);"></i>
          </div>
          <div class="kpi-val" style="color:var(--alert);" id="kpi-prev-sin">__SIN_PREVENTOR__</div>
          <div class="kpi-sub">
            <span>99.1% de las visitas pendientes</span>
            <span class="badge badge-alert">Sin Asignar</span>
          </div>
        </div>

        <div class="kpi-card success-border">
          <div class="kpi-header">
            <span class="kpi-label">Sedes con Preventor Asignado</span>
            <i class="fa-solid fa-user-check kpi-icon" style="color:var(--primary);"></i>
          </div>
          <div class="kpi-val" id="kpi-prev-asig">__PREV_ASIGNADOS__</div>
          <div class="kpi-sub">
            <span>743 visitas ya completadas</span>
            <span class="badge badge-success">Asignadas</span>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Preventores en Registro</span>
            <i class="fa-solid fa-users-gear kpi-icon"></i>
          </div>
          <div class="kpi-val">16</div>
          <div class="kpi-sub">
            <span>Profesionales matriculados</span>
            <span class="badge badge-info">Capacidad</span>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title"><i class="fa-solid fa-id-card-clip"></i> Carga y Desempeño por Profesional Asignado</h2>
            <div class="panel-subtitle">Establecimientos asignados, visitas completadas y tasa de efectividad</div>
          </div>
        </div>
        <div style="overflow-x:auto;">
          <table class="metric-table">
            <thead>
              <tr>
                <th>Profesional Preventor</th>
                <th class="num">Asignados</th>
                <th class="num">Visitas Efectivas</th>
                <th class="num">Pendientes</th>
                <th>% Completado</th>
              </tr>
            </thead>
            <tbody id="tbody-preventores">
              __PREVENTORES_ROWS__
            </tbody>
          </table>
        </div>
      </div>

    </div>

  </div>

  <!-- Scripts para Navegación, Gráficos y Sincronización en Vivo -->
  <script>
    function switchTab(tabId, btn) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      const targetPane = document.getElementById('tab-' + tabId);
      if (targetPane) targetPane.classList.add('active');
      if (btn) btn.classList.add('active');

      setTimeout(() => { window.dispatchEvent(new Event('resize')); }, 50);
    }

    let dataMetrics = __DATA_JSON__;
    let chartHistInst = null;
    let chartNormInst = null;
    let chartOrgInst = null;
    let chartCronoInst = null;

    function renderCharts() {
      // 1. Gráfico Histórico
      const ctxHist = document.getElementById('chartHistorico').getContext('2d');
      if (chartHistInst) chartHistInst.destroy();
      chartHistInst = new Chart(ctxHist, {
        type: 'bar',
        data: {
          labels: dataMetrics.hist_labels.map(l => {
            const m = { '06': 'Jun', '07': 'Jul', '08': 'Ago', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic' };
            const parts = l.split('-');
            return (m[parts[1]] || parts[1]) + ' ' + parts[0];
          }),
          datasets: [{
            label: 'Visitas Realizadas',
            data: dataMetrics.hist_values,
            backgroundColor: '#0F5132',
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { color: '#E3E8E3' }, ticks: { font: { family: "'IBM Plex Mono', monospace" } } },
            x: { grid: { display: false }, ticks: { font: { family: "'IBM Plex Sans', sans-serif" } } }
          }
        }
      });

      // 2. Gráfico Normativas
      const ctxNorm = document.getElementById('chartNormativas').getContext('2d');
      if (chartNormInst) chartNormInst.destroy();
      chartNormInst = new Chart(ctxNorm, {
        type: 'doughnut',
        data: {
          labels: ['RGRL Presentado', 'RGRL Pendiente', 'RAR Presentado', 'RAR Pendiente'],
          datasets: [{
            data: [
              dataMetrics.rgrl_si,
              dataMetrics.total_activos - dataMetrics.rgrl_si,
              dataMetrics.rar_si,
              dataMetrics.total_activos - dataMetrics.rar_si
            ],
            backgroundColor: ['#0F5132', '#D1E7DD', '#0284C7', '#BAE6FD'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { font: { family: "'IBM Plex Sans', sans-serif", size: 12 } } }
          }
        }
      });

      // 3. Gráfico Organismos
      const ctxOrg = document.getElementById('chartOrganismos').getContext('2d');
      if (chartOrgInst) chartOrgInst.destroy();
      const topOrg = dataMetrics.organismos.slice(0, 7);
      chartOrgInst = new Chart(ctxOrg, {
        type: 'bar',
        data: {
          labels: topOrg.map(o => o.organismo.length > 28 ? o.organismo.substring(0, 25) + '...' : o.organismo),
          datasets: [
            { label: 'Visitados', data: topOrg.map(o => o.visitados), backgroundColor: '#0F5132', borderRadius: 3 },
            { label: 'Pendientes', data: topOrg.map(o => o.pendientes), backgroundColor: '#D1E7DD', borderRadius: 3 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: { legend: { position: 'top', labels: { font: { family: "'IBM Plex Sans', sans-serif" } } } },
          scales: {
            x: { stacked: true, grid: { color: '#E3E8E3' }, ticks: { font: { family: "'IBM Plex Mono', monospace" } } },
            y: { stacked: true, grid: { display: false }, ticks: { font: { family: "'IBM Plex Sans', sans-serif", size: 11 } } }
          }
        }
      });

      // 4. Gráfico Cronograma
      const ctxCrono = document.getElementById('chartCronograma').getContext('2d');
      if (chartCronoInst) chartCronoInst.destroy();
      chartCronoInst = new Chart(ctxCrono, {
        type: 'line',
        data: {
          labels: dataMetrics.crono_labels.map(l => {
            const m = { '01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun','07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic' };
            const p = l.split('-');
            return (m[p[1]] || p[1]) + ' ' + p[0];
          }),
          datasets: [{
            label: 'Establecimientos con Vencimiento de Visita',
            data: dataMetrics.crono_values,
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.08)',
            borderWidth: 2,
            fill: true,
            tension: 0.25,
            pointBackgroundColor: '#2563EB',
            pointRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { color: '#E3E8E3' }, ticks: { font: { family: "'IBM Plex Mono', monospace" } } },
            x: { grid: { display: false }, ticks: { font: { family: "'IBM Plex Sans', sans-serif" } } }
          }
        }
      });
    }

    // Sincronización en vivo con Google Sheets / data.json
    async function syncWithGoogleSheets() {
      const btn = document.getElementById('btn-sync');
      const syncText = document.getElementById('sync-text');
      btn.classList.add('loading');
      syncText.innerText = 'Sincronizando...';

      try {
        // Intentar primero data/metrics_data.json fresco
        const res = await fetch('data/metrics_data.json?t=' + Date.now());
        if (res.ok) {
          dataMetrics = await res.json();
          updateDOM();
          renderCharts();
          syncText.innerHTML = '<i class="fa-solid fa-circle" style="color:#A3E635;font-size:9px;"></i> En vivo (Sheets)';
          btn.classList.remove('loading');
          return;
        }
      } catch (err) {
        console.warn('Fallback a datos embebidos:', err);
      }

      syncText.innerHTML = '<i class="fa-solid fa-circle" style="color:#A3E635;font-size:9px;"></i> Actualizado';
      btn.classList.remove('loading');
    }

    function updateDOM() {
      document.getElementById('kpi-visitados').innerText = dataMetrics.visitados;
      document.getElementById('kpi-total-activos').innerText = dataMetrics.total_activos;
      document.getElementById('kpi-pct-avance').innerText = dataMetrics.pct_avance;
      document.getElementById('bar-visitados').style.width = dataMetrics.pct_avance + '%';

      document.getElementById('kpi-vencidas').innerText = dataMetrics.vencidas_criticas;
      document.getElementById('alert-vencidas').innerText = dataMetrics.vencidas_criticas + ' visitas vencidas sin realizar';

      document.getElementById('kpi-urgentes').innerText = dataMetrics.urgentes_nov26;
      document.getElementById('alert-urgentes').innerText = dataMetrics.urgentes_nov26 + ' por vencer este mes';

      document.getElementById('kpi-futuras').innerText = dataMetrics.futuras_programadas;

      document.getElementById('kpi-rgrl-si').innerText = dataMetrics.rgrl_si;
      document.getElementById('kpi-rgrl-tot').innerText = dataMetrics.total_activos;
      document.getElementById('kpi-rgrl-pct').innerText = dataMetrics.rgrl_pct;
      document.getElementById('bar-rgrl').style.width = dataMetrics.rgrl_pct + '%';
      document.getElementById('kpi-rgrl-venc').innerText = dataMetrics.rgrl_vencidos_pend;

      document.getElementById('kpi-rar-si').innerText = dataMetrics.rar_si;
      document.getElementById('kpi-rar-tot').innerText = dataMetrics.total_activos;
      document.getElementById('kpi-rar-pct').innerText = dataMetrics.rar_pct;
      document.getElementById('bar-rar').style.width = dataMetrics.rar_pct + '%';

      document.getElementById('kpi-svcc-si').innerText = dataMetrics.svcc_si;
      document.getElementById('kpi-svcc-pct').innerText = dataMetrics.svcc_pct;
      document.getElementById('bar-svcc').style.width = dataMetrics.svcc_pct + '%';

      document.getElementById('kpi-zf-vis').innerText = dataMetrics.zona_fria_vis;
      document.getElementById('kpi-zf-tot').innerText = dataMetrics.zona_fria_total;
      document.getElementById('kpi-zf-pct').innerText = dataMetrics.zona_fria_pct;
      document.getElementById('bar-zf').style.width = dataMetrics.zona_fria_pct + '%';
      document.getElementById('kpi-zf-pend').innerText = dataMetrics.zona_fria_total - dataMetrics.zona_fria_vis;
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderCharts();
      // Verificación en segundo plano si hay nuevos datos
      setTimeout(syncWithGoogleSheets, 1000);
    });
  </script>
</body>
</html>
"""

replacements = {
    '__TOTAL_ORGANISMOS__': str(len(data['organismos'])),
    '__TOTAL_CRITICAS__': str(data['vencidas_criticas'] + data['urgentes_nov26']),
    '__TOTAL_PREVENTORES__': str(len(data['preventores'])),
    '__VENCIDAS_CRITICAS__': str(data['vencidas_criticas']),
    '__URGENTES_NOV26__': str(data['urgentes_nov26']),
    '__SIN_PREVENTOR__': str(data['sin_preventor']),
    '__SIN_PREVENTOR_PCT__': str(round(data['sin_preventor'] / data['total_activos'] * 100, 1)),
    '__VISITADOS__': str(data['visitados']),
    '__TOTAL_ACTIVOS__': str(data['total_activos']),
    '__PCT_AVANCE__': str(data['pct_avance']),
    '__FUTURAS_PROGRAMADAS__': str(data['futuras_programadas']),
    '__RGRL_SI__': str(data['rgrl_si']),
    '__RGRL_PCT__': str(data['rgrl_pct']),
    '__RGRL_VENCIDOS_PEND__': str(data['rgrl_vencidos_pend']),
    '__RAR_SI__': str(data['rar_si']),
    '__RAR_PCT__': str(data['rar_pct']),
    '__SVCC_SI__': str(data['svcc_si']),
    '__SVCC_PCT__': str(data['svcc_pct']),
    '__ZONA_FRIA_VIS__': str(data['zona_fria_vis']),
    '__ZONA_FRIA_TOTAL__': str(data['zona_fria_total']),
    '__ZONA_FRIA_PCT__': str(data['zona_fria_pct']),
    '__ZONA_FRIA_PEND__': str(data['zona_fria_total'] - data['zona_fria_vis']),
    '__TOTAL_BAJAS__': str(data['total_bajas']),
    '__HAS_REF_PCT__': str(round(data['has_ref'] / data['total_activos'] * 100, 1)),
    '__HAS_TEL_PCT__': str(round(data['has_tel'] / data['total_activos'] * 100, 1)),
    '__SIN_TEL__': str(data['total_activos'] - data['has_tel']),
    '__PREV_ASIGNADOS__': str(data['prev_asignados']),
    '__PENDIENTES__': str(data['pendientes']),
    '__ORGANISMOS_ROWS__': org_html,
    '__DEPARTAMENTOS_ROWS__': dept_html,
    '__PREVENTORES_ROWS__': prev_html,
    '__DATA_JSON__': json.dumps(data, ensure_ascii=False)
}

final_html = html_template
for k, v in replacements.items():
    final_html = final_html.replace(k, v)

# Save both index.html and PLAN_NEUQUEN.html
for fname in ['index.html', 'PLAN_NEUQUEN.html']:
    target = os.path.join(r'c:\Users\cript\OneDrive\Escritorio\Antigravity\NQN', fname)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Written: {target} ({len(final_html)} bytes)")
