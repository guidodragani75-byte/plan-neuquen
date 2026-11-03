import urllib.request
import csv
import io
import json
import os
from datetime import datetime

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1kxkrqu1bqtADiMKyNOP5uib-5Wv_-dNEmDngJCAJAHk/export?format=csv&gid=192789465"
SHEET_GVIZ_URL = "https://docs.google.com/spreadsheets/d/1kxkrqu1bqtADiMKyNOP5uib-5Wv_-dNEmDngJCAJAHk/gviz/tq?tqx=out:csv&gid=192789465"

def fetch_csv():
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in [SHEET_CSV_URL, SHEET_GVIZ_URL]:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                text = resp.read().decode('utf-8', errors='replace')
                if len(text) > 1000:
                    print(f"Downloaded CSV from {url} ({len(text)} bytes)")
                    return text
        except Exception as e:
            print(f"Failed to fetch from {url}: {e}")
    raise RuntimeError("Could not download CSV from any Google Sheets endpoint.")

def parse_and_compute(csv_text):
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    
    # Locate header row: has RS and ORGANISMO
    header_idx = -1
    for i, r in enumerate(rows[:10]):
        r_str = " ".join(r)
        if "ORGANISMO" in r_str and ("RS" in r_str or "NOMBRE_ESTAB" in r_str):
            header_idx = i
            break
            
    if header_idx == -1:
        # Fallback to row 5 or 0
        header_idx = 5 if len(rows) > 5 else 0
        
    data_rows = rows[header_idx + 1:]
    today = datetime.now()

    # Column mapping indices based on standard layout
    # 0: RS, 1: CUIT, 2: ORGANISMO, 3: CUIT_ORG, 4: NOMBRE_ESTAB, 5: ESTADO
    # 8: RGRL, 14: RAR, 18: SVCC, 23: DEPARTAMENTO, 27: Zona fría
    # 29: Fecha límite RGRL, 30: Fecha límite Visita, 31: Preventor
    # 32: Referente, 33: Mail, 34: Teléfono, 35: Fecha Visita, 39: Comentarios
    
    total_padron = len(data_rows)
    activos = []
    bajas = []
    
    for r in data_rows:
        if len(r) < 6:
            continue
        estado = r[5].strip().title() if len(r) > 5 else 'Activo'
        if estado == 'Baja':
            bajas.append(r)
        else:
            activos.append(r)
            
    total_activos = len(activos)
    total_bajas = len(bajas)
    
    def parse_date(d_str):
        if not d_str or not d_str.strip():
            return None
        d_str = d_str.strip().split()[0]
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%m/%d/%y'):
            try:
                return datetime.strptime(d_str, fmt)
            except ValueError:
                pass
        return None

    visitados = 0
    vencidas_criticas = 0
    urgentes_nov26 = 0
    futuras_programadas = 0
    rgrl_si = 0
    rgrl_vencidos_pend = 0
    rar_si = 0
    svcc_si = 0
    zona_fria_total = 0
    zona_fria_vis = 0
    prev_asignados = 0
    has_ref = 0
    has_mail = 0
    has_tel = 0
    
    hist_visits = {}
    future_deadlines = {}
    orgs_map = {}
    prev_map = {}
    dept_map = {}
    
    for r in activos:
        org = r[2].strip() if len(r) > 2 and r[2].strip() else 'SIN ORGANISMO'
        rgrl = r[8].strip().upper() if len(r) > 8 else 'NO'
        rar = r[14].strip().upper() if len(r) > 14 else 'NO'
        svcc = r[18].strip().upper() if len(r) > 18 else 'NO'
        dept = r[23].strip().upper() if len(r) > 23 and r[23].strip() else 'SIN DEPARTAMENTO'
        zf = r[27].strip().lower() if len(r) > 27 else ''
        f_rgrl_lim = parse_date(r[29]) if len(r) > 29 else None
        f_vis_lim = parse_date(r[30]) if len(r) > 30 else None
        preventor = r[31].strip().upper() if len(r) > 31 else ''
        if preventor in ('NAN', 'NONE'):
            preventor = ''
        ref_n = r[32].strip() if len(r) > 32 else ''
        ref_m = r[33].strip() if len(r) > 33 else ''
        ref_t = r[34].strip() if len(r) > 34 else ''
        f_vis = parse_date(r[35]) if len(r) > 35 else None
        
        has_visit = (f_vis is not None) or (len(r) > 35 and bool(r[35].strip()))
        if has_visit:
            visitados += 1
            if f_vis:
                k = f_vis.strftime('%Y-%m')
                hist_visits[k] = hist_visits.get(k, 0) + 1
        else:
            if f_vis_lim:
                if f_vis_lim < today:
                    vencidas_criticas += 1
                elif f_vis_lim.year == today.year and f_vis_lim.month == today.month:
                    urgentes_nov26 += 1
                elif f_vis_lim > today:
                    futuras_programadas += 1
                    k = f_vis_lim.strftime('%Y-%m')
                    future_deadlines[k] = future_deadlines.get(k, 0) + 1
            else:
                futuras_programadas += 1
                
        if rgrl == 'SI':
            rgrl_si += 1
        elif f_rgrl_lim and f_rgrl_lim < today:
            rgrl_vencidos_pend += 1
            
        if rar == 'SI':
            rar_si += 1
        if svcc == 'SI':
            svcc_si += 1
            
        if zf == 'si':
            zona_fria_total += 1
            if has_visit:
                zona_fria_vis += 1
                
        if preventor:
            prev_asignados += 1
            if preventor not in prev_map:
                prev_map[preventor] = {'asignados': 0, 'visitados': 0}
            prev_map[preventor]['asignados'] += 1
            if has_visit:
                prev_map[preventor]['visitados'] += 1
                
        if ref_n and ref_n.lower() != 'nan': has_ref += 1
        if ref_m and ref_m.lower() != 'nan': has_mail += 1
        if ref_t and ref_t.lower() != 'nan': has_tel += 1
        
        # Org Map
        if org not in orgs_map:
            orgs_map[org] = {'total': 0, 'visitados': 0, 'vencidas': 0, 'urg_nov': 0, 'rgrl': 0, 'rar': 0}
        orgs_map[org]['total'] += 1
        if has_visit: orgs_map[org]['visitados'] += 1
        else:
            if f_vis_lim and f_vis_lim < today: orgs_map[org]['vencidas'] += 1
            elif f_vis_lim and f_vis_lim.year == today.year and f_vis_lim.month == today.month: orgs_map[org]['urg_nov'] += 1
        if rgrl == 'SI': orgs_map[org]['rgrl'] += 1
        if rar == 'SI': orgs_map[org]['rar'] += 1
        
        # Dept Map
        if dept not in dept_map:
            dept_map[dept] = {'total': 0, 'visitados': 0}
        dept_map[dept]['total'] += 1
        if has_visit: dept_map[dept]['visitados'] += 1

    # Format outputs
    org_list = []
    for org, v in orgs_map.items():
        tot = v['total']
        vis = v['visitados']
        org_list.append({
            'organismo': org,
            'total': tot,
            'visitados': vis,
            'pendientes': tot - vis,
            'pct_avance': round(vis / tot * 100, 1) if tot else 0,
            'vencidas': v['vencidas'],
            'urgentes_nov': v['urg_nov'],
            'rgrl_pct': round(v['rgrl'] / tot * 100, 1) if tot else 0,
            'rar_pct': round(v['rar'] / tot * 100, 1) if tot else 0
        })
    org_list.sort(key=lambda x: x['total'], reverse=True)
    
    prev_list = []
    for p, v in prev_map.items():
        tot = v['asignados']
        vis = v['visitados']
        prev_list.append({
            'preventor': p,
            'asignados': tot,
            'visitados': vis,
            'pendientes': tot - vis,
            'pct_completado': round(vis / tot * 100, 1) if tot else 0
        })
    prev_list.sort(key=lambda x: x['asignados'], reverse=True)
    
    dept_list = []
    for d, v in dept_map.items():
        tot = v['total']
        vis = v['visitados']
        dept_list.append({
            'departamento': d,
            'total': tot,
            'visitados': vis,
            'pendientes': tot - vis,
            'pct_avance': round(vis / tot * 100, 1) if tot else 0
        })
    dept_list.sort(key=lambda x: x['total'], reverse=True)

    sorted_hist = sorted(hist_visits.items())
    sorted_crono = sorted(future_deadlines.items())

    metrics = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_padron': total_padron,
        'total_activos': total_activos,
        'total_bajas': total_bajas,
        'visitados': visitados,
        'pendientes': total_activos - visitados,
        'pct_avance': round(visitados / total_activos * 100, 1) if total_activos else 0,
        'vencidas_criticas': vencidas_criticas,
        'urgentes_nov26': urgentes_nov26,
        'futuras_programadas': futuras_programadas,
        'rgrl_si': rgrl_si,
        'rgrl_pct': round(rgrl_si / total_activos * 100, 1) if total_activos else 0,
        'rgrl_vencidos_pend': rgrl_vencidos_pend,
        'rar_si': rar_si,
        'rar_pct': round(rar_si / total_activos * 100, 1) if total_activos else 0,
        'total_expuestos': 15472,
        'svcc_si': svcc_si,
        'svcc_pct': round(svcc_si / total_activos * 100, 1) if total_activos else 0,
        'zona_fria_total': zona_fria_total,
        'zona_fria_vis': zona_fria_vis,
        'zona_fria_pct': round(zona_fria_vis / zona_fria_total * 100, 1) if zona_fria_total else 0,
        'sin_preventor': total_activos - prev_asignados,
        'prev_asignados': prev_asignados,
        'has_ref': has_ref,
        'has_mail': has_mail,
        'has_tel': has_tel,
        'hist_labels': [k for k, _ in sorted_hist],
        'hist_values': [v for _, v in sorted_hist],
        'crono_labels': [k for k, _ in sorted_crono],
        'crono_values': [v for _, v in sorted_crono],
        'organismos': org_list,
        'preventores': prev_list,
        'departamentos': dept_list
    }
    return metrics

def main():
    print(f"[{datetime.now()}] Updating metrics from Google Sheets...")
    csv_text = fetch_csv()
    metrics = parse_and_compute(csv_text)
    
    # Save to data/metrics_data.json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, 'metrics_data.json')
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"Saved metrics data to {json_path}")
    print(f"Metrics update complete: {metrics['visitados']}/{metrics['total_activos']} visitados ({metrics['pct_avance']}%)")

if __name__ == '__main__':
    main()
