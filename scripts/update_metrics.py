import urllib.request
import csv
import io
import json
import os
from datetime import datetime

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1kxkrqu1bqtADiMKyNOP5uib-5Wv_-dNEmDngJCAJAHk/export?format=csv&gid=192789465"
SHEET_GVIZ_URL = "https://docs.google.com/spreadsheets/d/1kxkrqu1bqtADiMKyNOP5uib-5Wv_-dNEmDngJCAJAHk/gviz/tq?tqx=out:csv&gid=192789465"

def clean_txt(t):
    if not t:
        return ''
    t = str(t).replace('\ufffd', '°').replace('\xa0', ' ').strip()
    return t

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
        header_idx = 5 if len(rows) > 5 else 0
        
    data_rows = rows[header_idx + 1:]
    today = datetime.now()

    # Column mapping indices based on standard layout
    # 0: RS, 1: CUIT, 2: ORGANISMO, 3: CUIT_ORG, 4: NOMBRE_ESTAB, 5: ESTADO
    # 6: COD_ESTAB ANTERIORES, 7: DOMICILIO, 8: RGRL, 9: FECHA CARGA RGRL, 10: FECHA ENVIO SRT
    # 14: RAR, 18: SVCC, 23: DEPARTAMENTO, 27: Zona fría
    # 29: Fecha límite RGRL, 30: Fecha límite Visita, 31: Preventor
    # 32: Referente, 33: Mail, 34: Teléfono, 35: Fecha Visita, 36: Nro SRT, 37: ID Empresa, 39: Comentarios
    
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
    casos = []
    
    for idx, r in enumerate(activos, 1):
        org = clean_txt(r[2]) if len(r) > 2 and clean_txt(r[2]) else 'SIN ORGANISMO'
        rgrl = clean_txt(r[8]).upper() if len(r) > 8 else 'NO'
        rar = clean_txt(r[14]).upper() if len(r) > 14 else 'NO'
        svcc = clean_txt(r[18]).upper() if len(r) > 18 else 'NO'
        dept = clean_txt(r[23]).upper() if len(r) > 23 and clean_txt(r[23]) else 'SIN DEPARTAMENTO'
        zf = clean_txt(r[27]).lower() if len(r) > 27 else ''
        f_rgrl_lim = parse_date(r[29]) if len(r) > 29 else None
        f_vis_lim = parse_date(r[30]) if len(r) > 30 else None
        preventor = clean_txt(r[31]).upper() if len(r) > 31 else ''
        if preventor in ('NAN', 'NONE', 'SIN PREVENTOR'):
            preventor = ''
        ref_n = clean_txt(r[32]) if len(r) > 32 else ''
        ref_m = clean_txt(r[33]) if len(r) > 33 else ''
        ref_t = clean_txt(r[34]) if len(r) > 34 else ''
        f_vis = parse_date(r[35]) if len(r) > 35 else None
        
        has_visit = (f_vis is not None) or (len(r) > 35 and bool(r[35].strip()))
        
        # Tags for interactive drill-down views
        kpi_tags = []
        estado_visita = 'sin_fecha'
        estado_visita_label = 'Sin programar'

        if has_visit:
            visitados += 1
            kpi_tags.append('visitados')
            estado_visita = 'efectuada'
            f_vis_str = f_vis.strftime('%d/%m/%Y') if f_vis else clean_txt(r[35])
            estado_visita_label = f'Efectuada: {f_vis_str}'
            if f_vis:
                k = f_vis.strftime('%Y-%m')
                hist_visits[k] = hist_visits.get(k, 0) + 1
        else:
            if f_vis_lim:
                if f_vis_lim < today:
                    vencidas_criticas += 1
                    kpi_tags.append('vencidas')
                    estado_visita = 'vencida'
                    dias = (today - f_vis_lim).days
                    estado_visita_label = f'Vencida: {f_vis_lim.strftime("%d/%m/%Y")} ({dias}d)'
                elif f_vis_lim.year == today.year and f_vis_lim.month == today.month:
                    urgentes_nov26 += 1
                    kpi_tags.append('urgentes_nov')
                    estado_visita = 'urgente_nov'
                    estado_visita_label = f'Vence Nov/26: {f_vis_lim.strftime("%d/%m/%Y")}'
                elif f_vis_lim > today:
                    futuras_programadas += 1
                    kpi_tags.append('futuras')
                    estado_visita = 'programada'
                    estado_visita_label = f'Prog: {f_vis_lim.strftime("%d/%m/%Y")}'
                    k = f_vis_lim.strftime('%Y-%m')
                    future_deadlines[k] = future_deadlines.get(k, 0) + 1
            else:
                futuras_programadas += 1
                kpi_tags.append('futuras')
                estado_visita = 'programada'
                estado_visita_label = 'Programada (Sin fecha fijada)'
                
        is_rgrl_venc = False
        if rgrl == 'SI':
            rgrl_si += 1
            kpi_tags.append('rgrl_si')
        elif f_rgrl_lim and f_rgrl_lim < today:
            rgrl_vencidos_pend += 1
            kpi_tags.append('rgrl_vencidos')
            is_rgrl_venc = True
            
        if rar == 'SI':
            rar_si += 1
            kpi_tags.append('rar_si')
        if svcc == 'SI':
            svcc_si += 1
            kpi_tags.append('svcc_si')
            
        is_zf = (zf == 'si')
        if is_zf:
            zona_fria_total += 1
            kpi_tags.append('zona_fria')
            if has_visit:
                zona_fria_vis += 1
                kpi_tags.append('zona_fria_vis')
            else:
                kpi_tags.append('zona_fria_pend')
                
        if preventor:
            prev_asignados += 1
            kpi_tags.append('prev_asignados')
            if preventor not in prev_map:
                prev_map[preventor] = {'asignados': 0, 'visitados': 0}
            prev_map[preventor]['asignados'] += 1
            if has_visit:
                prev_map[preventor]['visitados'] += 1
        else:
            kpi_tags.append('sin_preventor')
                
        if ref_n and ref_n.lower() != 'nan':
            has_ref += 1
        else:
            ref_n = ''
        if ref_m and ref_m.lower() != 'nan':
            has_mail += 1
        else:
            ref_m = ''
        if ref_t and ref_t.lower() != 'nan':
            has_tel += 1
        else:
            ref_t = ''
        
        # Org Map
        if org not in orgs_map:
            orgs_map[org] = {'total': 0, 'visitados': 0, 'vencidas': 0, 'urg_nov': 0, 'rgrl': 0, 'rar': 0}
        orgs_map[org]['total'] += 1
        if has_visit:
            orgs_map[org]['visitados'] += 1
        else:
            if f_vis_lim and f_vis_lim < today:
                orgs_map[org]['vencidas'] += 1
            elif f_vis_lim and f_vis_lim.year == today.year and f_vis_lim.month == today.month:
                orgs_map[org]['urg_nov'] += 1
        if rgrl == 'SI':
            orgs_map[org]['rgrl'] += 1
        if rar == 'SI':
            orgs_map[org]['rar'] += 1
        
        # Dept Map
        if dept not in dept_map:
            dept_map[dept] = {'total': 0, 'visitados': 0}
        dept_map[dept]['total'] += 1
        if has_visit:
            dept_map[dept]['visitados'] += 1

        # Build individual case object
        caso = {
            'id': idx,
            'rs': clean_txt(r[0]) if len(r) > 0 else '',
            'cuit': clean_txt(r[1]) if len(r) > 1 else '',
            'organismo': org,
            'cuit_org': clean_txt(r[3]) if len(r) > 3 else '',
            'nombre': clean_txt(r[4]) if len(r) > 4 else '',
            'estado': clean_txt(r[5]) if len(r) > 5 else 'Activo',
            'cod_ant': clean_txt(r[6]) if len(r) > 6 else '',
            'domicilio': clean_txt(r[7]) if len(r) > 7 else '',
            'rgrl': rgrl,
            'f_rgrl_carga': clean_txt(r[9]) if len(r) > 9 else '',
            'f_rgrl_lim': f_rgrl_lim.strftime('%d/%m/%Y') if f_rgrl_lim else '',
            'rgrl_vencido': is_rgrl_venc,
            'rar': rar,
            'svcc': svcc,
            'depto': dept,
            'zona_fria': is_zf,
            'f_vis_lim': f_vis_lim.strftime('%d/%m/%Y') if f_vis_lim else '',
            'f_vis': f_vis.strftime('%d/%m/%Y') if f_vis else (clean_txt(r[35]) if has_visit else ''),
            'preventor': preventor,
            'ref_nombre': ref_n,
            'ref_mail': ref_m,
            'ref_tel': ref_t,
            'nro_srt': clean_txt(r[36]) if len(r) > 36 else '',
            'id_empresa': clean_txt(r[37]) if len(r) > 37 else '',
            'comentarios': clean_txt(r[39]) if len(r) > 39 else '',
            'estado_visita': estado_visita,
            'estado_visita_label': estado_visita_label,
            'kpi_tags': kpi_tags
        }
        casos.append(caso)

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
    return metrics, casos

def main():
    print(f"[{datetime.now()}] Updating metrics & casos from Google Sheets...")
    csv_text = fetch_csv()
    metrics, casos = parse_and_compute(csv_text)
    
    # Save to data/metrics_data.json and data/casos_data.json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    metrics_path = os.path.join(data_dir, 'metrics_data.json')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"Saved metrics data to {metrics_path}")
    
    casos_path = os.path.join(data_dir, 'casos_data.json')
    with open(casos_path, 'w', encoding='utf-8') as f:
        json.dump(casos, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(casos)} casos to {casos_path}")
    
    print(f"Metrics update complete: {metrics['visitados']}/{metrics['total_activos']} visitados ({metrics['pct_avance']}%)")

if __name__ == '__main__':
    main()
