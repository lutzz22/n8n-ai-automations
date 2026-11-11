"""Generate the fictional tariff samples used by workflow 02.

- samples/cuadro_tarifario_vigente.json : current production config (Resolution ER 98/2026)
- samples/resolucion_ER_123_2026.xlsx    : new regulator publication, +4.2% on every charge
- samples/resolucion_ER_124_2026_con_error.xlsx : same file with a typo (one value x10)

The regulator, resolutions and values are invented.
Usage: pip install openpyxl && python tools/make_tariff_samples.py
"""
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

OUT = Path(__file__).resolve().parent.parent / "02-tariff-excel-to-json" / "samples"
OUT.mkdir(parents=True, exist_ok=True)

# Current config: tariff -> charge -> subsidy level
CURRENT = {
    "T1-R1": {"fixed_charge": [1215.40, 1215.40, 1215.40], "variable_charge": [98.512, 61.334, 55.020]},
    "T1-R2": {"fixed_charge": [1830.75, 1830.75, 1830.75], "variable_charge": [101.207, 63.118, 56.441]},
    "T1-R3": {"fixed_charge": [4410.10, 4410.10, 4410.10], "variable_charge": [107.889, 70.502, 62.996]},
    "T1-G1": {"fixed_charge": [3120.00], "variable_charge": [118.730]},
    "T1-G2": {"fixed_charge": [9875.55], "variable_charge": [121.045]},
}
LEVELS = ["N1", "N2", "N3"]
LABELS = {  # how the regulator names each tariff in the Excel
    "T1-R1": "T1 - R1 Residencial (hasta 150 kWh/mes)",
    "T1-R2": "T1 - R2 Residencial (151 a 300 kWh/mes)",
    "T1-R3": "T1 - R3 Residencial (más de 300 kWh/mes)",
    "T1-G1": "T1 - G1 General (hasta 1.600 kWh/bim)",
    "T1-G2": "T1 - G2 General (1.601 a 4.000 kWh/bim)",
}

config = {
    "distributor": "VoltaSur Energía",
    "resolution": "ER 98/2026",
    "valid_from": "2026-10-01",
    "currency": "ARS",
    "units": {"fixed_charge": "ARS/mes", "variable_charge": "ARS/kWh"},
    "tariffs": {
        t: {c: {LEVELS[i]: v for i, v in enumerate(vals)} for c, vals in charges.items()}
        for t, charges in CURRENT.items()
    },
}
(OUT / "cuadro_tarifario_vigente.json").write_text(json.dumps(config, indent=2, ensure_ascii=False))

def excel(fname, resolution, valid_from, typo=False):
    wb = Workbook(); ws = wb.active; ws.title = "Cuadro Tarifario"
    ws["A1"] = f"ENTE REGULADOR ELÉCTRICO (ficticio) - Resolución {resolution}"
    ws["A2"] = f"Cuadro tarifario VoltaSur Energía - Vigencia {valid_from} - Valores sin impuestos"
    ws["A1"].font = Font(bold=True, size=13)
    headers = ["Tarifa", "Concepto", "Unidad", "Nivel 1 - Sin subsidio", "Nivel 2 - Menores ingresos", "Nivel 3 - Ingresos medios"]
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=4, column=i, value=h); c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True)
    r = 5
    for t, charges in CURRENT.items():
        first = True
        for charge, label, unit in [("fixed_charge", "Cargo Fijo", "$/mes"), ("variable_charge", "Cargo Variable", "$/kWh")]:
            ws.cell(row=r, column=1, value=LABELS[t] if first else None)  # merged-style: label only on first row
            ws.cell(row=r, column=2, value=label); ws.cell(row=r, column=3, value=unit)
            for i, v in enumerate(charges[charge]):
                nv = round(v * 1.042, 3 if charge == "variable_charge" else 2)
                if typo and t == "T1-G2" and charge == "variable_charge":
                    nv = round(nv * 10, 3)  # someone typed 1261.29 instead of 126.129
                ws.cell(row=r, column=4 + i, value=nv)
            first = False; r += 1
    ws.cell(row=r + 1, column=1, value="Nota: los usuarios de tarifas Generales no tienen niveles de subsidio.")
    for col, w in zip("ABCDEF", [42, 16, 9, 18, 22, 22]): ws.column_dimensions[col].width = w
    wb.save(OUT / fname)

excel("resolucion_ER_123_2026.xlsx", "ER 123/2026", "01/11/2026")
excel("resolucion_ER_124_2026_con_error.xlsx", "ER 124/2026", "01/12/2026", typo=True)
print("Samples written to", OUT)
