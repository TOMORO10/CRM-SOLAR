import csv
import json
import re

def clean_money(val_str):
    if not val_str: return 0
    # format could be "$427,180.00" or "1542015"
    if '.' in val_str:
        val_str = val_str.split('.')[0]
    s = re.sub(r'[^\d]', '', val_str)
    return int(s) if s else 0

data = []
# Explicitly use utf-8 or try/fallback based on what is in file (sometimes Windows CSVs are ISO-8859-1 or latin1 but user prompt says UTF-8)
try:
    with open('BENEFICIARIOS_ESTADOS - 500_Reg_base_datos_final_con_estado2.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_val = row.get('ID_Solicitud', '')
            nombre = f"{row.get('Nombre', '')} {row.get('Apellido', '')}".strip()
            cedula = row.get('Cedula', '')
            negocio = row.get('Negocio', '')
            nic = row.get('NIC', '')
            dept = row.get('Departamento', '')
            ciudad = row.get('Ciudad', '')
            dir_val = row.get('Direccion', '')
            e2 = row.get('ESTADO 2', '')
            ei = row.get('Estado_Interno', '')
            impl = row.get('Implementador', '')
            
            val_str = row.get('Valor_Factura', '0')
            val = clean_money(val_str)
            pot = str(row.get('Potencia_Q45', ''))
            
            m_col = row.get('MAYOR A $400K', '')
            m400 = (m_col == '1' or val > 400000)
            notas = row.get('Observaciones', '')
            email = row.get('Email', '')
            tel_key = next((k for k in row.keys() if k and k.startswith('Tel')), None)
            telefono = row.get(tel_key, '') if tel_key else ''
            
            obj = {
                "id": int(id_val) if id_val.isdigit() else id_val,
                "nombre": nombre,
                "cedula": cedula,
                "negocio": negocio,
                "nic": nic,
                "dept": dept,
                "ciudad": ciudad,
                "dir": dir_val,
                "e2": e2,
                "ei": ei,
                "impl": impl,
                "val": val,
                "pot": pot,
                "m400": m400,
                "email": email,
                "tel": telefono,
                "seg": "",
                "prox": "",
                "notas": notas
            }
            data.append(obj)
except UnicodeDecodeError:
    with open('BENEFICIARIOS_ESTADOS - 500_Reg_base_datos_final_con_estado2.csv', encoding='latin1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_val = row.get('ID_Solicitud', '')
            nombre = f"{row.get('Nombre', '')} {row.get('Apellido', '')}".strip()
            cedula = row.get('Cedula', '')
            negocio = row.get('Negocio', '')
            nic = row.get('NIC', '')
            dept = row.get('Departamento', '')
            ciudad = row.get('Ciudad', '')
            dir_val = row.get('Direccion', '')
            e2 = row.get('ESTADO 2', '')
            ei = row.get('Estado_Interno', '')
            impl = row.get('Implementador', '')
            
            val_str = row.get('Valor_Factura', '0')
            val = clean_money(val_str)
            pot = str(row.get('Potencia_Q45', ''))
            
            m_col = row.get('MAYOR A $400K', '')
            m400 = (m_col == '1' or val > 400000)
            notas = row.get('Observaciones', '')
            email = row.get('Email', '')
            tel_key = next((k for k in row.keys() if k and k.startswith('Tel')), None)
            telefono = row.get(tel_key, '') if tel_key else ''
            
            obj = {
                "id": int(id_val) if id_val.isdigit() else id_val,
                "nombre": nombre,
                "cedula": cedula,
                "negocio": negocio,
                "nic": nic,
                "dept": dept,
                "ciudad": ciudad,
                "dir": dir_val,
                "e2": e2,
                "ei": ei,
                "impl": impl,
                "val": val,
                "pot": pot,
                "m400": m400,
                "email": email,
                "tel": telefono,
                "seg": "",
                "prox": "",
                "notas": notas
            }
            data.append(obj)

js_data = "var D = " + json.dumps(data) + ";"

with open('fenoge_crm.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace between "var D = [" and the state config section
# The marker should be exact to what's in the file
end_marker = r"        // =====================================================================\n        // ESTADO GLOBAL Y CONFIGURACION"
start_marker = r"var D = \["

# using re.sub with cautious pattern
pattern = re.compile(start_marker + r".*?" + end_marker, re.DOTALL)
new_html = pattern.sub(lambda m: js_data + "\n\n" + end_marker.replace('\\n', '\n'), html)

with open('fenoge_crm.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Data replaced successfully! Embedded {len(data)} records.")
