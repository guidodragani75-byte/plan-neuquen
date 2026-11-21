import urllib.request
import csv
import io
from collections import defaultdict

url = 'https://docs.google.com/spreadsheets/d/1kxkrqu1bqtADiMKyNOP5uib-5Wv_-dNEmDngJCAJAHk/export?format=csv&gid=192789465'
data = urllib.request.urlopen(url).read().decode('utf-8', errors='replace')
rows = list(csv.reader(io.StringIO(data)))[6:]

muestras = [str(i) for i in range(11)]
meses_headers = [
    '01/07/2026', '01/08/2026', '01/09/2026', '01/10/2026', '01/11/2026',
    '01/12/2026', '01/01/2027', '01/02/2027', '01/03/2027', '01/04/2027', '01/05/2027'
]

print("==========================================================================================")
print("TABLA 1: CONTROL POR MUESTRA DE PLANIFICACIÓN (F, AC, AJ, AK, AN)")
print("==========================================================================================")

table1 = []
for m in muestras:
    r_m = [r for r in rows if len(r) > 28 and r[28].strip() == m]
    tot_plan = len(r_m)
    bajas = [r for r in r_m if len(r) > 5 and r[5].strip().title() == 'Baja']
    cant_bajas = len(bajas)
    activos = tot_plan - cant_bajas
    
    # Visitas realizadas
    con_visita = [r for r in r_m if len(r) > 35 and r[35].strip() != '' and r[35].strip().upper() != 'BAJA']
    
    # Fallidas según columna AN (o comentarios)
    fallidas = [r for r in r_m if len(r) > 39 and 'FALLIDA' in r[39].strip().upper()]
    cant_fallidas = len(fallidas)
    
    # Efectivas: visitados con fecha de visita AJ y sin fallida en AN
    # Nota: si un registro tiene fecha de visita pero AN=='Fallida', es una visita fallida
    efectivas = [r for r in con_visita if not (len(r) > 39 and 'FALLIDA' in r[39].strip().upper())]
    cant_efectivas = len(efectivas)
    
    # Pendientes de visita efectiva: activos - efectivas
    pendientes = activos - cant_efectivas
    
    table1.append({
        'muestra': f'Muestra {m}',
        'mes_plan': meses_headers[int(m)],
        'objetivo_min': 150 if int(m) <= 9 else 99,
        'plan': tot_plan,
        'activos': activos,
        'visitados_efectivos': cant_efectivas,
        'fallidas': cant_fallidas,
        'pendientes': pendientes,
        'bajas': cant_bajas,
        'pct_avance': (cant_efectivas / activos * 100) if activos > 0 else 0
    })

# Format print Table 1
headers = ["Muestra", "Mes Plan", "Obj Min", "Planif.", "Bajas", "Activos", "Efectivas", "Fallidas", "Pendientes", "% Avance"]
print(f"{headers[0]:<11} | {headers[1]:<10} | {headers[2]:<7} | {headers[3]:<7} | {headers[4]:<5} | {headers[5]:<7} | {headers[6]:<9} | {headers[7]:<8} | {headers[8]:<10} | {headers[9]:<8}")
print("-" * 100)
for r in table1:
    print(f"{r['muestra']:<11} | {r['mes_plan']:<10} | {r['objetivo_min']:<7} | {r['plan']:<7} | {r['bajas']:<5} | {r['activos']:<7} | {r['visitados_efectivos']:<9} | {r['fallidas']:<8} | {r['pendientes']:<10} | {r['pct_avance']:>6.1f}%")

print("-" * 100)
t_plan = sum(r['plan'] for r in table1)
t_bajas = sum(r['bajas'] for r in table1)
t_activos = sum(r['activos'] for r in table1)
t_efect = sum(r['visitados_efectivos'] for r in table1)
t_fall = sum(r['fallidas'] for r in table1)
t_pend = sum(r['pendientes'] for r in table1)
t_pct = (t_efect / t_activos * 100) if t_activos > 0 else 0
print(f"{'TOTALES':<11} | {'-':<10} | {1500:<7} | {t_plan:<7} | {t_bajas:<5} | {t_activos:<7} | {t_efect:<9} | {t_fall:<8} | {t_pend:<10} | {t_pct:>6.1f}%")

# Bajas sin muestra
bajas_sin_muestra = len([r for r in rows if (len(r) <= 28 or r[28].strip() not in muestras) and (len(r) > 5 and r[5].strip().title() == 'Baja')])
print(f"\n* Nota: Existen adicionalmente {bajas_sin_muestra} establecimientos de baja históricos/preexistentes sin muestra asignada en SIMP (Total Bajas Padrón = {t_bajas + bajas_sin_muestra}).")

print("\n==========================================================================================")
print("TABLA 2: MATRIZ DE DOBLE ENTRADA (MUESTRA 'AC' vs MES DE VISITA 'AQ')")
print("==========================================================================================")

meses_visita = ['01/07/2026', '01/08/2026', '01/09/2026', '01/10/2026', '01/11/2026']

mat_total = defaultdict(lambda: defaultdict(int))
mat_efect = defaultdict(lambda: defaultdict(int))
mat_fall = defaultdict(lambda: defaultdict(int))

for r in rows:
    m = r[28].strip() if len(r) > 28 else ''
    mv = r[42].strip() if len(r) > 42 else ''
    an = r[39].strip().title() if len(r) > 39 else ''
    if m in muestras and mv:
        mat_total[m][mv] += 1
        if 'Fallida' in an:
            mat_fall[m][mv] += 1
        else:
            mat_efect[m][mv] += 1

print(f"{'Muestra':<11} | " + " | ".join(f"{mv:<10}" for mv in meses_visita) + " | Total Visitas | Efectivas | Fallidas")
print("-" * 100)
for m in muestras:
    row_strs = []
    tot_row = 0
    ef_row = 0
    fa_row = 0
    for mv in meses_visita:
        tot = mat_total[m][mv]
        ef = mat_efect[m][mv]
        fa = mat_fall[m][mv]
        tot_row += tot
        ef_row += ef
        fa_row += fa
        if tot > 0:
            if fa > 0:
                row_strs.append(f"{tot:>3} ({ef}+{fa}f)")
            else:
                row_strs.append(f"{tot:>10}")
        else:
            row_strs.append(f"{'-':>10}")
    print(f"Muestra {m:<3} | " + " | ".join(row_strs) + f" | {tot_row:>13} | {ef_row:>9} | {fa_row:>8}")

print("-" * 100)
# Totales por columna de mes de visita
tot_cols = []
for mv in meses_visita:
    tot_c = sum(mat_total[m][mv] for m in muestras)
    ef_c = sum(mat_efect[m][mv] for m in muestras)
    fa_c = sum(mat_fall[m][mv] for m in muestras)
    if fa_c > 0:
        tot_cols.append(f"{tot_c:>3} ({ef_c}+{fa_c}f)")
    else:
        tot_cols.append(f"{tot_c:>10}")

tot_general = sum(mat_total[m][mv] for m in muestras for mv in meses_visita)
tot_efect_gen = sum(mat_efect[m][mv] for m in muestras for mv in meses_visita)
tot_fall_gen = sum(mat_fall[m][mv] for m in muestras for mv in meses_visita)

print(f"{'TOTAL REAL':<11} | " + " | ".join(tot_cols) + f" | {tot_general:>13} | {tot_efect_gen:>9} | {tot_fall_gen:>8}")
