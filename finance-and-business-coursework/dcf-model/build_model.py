"""Строит DCF-модель на 5 компаний: Допущения -> DCF -> Данные -> Сводная."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BLUE = Font(name="Arial", size=10, color="0000FF")          # вводные данные
BLACK = Font(name="Arial", size=10, color="000000")         # формулы
GREEN = Font(name="Arial", size=10, color="008000")         # ссылки на др. листы
BOLD = Font(name="Arial", size=10, bold=True)
TITLE = Font(name="Arial", size=13, bold=True)
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HDR_FILL = PatternFill("solid", fgColor="2F5496")
SUB_FILL = PatternFill("solid", fgColor="D9E1F2")
center = Alignment(horizontal="center")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)

RUB = '#,##0;(#,##0);-'
PCT = '0.0%'

companies = [
    # name, sector, base_rev, growth, ebit_m, tax, da, capex, nwc, wacc, term_g
    ("ТехноПлюс",       "IT",          1200, 0.18, 0.22, 0.20, 0.04, 0.06, 0.10, 0.15, 0.04),
    ("ДатаСофт",        "IT",           800, 0.22, 0.20, 0.20, 0.03, 0.05, 0.09, 0.16, 0.04),
    ("РозницаМаркет",   "Ритейл",      8500, 0.08, 0.06, 0.20, 0.03, 0.04, 0.08, 0.12, 0.03),
    ("НефтеГазИнвест",  "Энергетика", 15000, 0.05, 0.25, 0.20, 0.08, 0.12, 0.05, 0.13, 0.02),
    ("МедФарм",         "Фарма",       2100, 0.12, 0.18, 0.20, 0.04, 0.05, 0.09, 0.13, 0.035),
]

wb = Workbook()

# ============================================================
# Лист 1: Допущения
# ============================================================
a = wb.active
a.title = "Допущения"
a["A1"] = "Допущения DCF-модели (суммы в млн руб.)"
a["A1"].font = TITLE

headers = ["Компания", "Сектор", "Базовая выручка", "Рост выручки",
           "Маржа EBIT", "Налог", "D&A, % выручки", "Capex, % выручки",
           "ΔОбор. капитал, % прироста", "WACC", "Темп роста (g)"]
for j, h in enumerate(headers, start=1):
    c = a.cell(row=3, column=j, value=h)
    c.font = HDR; c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center", wrap_text=True, vertical="center")
    c.border = box

for i, comp in enumerate(companies):
    r = 4 + i
    vals = comp
    a.cell(row=r, column=1, value=vals[0]).font = BOLD
    a.cell(row=r, column=2, value=vals[1]).font = BLACK
    for j, v in enumerate(vals[2:], start=3):   # вводные -> синие
        cell = a.cell(row=r, column=j, value=v)
        cell.font = BLUE
        cell.number_format = RUB if j == 3 else PCT
    for j in range(1, 12):
        a.cell(row=r, column=j).border = box

widths = [16, 12, 14, 12, 11, 9, 13, 14, 16, 9, 13]
for j, w in enumerate(widths, start=1):
    a.column_dimensions[get_column_letter(j)].width = w
a.cell(row=4+len(companies)+1, column=1,
       value="Синим выделены вводные параметры (их можно менять для сценариев).").font = Font(italic=True, size=9, color="808080")

# ============================================================
# Лист 2: DCF
# ============================================================
d = wb.create_sheet("DCF")
d["A1"] = "DCF-оценка по компаниям (млн руб.)"
d["A1"].font = TITLE
d.column_dimensions["A"].width = 2
d.column_dimensions["B"].width = 30
for col in "CDEFGH":
    d.column_dimensions[col].width = 12

BLOCK = 18
rows_label = ["Год", "Выручка", "EBIT", "NOPAT (EBIT × (1−налог))",
              "D&A (+)", "Capex (−)", "Δ Оборотный капитал (−)", "FCF",
              "Коэффициент дисконтирования", "PV (приведённый FCF)"]

ev_cells = []  # для сводной: (name, sector, 'DCF'!Cell EV)

for i, comp in enumerate(companies):
    arow = 4 + i
    base = 3 + i * BLOCK
    yrs = base + 1
    rev, ebit, nopat, da, capex, nwc, fcf, df, pv = (base+2, base+3, base+4,
                                                     base+5, base+6, base+7,
                                                     base+8, base+9, base+10)
    tv, pvtv, sumpv, ev = base+12, base+13, base+14, base+15
    A = "'Допущения'!"

    # заголовок блока
    d.cell(row=base, column=2, value=f"{comp[0]}  ({comp[1]})").font = Font(name="Arial", bold=True, size=11)
    d.merge_cells(start_row=base, start_column=2, end_row=base, end_column=8)
    for j in range(2, 9):
        d.cell(row=base, column=j).fill = SUB_FILL

    # строка годов: B="Год", C=0 ... H=5
    d.cell(row=yrs, column=2, value="Год").font = BOLD
    for k in range(0, 6):
        cc = d.cell(row=yrs, column=3 + k, value=k)
        cc.font = BOLD; cc.alignment = center
    # подписи строк
    labels = ["Выручка", "EBIT", "NOPAT (EBIT × (1−налог))", "D&A (+)",
              "Capex (−)", "Δ Оборотный капитал (−)", "FCF",
              "Коэффициент дисконтирования", "PV (приведённый FCF)"]
    for off, lab in enumerate(labels):
        d.cell(row=rev + off, column=2, value=lab).font = BLACK

    # Выручка: C = база (ссылка), D..H = рост
    d.cell(row=rev, column=3, value=f"={A}$C${arow}").font = GREEN
    d.cell(row=rev, column=3).number_format = RUB
    for col in range(4, 9):  # D..H
        L, P = get_column_letter(col), get_column_letter(col-1)
        cell = d.cell(row=rev, column=col, value=f"={P}{rev}*(1+{A}$D${arow})")
        cell.font = BLACK; cell.number_format = RUB

    # строки, считаемые только для лет 1..5 (D..H)
    for col in range(4, 9):
        L = get_column_letter(col)
        Lprev = get_column_letter(col - 1)
        # EBIT
        d.cell(row=ebit, column=col, value=f"={L}{rev}*{A}$E${arow}")
        # NOPAT
        d.cell(row=nopat, column=col, value=f"={L}{ebit}*(1-{A}$F${arow})")
        # D&A
        d.cell(row=da, column=col, value=f"={L}{rev}*{A}$G${arow}")
        # Capex
        d.cell(row=capex, column=col, value=f"={L}{rev}*{A}$H${arow}")
        # ΔNWC = (выручка_t - выручка_{t-1}) * %
        d.cell(row=nwc, column=col, value=f"=({L}{rev}-{Lprev}{rev})*{A}$I${arow}")
        # FCF
        d.cell(row=fcf, column=col, value=f"={L}{nopat}+{L}{da}-{L}{capex}-{L}{nwc}")
        # коэф. дисконтирования = 1/(1+WACC)^год
        d.cell(row=df, column=col, value=f"=1/(1+{A}$J${arow})^{L}${yrs}")
        # PV
        d.cell(row=pv, column=col, value=f"={L}{fcf}*{L}{df}")
        for rr, fmt in [(ebit, RUB), (nopat, RUB), (da, RUB), (capex, RUB),
                        (nwc, RUB), (fcf, RUB), (df, '0.000'), (pv, RUB)]:
            d.cell(row=rr, column=col).number_format = fmt
            d.cell(row=rr, column=col).font = BLACK

    # Терминальная стоимость (в столбце H) = FCF5*(1+g)/(WACC-g)
    d.cell(row=tv, column=2, value="Терминальная стоимость (TV)").font = BLACK
    d.cell(row=tv, column=8,
           value=f"=H{fcf}*(1+{A}$K${arow})/({A}$J${arow}-{A}$K${arow})")
    d.cell(row=tv, column=8).number_format = RUB
    # PV терминальной стоимости = TV * коэф.дисконт. 5-го года
    d.cell(row=pvtv, column=2, value="PV терминальной стоимости").font = BLACK
    d.cell(row=pvtv, column=8, value=f"=H{tv}*H{df}")
    d.cell(row=pvtv, column=8).number_format = RUB
    # Сумма PV прогнозных FCF
    d.cell(row=sumpv, column=2, value="Сумма PV прогнозных FCF").font = BLACK
    d.cell(row=sumpv, column=3, value=f"=SUM(D{pv}:H{pv})")
    d.cell(row=sumpv, column=3).number_format = RUB
    # Стоимость бизнеса (EV)
    d.cell(row=ev, column=2, value="Стоимость бизнеса (EV)").font = BOLD
    evc = d.cell(row=ev, column=3, value=f"=C{sumpv}+H{pvtv}")
    evc.font = Font(name="Arial", bold=True, size=10)
    evc.number_format = RUB
    evc.fill = PatternFill("solid", fgColor="FFF2CC")
    ev_cells.append((comp[0], comp[1], f"C{ev}", fcf))

# ============================================================
# Лист 3: Данные (плоская таблица для сводной)  FCF по компаниям/годам
# ============================================================
dat = wb.create_sheet("Данные")
dat["A1"] = "Денежные потоки (FCF) по компаниям и годам — источник для сводной"
dat["A1"].font = TITLE
for j, h in enumerate(["Сектор", "Компания", "Год", "FCF"], start=1):
    c = dat.cell(row=3, column=j, value=h)
    c.font = HDR; c.fill = HDR_FILL; c.border = box; c.alignment = center
dat.column_dimensions["A"].width = 14
dat.column_dimensions["B"].width = 16
dat.column_dimensions["C"].width = 8
dat.column_dimensions["D"].width = 12

row = 4
for name, sector, evcell, fcf_row in ev_cells:
    for k, col in enumerate(range(4, 9), start=1):  # годы 1..5, столбцы D..H
        L = get_column_letter(col)
        dat.cell(row=row, column=1, value=sector).font = BLACK
        dat.cell(row=row, column=2, value=name).font = BLACK
        dat.cell(row=row, column=3, value=k).font = BLACK
        fc = dat.cell(row=row, column=4, value=f"=DCF!{L}{fcf_row}")
        fc.font = GREEN; fc.number_format = RUB
        for j in range(1, 5):
            dat.cell(row=row, column=j).border = box
        row += 1
last_data_row = row - 1

# ============================================================
# Лист 4: Сводная (pivot через SUMIFS): Сектор × Год = сумма FCF
# ============================================================
p = wb.create_sheet("Сводная")
p["A1"] = "Сводная таблица: суммарный FCF по секторам и годам (млн руб.)"
p["A1"].font = TITLE
sectors = []
for _, sec, _, _ in ev_cells:
    if sec not in sectors:
        sectors.append(sec)

# шапка
p.cell(row=3, column=1, value="Сектор").font = HDR
p.cell(row=3, column=1).fill = HDR_FILL; p.cell(row=3, column=1).border = box
for k in range(1, 6):
    c = p.cell(row=3, column=1 + k, value=f"Год {k}")
    c.font = HDR; c.fill = HDR_FILL; c.alignment = center; c.border = box
tot = p.cell(row=3, column=7, value="Итого")
tot.font = HDR; tot.fill = HDR_FILL; tot.alignment = center; tot.border = box

DATA = "Данные!"
for i, sec in enumerate(sectors):
    r = 4 + i
    p.cell(row=r, column=1, value=sec).font = BOLD
    p.cell(row=r, column=1).border = box
    for k in range(1, 6):
        col = 1 + k
        cell = p.cell(row=r, column=col,
                      value=f'=SUMIFS({DATA}$D$4:$D${last_data_row},'
                            f'{DATA}$A$4:$A${last_data_row},$A{r},'
                            f'{DATA}$C$4:$C${last_data_row},{k})')
        cell.number_format = RUB; cell.font = BLACK; cell.border = box
    # итог по строке
    tc = p.cell(row=r, column=7, value=f"=SUM(B{r}:F{r})")
    tc.font = BOLD; tc.number_format = RUB; tc.border = box

# нижняя строка итогов
rtot = 4 + len(sectors)
p.cell(row=rtot, column=1, value="Итого").font = BOLD
p.cell(row=rtot, column=1).fill = SUB_FILL; p.cell(row=rtot, column=1).border = box
for col in range(2, 8):
    L = get_column_letter(col)
    c = p.cell(row=rtot, column=col, value=f"=SUM({L}4:{L}{rtot-1})")
    c.font = BOLD; c.number_format = RUB; c.fill = SUB_FILL; c.border = box

p.column_dimensions["A"].width = 14
for col in "BCDEFG":
    p.column_dimensions[col].width = 11

# --- вторая таблица: EV по компаниям и доля ---
sr = rtot + 3
p.cell(row=sr, column=1, value="Стоимость бизнеса (EV) по компаниям").font = TITLE
for j, h in enumerate(["Компания", "Сектор", "EV", "Доля"], start=1):
    c = p.cell(row=sr+1, column=j, value=h)
    c.font = HDR; c.fill = HDR_FILL; c.border = box; c.alignment = center
for i, (name, sec, evcell, _) in enumerate(ev_cells):
    r = sr + 2 + i
    p.cell(row=r, column=1, value=name).font = BLACK
    p.cell(row=r, column=2, value=sec).font = BLACK
    ec = p.cell(row=r, column=3, value=f"=DCF!{evcell}")
    ec.font = GREEN; ec.number_format = RUB
    for j in range(1, 5):
        p.cell(row=r, column=j).border = box
ev_first = sr + 2
ev_last = sr + 1 + len(ev_cells)
ev_tot_row = ev_last + 1
p.cell(row=ev_tot_row, column=1, value="Итого").font = BOLD
p.cell(row=ev_tot_row, column=1).fill = SUB_FILL
tev = p.cell(row=ev_tot_row, column=3, value=f"=SUM(C{ev_first}:C{ev_last})")
tev.font = BOLD; tev.number_format = RUB; tev.fill = SUB_FILL
for i in range(len(ev_cells)):
    r = ev_first + i
    sh = p.cell(row=r, column=4, value=f"=C{r}/$C${ev_tot_row}")
    sh.number_format = PCT; sh.font = BLACK
for j in range(1,5):
    p.cell(row=ev_tot_row, column=j).border = box; p.cell(row=ev_tot_row, column=j).fill = SUB_FILL

wb.save("dcf_model.xlsx")
print("saved, last_data_row =", last_data_row)
