import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
metrics_path = os.path.join(base_dir, 'data', 'metrics_data.json')
casos_path = os.path.join(base_dir, 'data', 'casos_data.json')

with open(metrics_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

casos = []
if os.path.exists(casos_path):
    with open(casos_path, 'r', encoding='utf-8') as f:
        casos = json.load(f)

# Helper function to generate rows
def gen_org_rows(orgs):
    rows = []
    for o in orgs:
        venc_b = f'<span class="badge badge-alert" style="cursor:pointer;" onclick="event.stopPropagation(); abrirCasosConFiltro(\'{o["organismo"]}\', \'vencidas\')">{o["vencidas"]}</span>' if o["vencidas"] > 0 else '<span style="color:#A0B0A4;">0</span>'
        urg_b = f'<span class="badge badge-warn" style="cursor:pointer;" onclick="event.stopPropagation(); abrirCasosConFiltro(\'{o["organismo"]}\', \'urgentes_nov\')">{o["urgentes_nov"]}</span>' if o["urgentes_nov"] > 0 else '<span style="color:#A0B0A4;">0</span>'
        rows.append(f'''
        <tr style="cursor:pointer;" onclick="abrirCasosConFiltro('{o["organismo"]}', 'todos')" title="Ver casos de este organismo">
          <td><strong>{o['organismo']}</strong> <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:10px; color:var(--text-muted); margin-left:4px;"></i></td>
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
        <tr style="cursor:pointer;" onclick="abrirCasosPorDepto('{d["departamento"]}')" title="Ver casos de este departamento">
          <td><strong>{d['departamento']}</strong> <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:10px; color:var(--text-muted); margin-left:4px;"></i></td>
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
        <tr style="cursor:pointer;" onclick="abrirCasosPorPreventor('{p["preventor"]}')" title="Ver casos asignados a este profesional">
          <td><strong>{p['preventor']}</strong> <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:10px; color:var(--text-muted); margin-left:4px;"></i></td>
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
    .tab-btn-highlight { color: #0284C7; }
    .tab-btn-highlight.active { color: var(--primary-dark); }

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
      position: relative;
    }

    .kpi-card.clickable {
      cursor: pointer;
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
      user-select: none;
    }

    .kpi-card.clickable:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(15, 81, 50, 0.1);
      border-color: #0F5132;
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
      gap: 6px;
      flex-wrap: wrap;
    }

    .kpi-action-hint {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 5px;
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px dashed var(--border-subtle);
      font-size: 11px;
      font-weight: 600;
      color: var(--primary);
      opacity: 0.8;
      transition: opacity 0.15s, transform 0.15s;
    }
    .kpi-card.clickable:hover .kpi-action-hint {
      opacity: 1;
      transform: translateX(2px);
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
    .badge-neutral { background: #E8ECE8; color: #404B42; }

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

    /* ==================== ESTILOS PARA VISTA DE CASOS ==================== */
    .chips-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }

    .chip-btn {
      background: #FFFFFF;
      border: 1px solid var(--border-table);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: var(--font-sans);
    }

    .chip-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
      background: #F8FAF8;
    }

    .chip-btn.active {
      background: var(--rail-bg);
      color: #FFFFFF;
      border-color: var(--rail-bg);
      box-shadow: 0 2px 6px rgba(15, 81, 50, 0.25);
    }

    .chip-count {
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 1px 6px;
      border-radius: 10px;
      background: #E8ECE8;
      color: #2D3748;
    }

    .chip-btn.active .chip-count {
      background: rgba(255, 255, 255, 0.25);
      color: #FFFFFF;
    }

    .filter-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      background: #F8FAF8;
      padding: 12px 16px;
      border-radius: 6px;
      border: 1px solid var(--border-subtle);
      margin-bottom: 16px;
    }

    .filter-search-wrap {
      flex: 1 1 260px;
      position: relative;
    }

    .filter-search-input {
      width: 100%;
      padding: 9px 12px 9px 34px;
      font-size: 13px;
      font-family: var(--font-sans);
      border: 1px solid var(--border-table);
      border-radius: 4px;
      background: #FFFFFF;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .filter-search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(15, 81, 50, 0.12);
    }

    .filter-search-icon {
      position: absolute;
      left: 11px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 13px;
    }

    .filter-select {
      padding: 8px 12px;
      font-size: 12px;
      font-family: var(--font-sans);
      border: 1px solid var(--border-table);
      border-radius: 4px;
      background: #FFFFFF;
      outline: none;
      color: var(--text-main);
      cursor: pointer;
      max-width: 220px;
    }

    .filter-select:focus { border-color: var(--primary); }

    .action-btn {
      padding: 7px 14px;
      font-size: 12px;
      font-weight: 600;
      font-family: var(--font-sans);
      border-radius: 4px;
      border: 1px solid var(--border-table);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .action-btn:hover { background: #F1F4F1; border-color: #BAC2BA; }

    .action-btn-primary {
      background: var(--primary);
      color: #FFFFFF;
      border-color: var(--primary);
    }
    .action-btn-primary:hover { background: var(--primary-dark); }

    .action-btn-success {
      background: #198754;
      color: #FFFFFF;
      border-color: #198754;
    }
    .action-btn-success:hover { background: #146C43; }

    .casos-summary-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--text-muted);
      padding: 8px 4px;
      margin-bottom: 8px;
      flex-wrap: wrap;
      gap: 10px;
    }

    .casos-table td { vertical-align: middle; }
    .estab-title { font-size: 13px; font-weight: 600; color: var(--text-main); line-height: 1.3; }
    .estab-dom { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px solid var(--border-subtle);
      flex-wrap: wrap;
      gap: 12px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .pagination-controls {
      display: flex;
      gap: 4px;
      align-items: center;
    }

    .pag-btn {
      border: 1px solid var(--border-table);
      background: #FFFFFF;
      padding: 5px 10px;
      font-size: 12px;
      font-family: var(--font-mono);
      border-radius: 3px;
      cursor: pointer;
      color: var(--text-main);
      transition: all 0.15s;
    }

    .pag-btn:hover:not(:disabled) { background: #F1F4F1; border-color: var(--primary); color: var(--primary); }
    .pag-btn.active { background: var(--primary); color: #FFFFFF; border-color: var(--primary); }
    .pag-btn:disabled { opacity: 0.4; cursor: not-allowed; }

    /* Modal Ficha Técnica */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(17, 34, 23, 0.65);
      backdrop-filter: blur(2px);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }

    .modal-overlay.open { opacity: 1; pointer-events: auto; }

    .modal-container {
      background: #FFFFFF;
      border-radius: 8px;
      width: 100%;
      max-width: 860px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
      display: flex;
      flex-direction: column;
      transform: translateY(12px);
      transition: transform 0.2s ease;
    }

    .modal-overlay.open .modal-container { transform: translateY(0); }

    .modal-header {
      padding: 20px 24px;
      background: var(--rail-bg);
      color: #FFFFFF;
      border-bottom: 2px solid var(--primary-accent);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .modal-close-btn {
      background: rgba(255, 255, 255, 0.15);
      border: none;
      color: #FFFFFF;
      width: 32px;
      height: 32px;
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      transition: background 0.2s;
    }

    .modal-close-btn:hover { background: rgba(255, 255, 255, 0.3); }

    .modal-body { padding: 24px; }

    .ficha-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }

    .ficha-box {
      background: #F8FAF8;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px 14px;
    }

    .ficha-box-label {
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }

    .ficha-box-val {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      word-break: break-word;
    }

    .ficha-section-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--primary-dark);
      margin: 18px 0 10px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-subtle);
    }
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
    <button class="tab-btn active" id="btn-tab-resumen" onclick="switchTab('resumen', this)">
      <i class="fa-solid fa-chart-pie"></i> Resumen General
    </button>
    <button class="tab-btn" id="btn-tab-organismos" onclick="switchTab('organismos', this)">
      <i class="fa-solid fa-building-columns"></i> Organismos <span class="tab-counter" id="tab-counter-org">__TOTAL_ORGANISMOS__</span>
    </button>
    <button class="tab-btn" id="btn-tab-vencimientos" onclick="switchTab('vencimientos', this)">
      <i class="fa-solid fa-calendar-check"></i> Vencimientos & Cronograma <span class="tab-counter" id="tab-counter-crono">__TOTAL_CRITICAS__</span>
    </button>
    <button class="tab-btn" id="btn-tab-preventores" onclick="switchTab('preventores', this)">
      <i class="fa-solid fa-user-shield"></i> Preventores & Asignación <span class="tab-counter" id="tab-counter-prev">__TOTAL_PREVENTORES__</span>
    </button>
    <button class="tab-btn tab-btn-highlight" id="btn-tab-casos" onclick="switchTab('casos', this)">
      <i class="fa-solid fa-table-list"></i> Vista de Casos & Sedes <span class="tab-counter" id="tab-counter-casos">__TOTAL_ACTIVOS__</span>
    </button>
  </nav>

  <div class="container">

    <!-- ==================== PESTAÑA 1: RESUMEN GENERAL ==================== -->
    <div id="tab-resumen" class="tab-pane active">
      
      <div class="alert-banner">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <div class="alert-banner-content">
          <h4>Vencimientos Críticos y Asignaciones al 02/11/2026</h4>
          <p>Se registran <strong id="alert-vencidas" style="cursor:pointer; text-decoration:underline;" onclick="abrirCasos('vencidas')">__VENCIDAS_CRITICAS__ visitas vencidas sin realizar</strong> y <strong id="alert-urgentes" style="cursor:pointer; text-decoration:underline;" onclick="abrirCasos('urgentes_nov')">__URGENTES_NOV26__ por vencer este mes</strong>. Asimismo, el <strong id="alert-sin-prev-pct" style="cursor:pointer; text-decoration:underline;" onclick="abrirCasos('sin_preventor')">__SIN_PREVENTOR_PCT__% (__SIN_PREVENTOR__ sedes)</strong> de los establecimientos activos aún no cuenta con preventor asignado en la planilla.</p>
        </div>
      </div>

      <!-- Fila 1 de KPIs (Clicables para ver casos) -->
      <div class="kpi-grid">
        <!-- KPI 1: Stock Visitas Efectivas -->
        <div class="kpi-card success-border clickable" onclick="abrirCasos('visitados')" title="Haga clic para ver los 745 casos con visitas efectivas realizadas">
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
          <div class="kpi-action-hint">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver los 745 casos
          </div>
        </div>

        <!-- KPI 2: Visitas Vencidas s/Realizar -->
        <div class="kpi-card alert-border clickable" onclick="abrirCasos('vencidas')" title="Haga clic para ver los 30 casos con visitas vencidas sin realizar">
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
          <div class="kpi-action-hint" style="color:var(--alert);">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver los 30 casos vencidos
          </div>
        </div>

        <!-- KPI 3: Vencen en Noviembre 2026 -->
        <div class="kpi-card warn-border clickable" onclick="abrirCasos('urgentes_nov')" title="Haga clic para ver los 26 casos que vencen este mes">
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
          <div class="kpi-action-hint" style="color:var(--warn);">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver los 26 casos urgentes
          </div>
        </div>

        <!-- KPI 4: Cronograma Dic '26 - May '27 -->
        <div class="kpi-card info-border clickable" onclick="abrirCasos('futuras')" title="Haga clic para ver las 863 sedes con visitas programadas">
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
          <div class="kpi-action-hint" style="color:var(--info);">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver las 863 sedes programadas
          </div>
        </div>
      </div>

      <!-- Fila 2 de KPIs (Clicables para ver casos) -->
      <div class="kpi-grid">
        <!-- KPI 5: Cumplimiento RGRL -->
        <div class="kpi-card clickable" onclick="abrirCasos('rgrl_si')" title="Haga clic para ver los 747 casos con RGRL cargado en SRT">
          <div class="kpi-header">
            <span class="kpi-label">Cumplimiento RGRL</span>
            <i class="fa-solid fa-file-shield kpi-icon"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-rgrl-si">__RGRL_SI__</span> <span class="unit">/ <span id="kpi-rgrl-tot">__TOTAL_ACTIVOS__</span></span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--primary);"><span id="kpi-rgrl-pct">__RGRL_PCT__</span>% cargados en SRT</span>
            <span class="badge badge-alert" style="cursor:pointer;" onclick="event.stopPropagation(); abrirCasos('rgrl_vencidos')">
              <span id="kpi-rgrl-venc">__RGRL_VENCIDOS_PEND__</span> vencidos pend.
            </span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-rgrl" class="micro-bar-fill" style="width:__RGRL_PCT__%; background:var(--primary);"></div>
          </div>
          <div class="kpi-action-hint">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver casos RGRL
          </div>
        </div>

        <!-- KPI 6: Relevamiento RAR -->
        <div class="kpi-card clickable" onclick="abrirCasos('rar_si')" title="Haga clic para ver las 556 sedes con relevamiento RAR presentado">
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
          <div class="kpi-action-hint" style="color:#0284C7;">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver los 556 casos RAR
          </div>
        </div>

        <!-- KPI 7: Vigilancia SVCC -->
        <div class="kpi-card clickable" onclick="abrirCasos('svcc_si')" title="Haga clic para ver las 50 sedes con vigilancia SVCC (Cancerígenos)">
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
          <div class="kpi-action-hint" style="color:#D97706;">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver las 50 sedes SVCC
          </div>
        </div>

        <!-- KPI 8: Sedes en Zona Fría -->
        <div class="kpi-card clickable" onclick="abrirCasos('zona_fria')" title="Haga clic para ver las 209 sedes ubicadas en Zona Fría">
          <div class="kpi-header">
            <span class="kpi-label">Sedes en Zona Fría</span>
            <i class="fa-solid fa-snowflake kpi-icon" style="color:#0284C7;"></i>
          </div>
          <div class="kpi-val">
            <span id="kpi-zf-vis">__ZONA_FRIA_VIS__</span> <span class="unit">/ <span id="kpi-zf-tot">__ZONA_FRIA_TOTAL__</span></span>
          </div>
          <div class="kpi-sub">
            <span style="color:var(--primary);"><span id="kpi-zf-pct">__ZONA_FRIA_PCT__</span>% visitadas</span>
            <span class="badge badge-info" style="cursor:pointer;" onclick="event.stopPropagation(); abrirCasos('zona_fria_pend')">
              <span id="kpi-zf-pend">__ZONA_FRIA_PEND__</span> pendientes
            </span>
          </div>
          <div class="micro-bar-bg">
            <div id="bar-zf" class="micro-bar-fill" style="width:__ZONA_FRIA_PCT__%; background:#0284C7;"></div>
          </div>
          <div class="kpi-action-hint" style="color:#0284C7;">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver las 209 sedes Zona Fría
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
            <div class="panel-subtitle">Desglose de avance inspectivo, cumplimiento legal y criticidades por ministerio y ente (Haga clic en una fila para ver sus casos)</div>
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
        <div class="kpi-card alert-border clickable" onclick="abrirCasos('vencidas')" title="Ver las 30 sedes con visitas vencidas">
          <div class="kpi-header">
            <span class="kpi-label">Total Vencidas al 02/11</span>
            <i class="fa-solid fa-ban kpi-icon" style="color:var(--alert);"></i>
          </div>
          <div class="kpi-val" style="color:var(--alert);" id="crono-kpi-vencidas">__VENCIDAS_CRITICAS__</div>
          <div class="kpi-sub">
            <span>Superaron plazo de verosimilitud</span>
            <span class="badge badge-alert">Urgente</span>
          </div>
          <div class="kpi-action-hint" style="color:var(--alert);">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver casos vencidos
          </div>
        </div>

        <div class="kpi-card warn-border clickable" onclick="abrirCasos('urgentes_nov')" title="Ver las 26 sedes que vencen este mes">
          <div class="kpi-header">
            <span class="kpi-label">Urgencia Noviembre 2026</span>
            <i class="fa-solid fa-hourglass-half kpi-icon" style="color:var(--warn);"></i>
          </div>
          <div class="kpi-val" style="color:var(--warn);" id="crono-kpi-urgentes">__URGENTES_NOV26__</div>
          <div class="kpi-sub">
            <span>Vencen en los próximos 28 días</span>
            <span class="badge badge-warn">Este Mes</span>
          </div>
          <div class="kpi-action-hint" style="color:var(--warn);">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver casos urgentes
          </div>
        </div>

        <div class="kpi-card clickable" onclick="abrirCasos('futuras')" title="Ver sedes con cronograma futuro">
          <div class="kpi-header">
            <span class="kpi-label">Carga Diciembre 2026</span>
            <i class="fa-solid fa-calendar-day kpi-icon"></i>
          </div>
          <div class="kpi-val">160</div>
          <div class="kpi-sub">
            <span>Meta de cierre de año</span>
            <span class="badge badge-info">Programada</span>
          </div>
          <div class="kpi-action-hint">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver programadas
          </div>
        </div>

        <div class="kpi-card clickable" onclick="abrirCasos('futuras')" title="Ver sedes con cronograma primer semestre 2027">
          <div class="kpi-header">
            <span class="kpi-label">Primer Semestre 2027</span>
            <i class="fa-solid fa-forward kpi-icon"></i>
          </div>
          <div class="kpi-val">702</div>
          <div class="kpi-sub">
            <span>Enero a Mayo 2027</span>
            <span class="badge badge-success">Plan 2027</span>
          </div>
          <div class="kpi-action-hint">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver cronograma 2027
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
            <div class="panel-subtitle">Avance de visitas según departamento provincial (Haga clic en una fila para ver sus casos)</div>
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
          <p>Actualmente <strong id="alert-prev-sin" style="cursor:pointer; text-decoration:underline;" onclick="abrirCasos('sin_preventor')">__SIN_PREVENTOR__ establecimientos activos (__SIN_PREVENTOR_PCT__%)</strong> no tienen un profesional asignado en la planilla. Las 743 visitas realizadas fueron cubiertas por solo 12 preventores.</p>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card alert-border clickable" onclick="abrirCasos('sin_preventor')" title="Ver las 921 sedes sin profesional preventor asignado">
          <div class="kpi-header">
            <span class="kpi-label">Sedes sin Preventor Asignado</span>
            <i class="fa-solid fa-triangle-exclamation kpi-icon" style="color:var(--alert);"></i>
          </div>
          <div class="kpi-val" style="color:var(--alert);" id="kpi-prev-sin">__SIN_PREVENTOR__</div>
          <div class="kpi-sub">
            <span>99.1% de las visitas pendientes</span>
            <span class="badge badge-alert">Sin Asignar</span>
          </div>
          <div class="kpi-action-hint" style="color:var(--alert);">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver las 921 sedes sin preventor
          </div>
        </div>

        <div class="kpi-card success-border clickable" onclick="abrirCasos('prev_asignados')" title="Ver las 743 sedes con profesional asignado">
          <div class="kpi-header">
            <span class="kpi-label">Sedes con Preventor Asignado</span>
            <i class="fa-solid fa-user-check kpi-icon" style="color:var(--primary);"></i>
          </div>
          <div class="kpi-val" id="kpi-prev-asig">__PREV_ASIGNADOS__</div>
          <div class="kpi-sub">
            <span>743 visitas ya completadas</span>
            <span class="badge badge-success">Asignadas</span>
          </div>
          <div class="kpi-action-hint">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ver sedes asignadas
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">Preventores en Registro</span>
            <i class="fa-solid fa-users-gear kpi-icon"></i>
          </div>
          <div class="kpi-val">__TOTAL_PREVENTORES__</div>
          <div class="kpi-sub">
            <span>Equipo técnico en territorio</span>
            <span class="badge badge-info">Activos</span>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title"><i class="fa-solid fa-id-card-clip"></i> Carga y Desempeño por Profesional Asignado</h2>
            <div class="panel-subtitle">Establecimientos asignados, visitas completadas y tasa de efectividad (Haga clic en un preventor para ver sus casos)</div>
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

    <!-- ==================== PESTAÑA 5: VISTA DETALLADA DE CASOS & SEDES ==================== -->
    <div id="tab-casos" class="tab-pane">
      
      <div class="panel">
        <div class="panel-header" style="flex-wrap: wrap; gap: 14px;">
          <div>
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--primary); margin-bottom: 4px;">
              <a href="javascript:void(0)" onclick="switchTab('resumen', document.getElementById('btn-tab-resumen'))" style="color:var(--primary); text-decoration:none;">
                <i class="fa-solid fa-arrow-left"></i> Volver al Resumen General
              </a>
            </div>
            <h2 class="panel-title" style="font-size: 18px; margin-top: 2px;">
              <i class="fa-solid fa-table-list" style="color:var(--primary);"></i> Padrón & Vista Detallada de Sedes y Casos HyS
            </h2>
            <div class="panel-subtitle">
              Exploración interactiva caso a caso, trazabilidad inspectiva, búsqueda cruzada y ficha técnica individual.
            </div>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
            <button class="action-btn action-btn-success" onclick="exportarCasosCSV()" title="Descargar planilla CSV compatible con Microsoft Excel">
              <i class="fa-solid fa-file-excel"></i> Exportar a Excel (CSV)
            </button>
            <button class="action-btn" onclick="resetCasosFiltros()" title="Restablecer todos los filtros y buscador">
              <i class="fa-solid fa-arrows-rotate"></i> Limpiar Filtros
            </button>
          </div>
        </div>

        <!-- Barra de Filtros Rápidos (KPI Chips) -->
        <div style="margin-top: 14px; margin-bottom: 8px;">
          <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--text-muted); letter-spacing:0.5px; margin-bottom:8px;">
            <i class="fa-solid fa-filter"></i> Seleccione una Categoría o Métrica KPI para explorar sus casos:
          </div>
          <div class="chips-container" id="kpi-chips-container">
            <!-- Renderizado dinámicamente -->
          </div>
        </div>

        <!-- Barra de Búsqueda y Filtros Combinados -->
        <div class="filter-bar">
          <div class="filter-search-wrap">
            <i class="fa-solid fa-magnifying-glass filter-search-icon"></i>
            <input type="text" id="casos-search" class="filter-search-input" placeholder="Buscar por establecimiento, CUIT, organismo, depto, domicilio, referente..." oninput="filtrarCasos(true)">
          </div>

          <select id="casos-filter-org" class="filter-select" onchange="filtrarCasos(true)">
            <option value="">Todos los Organismos</option>
          </select>

          <select id="casos-filter-prev" class="filter-select" onchange="filtrarCasos(true)">
            <option value="">Todos los Preventores</option>
            <option value="__SIN_PREV__">⚠️ Sin Preventor Asignado</option>
          </select>

          <select id="casos-filter-depto" class="filter-select" onchange="filtrarCasos(true)">
            <option value="">Todos los Departamentos</option>
          </select>

          <select id="casos-filter-zf" class="filter-select" onchange="filtrarCasos(true)">
            <option value="">Zona Fría: Todas</option>
            <option value="si">Solo Zona Fría</option>
            <option value="no">Fuera de Zona Fría</option>
          </select>
        </div>

        <!-- Resumen del Estado de Filtro y Contador -->
        <div class="casos-summary-bar">
          <div>
            Mostrando <strong id="casos-count-filtered" style="font-family:var(--font-mono); font-size:14px; color:var(--primary-dark);">0</strong> de <span id="casos-count-total" style="font-family:var(--font-mono);">__TOTAL_ACTIVOS__</span> sedes activas
            <span id="casos-active-filter-badge" class="badge badge-info" style="margin-left: 8px;"></span>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:12px; color:var(--text-muted);">Paginación:</span>
            <select id="casos-page-size" class="filter-select" style="padding:4px 8px; width:auto;" onchange="cambiarPageSize(this.value)">
              <option value="25">25 por pág.</option>
              <option value="50" selected>50 por pág.</option>
              <option value="100">100 por pág.</option>
              <option value="250">250 por pág.</option>
              <option value="all">Todas las sedes</option>
            </select>
          </div>
        </div>

        <!-- Tabla de Casos -->
        <div style="overflow-x:auto;">
          <table class="metric-table casos-table">
            <thead>
              <tr>
                <th style="width:45px;">#</th>
                <th>Establecimiento & Domicilio</th>
                <th>Organismo</th>
                <th>Departamento</th>
                <th>Preventor Asignado</th>
                <th>Estado Visita</th>
                <th class="num">RGRL</th>
                <th class="num">RAR</th>
                <th class="num">SVCC</th>
                <th>Contacto Referente</th>
                <th style="text-align:center; width:70px;">Acción</th>
              </tr>
            </thead>
            <tbody id="tbody-casos">
              <!-- Renderizado dinámicamente -->
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="pagination-bar" id="casos-pagination">
          <div id="pag-info">Mostrando página 1</div>
          <div class="pagination-controls" id="pag-buttons"></div>
        </div>

      </div>

    </div>

  </div>

  <!-- Modal Ficha Técnica de la Sede -->
  <div id="modal-ficha" class="modal-overlay" onclick="cerrarModalFicha(event)">
    <div class="modal-container" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div>
          <div class="header-badge" style="display:inline-block; margin-bottom:6px;"><i class="fa-solid fa-building-circle-check"></i> EXPEDIENTE DE SEDE HyS</div>
          <h2 id="modal-title" style="font-size:18px; font-weight:700; line-height:1.2;">Nombre del Establecimiento</h2>
          <div id="modal-subtitle" style="font-size:12px; color:#A0B0A4; margin-top:4px;">Organismo | CUIT | Domicilio</div>
        </div>
        <button class="modal-close-btn" onclick="cerrarModalFicha()"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <div class="modal-body" id="modal-body-content">
        <!-- Renderizado dinámicamente -->
      </div>
      <div style="padding:16px 24px; background:#F8FAF8; border-top:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center;">
        <button class="action-btn" onclick="copiarFichaPortapapeles()"><i class="fa-solid fa-copy"></i> Copiar Ficha de la Sede</button>
        <button class="action-btn action-btn-primary" onclick="cerrarModalFicha()">Cerrar Ficha</button>
      </div>
    </div>
  </div>

  <!-- Scripts para Navegación, Gráficos, Casos y Sincronización en Vivo -->
  <script>
    function switchTab(tabId, btn) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      const targetPane = document.getElementById('tab-' + tabId);
      if (targetPane) targetPane.classList.add('active');
      
      if (btn) {
        btn.classList.add('active');
      } else {
        const matchingBtn = document.getElementById('btn-tab-' + tabId);
        if (matchingBtn) matchingBtn.classList.add('active');
      }

      setTimeout(() => { window.dispatchEvent(new Event('resize')); }, 50);
    }

    let dataMetrics = __DATA_JSON__;
    let dataCasos = __CASOS_JSON__;
    let activeKpiTag = 'todos';
    let casosPaginaActual = 1;
    let casosPageSize = 50;
    let casosFiltrados = [];
    let casoSeleccionadoModal = null;

    let chartHistInst = null;
    let chartNormInst = null;
    let chartOrgInst = null;
    let chartCronoInst = null;

    // Definición de las Etiquetas y Filtros KPI
    const KPI_CHIP_DEFINITIONS = [
      { id: 'todos', label: 'Todos los Activos', countKey: 'total_activos', icon: 'fa-table-list', color: '#1C241E' },
      { id: 'visitados', label: 'Stock Visitas Efectivas', countKey: 'visitados', icon: 'fa-check-double', color: 'var(--primary)' },
      { id: 'vencidas', label: 'Visitas Vencidas s/Realizar', countKey: 'vencidas_criticas', icon: 'fa-circle-exclamation', color: 'var(--alert)' },
      { id: 'urgentes_nov', label: 'Vencen en Noviembre 2026', countKey: 'urgentes_nov26', icon: 'fa-clock-rotate-left', color: 'var(--warn)' },
      { id: 'futuras', label: 'Cronograma Dic 26 - May 27', countKey: 'futuras_programadas', icon: 'fa-calendar-days', color: 'var(--info)' },
      { id: 'rgrl_si', label: 'Cumplimiento RGRL (Cargados)', countKey: 'rgrl_si', icon: 'fa-file-shield', color: 'var(--primary)' },
      { id: 'rgrl_vencidos', label: 'RGRL Vencidos Pendientes', countKey: 'rgrl_vencidos_pend', icon: 'fa-triangle-exclamation', color: 'var(--alert)' },
      { id: 'rar_si', label: 'Relevamiento RAR (Riesgos)', countKey: 'rar_si', icon: 'fa-triangle-exclamation', color: '#0284C7' },
      { id: 'svcc_si', label: 'Vigilancia SVCC (Cancerígenos)', countKey: 'svcc_si', icon: 'fa-biohazard', color: '#D97706' },
      { id: 'zona_fria', label: 'Sedes en Zona Fría (Total)', countKey: 'zona_fria_total', icon: 'fa-snowflake', color: '#0284C7' },
      { id: 'zona_fria_vis', label: 'Zona Fría: Visitadas', countKey: 'zona_fria_vis', icon: 'fa-snowflake', color: 'var(--primary)' },
      { id: 'zona_fria_pend', label: 'Zona Fría: Pendientes', countKey: 'zona_fria_pend', icon: 'fa-snowflake', color: 'var(--warn)' },
      { id: 'sin_preventor', label: 'Sin Preventor Asignado', countKey: 'sin_preventor', icon: 'fa-user-xmark', color: 'var(--alert)' }
    ];

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

    // ==================== LÓGICA DE LA VISTA DETALLADA DE CASOS ====================
    function initCasosView() {
      // 1. Renderizar chips de KPI
      const container = document.getElementById('kpi-chips-container');
      container.innerHTML = KPI_CHIP_DEFINITIONS.map(chip => {
        let count = 0;
        if (chip.id === 'todos') {
          count = dataMetrics.total_activos;
        } else if (chip.id === 'zona_fria_pend') {
          count = dataMetrics.zona_fria_total - dataMetrics.zona_fria_vis;
        } else if (dataMetrics[chip.countKey] !== undefined) {
          count = dataMetrics[chip.countKey];
        } else {
          count = dataCasos.filter(c => c.kpi_tags && c.kpi_tags.includes(chip.id)).length;
        }
        return `
          <button class="chip-btn ${chip.id === activeKpiTag ? 'active' : ''}" id="chip-${chip.id}" onclick="filtrarPorTag('${chip.id}')">
            <i class="fa-solid ${chip.icon}"></i> ${chip.label}
            <span class="chip-count">${count}</span>
          </button>
        `;
      }).join('');

      // 2. Llenar Select de Organismos
      const orgSelect = document.getElementById('casos-filter-org');
      const uniqueOrgs = [...new Set(dataCasos.map(c => c.organismo))].sort();
      orgSelect.innerHTML = '<option value="">Todos los Organismos (' + uniqueOrgs.length + ')</option>' +
        uniqueOrgs.map(o => `<option value="${o}">${o}</option>`).join('');

      // 3. Llenar Select de Preventores
      const prevSelect = document.getElementById('casos-filter-prev');
      const uniquePrevs = [...new Set(dataCasos.map(c => c.preventor).filter(Boolean))].sort();
      prevSelect.innerHTML = '<option value="">Todos los Preventores</option>' +
        '<option value="__SIN_PREV__">⚠️ Sin Preventor Asignado (' + dataMetrics.sin_preventor + ')</option>' +
        uniquePrevs.map(p => `<option value="${p}">${p}</option>`).join('');

      // 4. Llenar Select de Departamentos
      const deptoSelect = document.getElementById('casos-filter-depto');
      const uniqueDeptos = [...new Set(dataCasos.map(c => c.depto).filter(Boolean))].sort();
      deptoSelect.innerHTML = '<option value="">Todos los Departamentos (' + uniqueDeptos.length + ')</option>' +
        uniqueDeptos.map(d => `<option value="${d}">${d}</option>`).join('');

      // 5. Filtrar inicialmente
      filtrarCasos();
    }

    // Abre la vista de casos configurando un tag de KPI específico
    function abrirCasos(kpiTag) {
      const btn = document.getElementById('btn-tab-casos');
      switchTab('casos', btn);
      filtrarPorTag(kpiTag);
      window.scrollTo({ top: 100, behavior: 'smooth' });
    }

    function abrirCasosConFiltro(org, kpiTag) {
      const btn = document.getElementById('btn-tab-casos');
      switchTab('casos', btn);
      document.getElementById('casos-filter-org').value = org;
      filtrarPorTag(kpiTag || 'todos');
      window.scrollTo({ top: 100, behavior: 'smooth' });
    }

    function abrirCasosPorDepto(depto) {
      const btn = document.getElementById('btn-tab-casos');
      switchTab('casos', btn);
      document.getElementById('casos-filter-depto').value = depto;
      filtrarPorTag('todos');
      window.scrollTo({ top: 100, behavior: 'smooth' });
    }

    function abrirCasosPorPreventor(prev) {
      const btn = document.getElementById('btn-tab-casos');
      switchTab('casos', btn);
      document.getElementById('casos-filter-prev').value = prev;
      filtrarPorTag('todos');
      window.scrollTo({ top: 100, behavior: 'smooth' });
    }

    function filtrarPorTag(tag) {
      activeKpiTag = tag;
      document.querySelectorAll('.chip-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('chip-' + tag);
      if (activeBtn) activeBtn.classList.add('active');
      filtrarCasos(true);
    }

    function resetCasosFiltros() {
      activeKpiTag = 'todos';
      document.querySelectorAll('.chip-btn').forEach(btn => btn.classList.remove('active'));
      const todosBtn = document.getElementById('chip-todos');
      if (todosBtn) todosBtn.classList.add('active');
      document.getElementById('casos-search').value = '';
      document.getElementById('casos-filter-org').value = '';
      document.getElementById('casos-filter-prev').value = '';
      document.getElementById('casos-filter-depto').value = '';
      document.getElementById('casos-filter-zf').value = '';
      filtrarCasos(true);
    }

    function filtrarCasos(resetPagina = false) {
      if (resetPagina) casosPaginaActual = 1;

      const searchTerm = document.getElementById('casos-search').value.toLowerCase().trim();
      const selOrg = document.getElementById('casos-filter-org').value;
      const selPrev = document.getElementById('casos-filter-prev').value;
      const selDepto = document.getElementById('casos-filter-depto').value;
      const selZf = document.getElementById('casos-filter-zf').value;

      casosFiltrados = dataCasos.filter(caso => {
        // Filtro por KPI Tag
        if (activeKpiTag && activeKpiTag !== 'todos') {
          if (!caso.kpi_tags || !caso.kpi_tags.includes(activeKpiTag)) return false;
        }

        // Filtro por Organismo
        if (selOrg && caso.organismo !== selOrg) return false;

        // Filtro por Preventor
        if (selPrev) {
          if (selPrev === '__SIN_PREV__' && caso.preventor) return false;
          else if (selPrev !== '__SIN_PREV__' && caso.preventor !== selPrev) return false;
        }

        // Filtro por Departamento
        if (selDepto && caso.depto !== selDepto) return false;

        // Filtro por Zona Fría
        if (selZf) {
          if (selZf === 'si' && !caso.zona_fria) return false;
          if (selZf === 'no' && caso.zona_fria) return false;
        }

        // Filtro de Búsqueda Textual Cruzada
        if (searchTerm) {
          const hayMatch = (
            caso.nombre.toLowerCase().includes(searchTerm) ||
            caso.organismo.toLowerCase().includes(searchTerm) ||
            caso.domicilio.toLowerCase().includes(searchTerm) ||
            caso.depto.toLowerCase().includes(searchTerm) ||
            caso.preventor.toLowerCase().includes(searchTerm) ||
            caso.cuit.includes(searchTerm) ||
            caso.ref_nombre.toLowerCase().includes(searchTerm) ||
            caso.comentarios.toLowerCase().includes(searchTerm) ||
            caso.nro_srt.includes(searchTerm)
          );
          if (!hayMatch) return false;
        }

        return true;
      });

      // Actualizar Contadores
      document.getElementById('casos-count-filtered').innerText = casosFiltrados.length.toLocaleString('es-AR');
      document.getElementById('casos-count-total').innerText = dataCasos.length.toLocaleString('es-AR');
      
      const badgeElem = document.getElementById('casos-active-filter-badge');
      const chipDef = KPI_CHIP_DEFINITIONS.find(c => c.id === activeKpiTag);
      if (chipDef && chipDef.id !== 'todos') {
        badgeElem.style.display = 'inline-flex';
        badgeElem.innerHTML = `<i class="fa-solid ${chipDef.icon}"></i> ${chipDef.label}`;
      } else {
        badgeElem.style.display = 'none';
      }

      renderTablaCasos();
    }

    function renderTablaCasos() {
      const tbody = document.getElementById('tbody-casos');
      const total = casosFiltrados.length;

      if (total === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="11" style="text-align:center; padding:40px 20px; color:var(--text-muted);">
              <i class="fa-solid fa-folder-open" style="font-size:32px; color:#A0B0A4; margin-bottom:10px; display:block;"></i>
              <strong>No se encontraron establecimientos</strong> que coincidan con los filtros seleccionados.<br>
              <button class="action-btn" style="margin-top:12px;" onclick="resetCasosFiltros()">Limpiar filtros y ver todos</button>
            </td>
          </tr>`;
        renderPagination(0, 0, 0);
        return;
      }

      const limit = casosPageSize === 'all' ? total : parseInt(casosPageSize);
      const totalPages = Math.ceil(total / limit) || 1;
      if (casosPaginaActual > totalPages) casosPaginaActual = totalPages;

      const startIdx = (casosPaginaActual - 1) * limit;
      const endIdx = casosPageSize === 'all' ? total : Math.min(startIdx + limit, total);
      const paginaCasos = casosFiltrados.slice(startIdx, endIdx);

      tbody.innerHTML = paginaCasos.map((c, idx) => {
        const rowNum = startIdx + idx + 1;
        
        // Badge Estado Visita
        let visBadge = '';
        if (c.estado_visita === 'efectuada') {
          visBadge = `<span class="badge badge-success"><i class="fa-solid fa-check"></i> Efectuada ${c.f_vis || ''}</span>`;
        } else if (c.estado_visita === 'vencida') {
          visBadge = `<span class="badge badge-alert"><i class="fa-solid fa-triangle-exclamation"></i> Vencida ${c.f_vis_lim || ''}</span>`;
        } else if (c.estado_visita === 'urgente_nov') {
          visBadge = `<span class="badge badge-warn"><i class="fa-solid fa-clock"></i> Vence Nov/26 (${c.f_vis_lim})</span>`;
        } else {
          visBadge = `<span class="badge badge-info"><i class="fa-solid fa-calendar"></i> Prog: ${c.f_vis_lim || 'S/Fecha'}</span>`;
        }

        // RGRL
        let rgrlBadge = c.rgrl === 'SI' 
          ? `<span class="badge badge-success">SI</span>` 
          : (c.rgrl_vencido ? `<span class="badge badge-alert">VENCIDO</span>` : `<span class="badge badge-neutral">NO</span>`);

        // RAR
        let rarBadge = c.rar === 'SI' ? `<span class="badge badge-info">SI</span>` : `<span class="badge badge-neutral">NO</span>`;

        // SVCC
        let svccBadge = c.svcc === 'SI' ? `<span class="badge badge-warn"><i class="fa-solid fa-biohazard"></i> SI</span>` : `<span class="badge badge-neutral">NO</span>`;

        // Preventor
        let prevDisplay = c.preventor 
          ? `<span style="font-weight:600;"><i class="fa-solid fa-user-shield" style="color:var(--primary); font-size:11px; margin-right:4px;"></i>${c.preventor}</span>`
          : `<span class="badge badge-alert"><i class="fa-solid fa-user-xmark"></i> Sin Asignar</span>`;

        // Zona Fría tag
        const zfTag = c.zona_fria ? `<span class="badge badge-info" style="font-size:9px; padding:1px 5px; margin-left:4px;"><i class="fa-solid fa-snowflake"></i> Fría</span>` : '';

        // Contacto
        let contactHtml = '';
        if (c.ref_nombre) {
          contactHtml += `<div style="font-weight:600; font-size:12px;">${c.ref_nombre}</div>`;
        }
        if (c.ref_tel) {
          contactHtml += `<a href="tel:${c.ref_tel}" style="font-size:11px; color:var(--primary); text-decoration:none; display:inline-flex; align-items:center; gap:3px; margin-right:6px;"><i class="fa-solid fa-phone" style="font-size:9px;"></i>${c.ref_tel}</a>`;
        }
        if (c.ref_mail) {
          contactHtml += `<a href="mailto:${c.ref_mail}" style="font-size:11px; color:#2563EB; text-decoration:none; display:inline-flex; align-items:center; gap:3px;"><i class="fa-solid fa-envelope" style="font-size:9px;"></i>Mail</a>`;
        }
        if (!contactHtml) contactHtml = `<span style="color:#A0B0A4; font-size:11px;">Sin datos</span>`;

        return `
          <tr>
            <td class="num" style="color:var(--text-muted); font-size:11px;">${rowNum}</td>
            <td>
              <div class="estab-title">${c.nombre} ${zfTag}</div>
              <div class="estab-dom"><i class="fa-solid fa-location-dot" style="font-size:10px; color:#A0B0A4; margin-right:3px;"></i>${c.domicilio || 'Domicilio no consignado'}</div>
            </td>
            <td style="font-size:12px;"><strong>${c.organismo}</strong></td>
            <td style="font-size:12px;">${c.depto}</td>
            <td>${prevDisplay}</td>
            <td>${visBadge}</td>
            <td class="num">${rgrlBadge}</td>
            <td class="num">${rarBadge}</td>
            <td class="num">${svccBadge}</td>
            <td>${contactHtml}</td>
            <td style="text-align:center;">
              <button class="action-btn" style="padding:4px 8px; font-size:11px;" onclick="abrirModalFicha(${c.id})" title="Ver ficha técnica completa">
                <i class="fa-solid fa-eye" style="color:var(--primary);"></i> Ficha
              </button>
            </td>
          </tr>
        `;
      }).join('');

      renderPagination(startIdx + 1, endIdx, total);
    }

    function renderPagination(start, end, total) {
      const pagInfo = document.getElementById('pag-info');
      const pagBtns = document.getElementById('pag-buttons');

      if (total === 0) {
        pagInfo.innerText = '0 registros';
        pagBtns.innerHTML = '';
        return;
      }

      pagInfo.innerText = `Mostrando ${start} - ${end} de ${total.toLocaleString('es-AR')} casos`;

      if (casosPageSize === 'all') {
        pagBtns.innerHTML = '';
        return;
      }

      const limit = parseInt(casosPageSize);
      const totalPages = Math.ceil(total / limit) || 1;

      let html = '';
      html += `<button class="pag-btn" onclick="cambiarPagina(1)" ${casosPaginaActual === 1 ? 'disabled' : ''}><i class="fa-solid fa-angles-left"></i></button>`;
      html += `<button class="pag-btn" onclick="cambiarPagina(${casosPaginaActual - 1})" ${casosPaginaActual === 1 ? 'disabled' : ''}><i class="fa-solid fa-chevron-left"></i></button>`;

      let startP = Math.max(1, casosPaginaActual - 2);
      let endP = Math.min(totalPages, casosPaginaActual + 2);
      if (startP > 1) html += `<span style="padding:0 4px;">...</span>`;
      for (let p = startP; p <= endP; p++) {
        html += `<button class="pag-btn ${p === casosPaginaActual ? 'active' : ''}" onclick="cambiarPagina(${p})">${p}</button>`;
      }
      if (endP < totalPages) html += `<span style="padding:0 4px;">...</span>`;

      html += `<button class="pag-btn" onclick="cambiarPagina(${casosPaginaActual + 1})" ${casosPaginaActual === totalPages ? 'disabled' : ''}><i class="fa-solid fa-chevron-right"></i></button>`;
      html += `<button class="pag-btn" onclick="cambiarPagina(${totalPages})" ${casosPaginaActual === totalPages ? 'disabled' : ''}><i class="fa-solid fa-angles-right"></i></button>`;

      pagBtns.innerHTML = html;
    }

    function cambiarPagina(p) {
      casosPaginaActual = p;
      renderTablaCasos();
      document.querySelector('.casos-table').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function cambiarPageSize(val) {
      casosPageSize = val;
      casosPaginaActual = 1;
      renderTablaCasos();
    }

    // Modal de Ficha Técnica Individual
    function abrirModalFicha(id) {
      const caso = dataCasos.find(c => c.id === id);
      if (!caso) return;
      casoSeleccionadoModal = caso;

      document.getElementById('modal-title').innerText = caso.nombre;
      document.getElementById('modal-subtitle').innerHTML = `
        <strong>${caso.organismo}</strong> &nbsp;|&nbsp; CUIT: ${caso.cuit || 'S/D'} &nbsp;|&nbsp; Depto: ${caso.depto}
      `;

      let visStatusHtml = '';
      if (caso.estado_visita === 'efectuada') {
        visStatusHtml = `<span class="badge badge-success"><i class="fa-solid fa-check"></i> Efectuada: ${caso.f_vis}</span>`;
      } else if (caso.estado_visita === 'vencida') {
        visStatusHtml = `<span class="badge badge-alert"><i class="fa-solid fa-triangle-exclamation"></i> VENCIDA (Límite: ${caso.f_vis_lim})</span>`;
      } else if (caso.estado_visita === 'urgente_nov') {
        visStatusHtml = `<span class="badge badge-warn"><i class="fa-solid fa-clock"></i> Vence en Noviembre 2026 (${caso.f_vis_lim})</span>`;
      } else {
        visStatusHtml = `<span class="badge badge-info"><i class="fa-solid fa-calendar"></i> Programada: ${caso.f_vis_lim || 'Sin fecha asignada'}</span>`;
      }

      const body = document.getElementById('modal-body-content');
      body.innerHTML = `
        <div class="ficha-section-title"><i class="fa-solid fa-building"></i> Identificación del Establecimiento</div>
        <div class="ficha-grid">
          <div class="ficha-box">
            <div class="ficha-box-label">Razón Social</div>
            <div class="ficha-box-val">${caso.rs || 'PROVINCIA DEL NEUQUEN ADMINISTRACION CENTRAL'}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">CUIT Establecimiento</div>
            <div class="ficha-box-val" style="font-family:var(--font-mono);">${caso.cuit || '30999068940'}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Organismo Gubernamental</div>
            <div class="ficha-box-val">${caso.organismo}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">CUIT Organismo</div>
            <div class="ficha-box-val" style="font-family:var(--font-mono);">${caso.cuit_org || 'S/D'}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">N° Establecimiento SRT / ID Empresa</div>
            <div class="ficha-box-val" style="font-family:var(--font-mono);">${caso.nro_srt || '-'} / ${caso.id_empresa || '-'}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Código Anterior</div>
            <div class="ficha-box-val" style="font-family:var(--font-mono);">${caso.cod_ant || '-'}</div>
          </div>
        </div>

        <div class="ficha-section-title"><i class="fa-solid fa-map-location-dot"></i> Ubicación Geográfica & Zona</div>
        <div class="ficha-grid">
          <div class="ficha-box" style="grid-column: span 2;">
            <div class="ficha-box-label">Domicilio Completo</div>
            <div class="ficha-box-val">${caso.domicilio || 'No especificado en la planilla'}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Departamento Provincial</div>
            <div class="ficha-box-val">${caso.depto}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Zona Fría (Riesgo Climático)</div>
            <div class="ficha-box-val">
              ${caso.zona_fria ? '<span class="badge badge-info"><i class="fa-solid fa-snowflake"></i> SI (Zona Fría)</span>' : '<span class="badge badge-neutral">NO</span>'}
            </div>
          </div>
        </div>

        <div class="ficha-section-title"><i class="fa-solid fa-clipboard-check"></i> Estado de Inspección y Visita Técnica</div>
        <div class="ficha-grid">
          <div class="ficha-box">
            <div class="ficha-box-label">Estado Actual de Visita</div>
            <div class="ficha-box-val" style="margin-top:4px;">${visStatusHtml}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Fecha de Visita Realizada</div>
            <div class="ficha-box-val" style="font-family:var(--font-mono); color:var(--primary); font-weight:700;">
              ${caso.f_vis ? '<i class="fa-solid fa-calendar-check"></i> ' + caso.f_vis : '<span style="color:#A0B0A4;">Pendiente de realización</span>'}
            </div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Fecha Límite / Verosimilitud</div>
            <div class="ficha-box-val" style="font-family:var(--font-mono);">
              ${caso.f_vis_lim || 'Sin fecha límite registrada'}
            </div>
          </div>
        </div>

        <div class="ficha-section-title"><i class="fa-solid fa-shield-halved"></i> Relevamientos Normativos Obligatorios (SRT)</div>
        <div class="ficha-grid">
          <div class="ficha-box">
            <div class="ficha-box-label">RGRL (Res. SRT 463/09)</div>
            <div class="ficha-box-val">
              ${caso.rgrl === 'SI' ? '<span class="badge badge-success">Cargado SI</span>' : (caso.rgrl_vencido ? '<span class="badge badge-alert">VENCIDO PENDIENTE</span>' : '<span class="badge badge-neutral">PENDIENTE</span>')}
              <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">Carga: ${caso.f_rgrl_carga || 'S/D'} | Límite: ${caso.f_rgrl_lim || 'S/D'}</div>
            </div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">RAR (Relevamiento de Riesgos)</div>
            <div class="ficha-box-val">
              ${caso.rar === 'SI' ? '<span class="badge badge-info"><i class="fa-solid fa-triangle-exclamation"></i> Presentado SI</span>' : '<span class="badge badge-neutral">No presentado</span>'}
            </div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">SVCC (Cancerígenos)</div>
            <div class="ficha-box-val">
              ${caso.svcc === 'SI' ? '<span class="badge badge-warn"><i class="fa-solid fa-biohazard"></i> Registrado SI</span>' : '<span class="badge badge-neutral">No registra</span>'}
            </div>
          </div>
        </div>

        <div class="ficha-section-title"><i class="fa-solid fa-user-shield"></i> Asignación Técnica & Referente de Contacto</div>
        <div class="ficha-grid">
          <div class="ficha-box">
            <div class="ficha-box-label">Profesional Preventor Asignado</div>
            <div class="ficha-box-val">
              ${caso.preventor ? '<strong style="color:var(--primary);"><i class="fa-solid fa-user-check"></i> ' + caso.preventor + '</strong>' : '<span class="badge badge-alert"><i class="fa-solid fa-user-xmark"></i> SIN PREVENTOR ASIGNADO</span>'}
            </div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Nombre del Referente Institucional</div>
            <div class="ficha-box-val">${caso.ref_nombre || 'No registrado'}</div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Teléfono de Contacto</div>
            <div class="ficha-box-val">
              ${caso.ref_tel ? `<a href="tel:${caso.ref_tel}" style="color:var(--primary); text-decoration:none;"><i class="fa-solid fa-phone"></i> ${caso.ref_tel}</a>` : 'Sin teléfono'}
            </div>
          </div>
          <div class="ficha-box">
            <div class="ficha-box-label">Correo Electrónico</div>
            <div class="ficha-box-val">
              ${caso.ref_mail ? `<a href="mailto:${caso.ref_mail}" style="color:#2563EB; text-decoration:none;"><i class="fa-solid fa-envelope"></i> ${caso.ref_mail}</a>` : 'Sin correo'}
            </div>
          </div>
        </div>

        ${caso.comentarios ? `
        <div class="ficha-section-title"><i class="fa-solid fa-comment-dots"></i> Observaciones & Comentarios Registrados</div>
        <div class="ficha-box" style="background:#FFFBEB; border-color:#FDE68A; color:#78350F; font-size:13px;">
          ${caso.comentarios}
        </div>
        ` : ''}
      `;

      document.getElementById('modal-ficha').classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function cerrarModalFicha(event) {
      if (event && event.target !== document.getElementById('modal-ficha') && !event.target.closest('.modal-close-btn') && !event.target.classList.contains('action-btn-primary')) {
        return;
      }
      document.getElementById('modal-ficha').classList.remove('open');
      document.body.style.overflow = '';
      casoSeleccionadoModal = null;
    }

    function copiarFichaPortapapeles() {
      if (!casoSeleccionadoModal) return;
      const c = casoSeleccionadoModal;
      const txt = `FICHA TÉCNICA HYS — PLAN NEUQUÉN
Establecimiento: ${c.nombre}
Organismo: ${c.organismo}
CUIT: ${c.cuit} | CUIT Org: ${c.cuit_org}
Domicilio: ${c.domicilio} | Depto: ${c.depto}
Zona Fría: ${c.zona_fria ? 'SÍ' : 'NO'}
Preventor Asignado: ${c.preventor || 'SIN PREVENTOR'}
Estado Visita: ${c.estado_visita_label} (Fecha: ${c.f_vis || 'Pendiente'} | Límite: ${c.f_vis_lim || 'S/D'})
RGRL: ${c.rgrl} (Límite: ${c.f_rgrl_lim || 'S/D'}) | RAR: ${c.rar} | SVCC: ${c.svcc}
Referente: ${c.ref_nombre || 'S/D'} | Tel: ${c.ref_tel || 'S/D'} | Mail: ${c.ref_mail || 'S/D'}
N° SRT: ${c.nro_srt || '-'} | ID Empresa: ${c.id_empresa || '-'}
Observaciones: ${c.comentarios || 'Ninguna'}`;

      navigator.clipboard.writeText(txt).then(() => {
        alert('¡Datos de la sede copiados al portapapeles con éxito!');
      }).catch(err => {
        console.error('Error al copiar:', err);
      });
    }

    // Exportar Casos Filtrados a Excel (CSV con UTF-8 BOM)
    function exportarCasosCSV() {
      if (!casosFiltrados || casosFiltrados.length === 0) {
        alert('No hay registros filtrados para exportar.');
        return;
      }

      const headers = [
        'Nro', 'Establecimiento', 'Organismo', 'Departamento', 'Domicilio', 'Zona Fria',
        'Preventor', 'Estado Visita', 'Fecha Visita', 'Fecha Limite Visita',
        'RGRL', 'Fecha Carga RGRL', 'Fecha Limite RGRL', 'RGRL Vencido',
        'RAR', 'SVCC', 'Referente', 'Telefono Referente', 'Mail Referente',
        'Nro SRT', 'ID Empresa', 'Comentarios'
      ];

      const escapeCSV = (val) => {
        if (val === null || val === undefined) return '""';
        const str = String(val).replace(/"/g, '""');
        return `"${str}"`;
      };

      const rows = [headers.map(escapeCSV).join(';')];

      casosFiltrados.forEach((c, idx) => {
        const row = [
          idx + 1,
          c.nombre,
          c.organismo,
          c.depto,
          c.domicilio,
          c.zona_fria ? 'SI' : 'NO',
          c.preventor || 'SIN PREVENTOR',
          c.estado_visita_label,
          c.f_vis,
          c.f_vis_lim,
          c.rgrl,
          c.f_rgrl_carga,
          c.f_rgrl_lim,
          c.rgrl_vencido ? 'SI' : 'NO',
          c.rar,
          c.svcc,
          c.ref_nombre,
          c.ref_tel,
          c.ref_mail,
          c.nro_srt,
          c.id_empresa,
          c.comentarios
        ];
        rows.push(row.map(escapeCSV).join(';'));
      });

      const csvContent = '\uFEFF' + rows.join('\\r\\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      const fTag = activeKpiTag || 'todos';
      const fecha = new Date().toISOString().split('T')[0];
      link.setAttribute('href', url);
      link.setAttribute('download', `PLAN_NEUQUEN_Casos_${fTag}_${fecha}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // Sincronización en vivo con Google Sheets / data.json
    async function syncWithGoogleSheets() {
      const btn = document.getElementById('btn-sync');
      const syncText = document.getElementById('sync-text');
      btn.classList.add('loading');
      syncText.innerText = 'Sincronizando...';

      try {
        const resMetrics = await fetch('data/metrics_data.json?t=' + Date.now());
        if (resMetrics.ok) {
          dataMetrics = await resMetrics.json();
          updateDOM();
          renderCharts();
        }

        const resCasos = await fetch('data/casos_data.json?t=' + Date.now());
        if (resCasos.ok) {
          dataCasos = await resCasos.json();
          initCasosView();
        }

        syncText.innerHTML = '<i class="fa-solid fa-circle" style="color:#A3E635;font-size:9px;"></i> En vivo (Sheets)';
        btn.classList.remove('loading');
        return;
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
      initCasosView();
      // Verificación en segundo plano si hay nuevos datos
      setTimeout(syncWithGoogleSheets, 1000);
    });

    // Cierre modal con escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') cerrarModalFicha();
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
    '__DATA_JSON__': json.dumps(data, ensure_ascii=False),
    '__CASOS_JSON__': json.dumps(casos, ensure_ascii=False)
}

final_html = html_template
for k, v in replacements.items():
    final_html = final_html.replace(k, v)

# Save both index.html and PLAN_NEUQUEN.html
for fname in ['index.html', 'PLAN_NEUQUEN.html']:
    target = os.path.join(base_dir, fname)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Written: {target} ({len(final_html)} bytes)")
