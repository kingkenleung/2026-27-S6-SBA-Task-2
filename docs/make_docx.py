#!/usr/bin/env python3
"""Convert STUDENT_INSTRUCTIONS.md into a formatted DOCX for Google Classroom."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Cm, Pt, RGBColor

BASE = Path(__file__).resolve().parent
SRC = BASE / "STUDENT_INSTRUCTIONS.md"
OUT = BASE / "STUDENT_INSTRUCTIONS.docx"
GITHUB_DOCS = "https://github.com/kingkenleung/2026-27-S6-SBA-Task-2/blob/main/docs/"

BLACK = RGBColor(0x00, 0x00, 0x00)
INK = RGBColor(0x1A, 0x1A, 0x1A)
GRAY = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

HEADER_FILL = "000000"
BAND_FILL = "F2F2F2"
SOFT_GRAY = "E6E6E6"
CALLOUT_FILL = "F2F2F2"
LIVE_FILL = "EDEDED"
BORDER = "BFBFBF"

# Content width on A4 with 1.7 cm margins: 21 - 3.4 = 17.6 cm.
WIDTHS = {
    2: [4.2, 13.4],
    3: [4.0, 6.4, 7.2],
    5: [1.2, 4.0, 4.2, 1.4, 6.8],
    8: [1.3, 2.3, 2.5, 2.5, 3.2, 2.5, 1.5, 1.8],
}

TOKEN_RE = re.compile(
    r"(`[^`]+`|\[[^\]]+\]\([^)]+\)|<https?://[^>]+>|https?://[^\s<]+|\*\*.+?\*\*|\*[^*\s][^*]*\*)"
)

doc = Document()
first_h1 = True
cover_mode = True
skip_next_hr = False

PPR_ORDER = [
    qn(tag)
    for tag in (
        "w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore",
        "w:framePr", "w:widowControl", "w:numPr", "w:suppressLineNumbers",
        "w:pBdr", "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku",
        "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE",
        "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
        "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
        "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
        "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
        "w:rPr", "w:sectPr", "w:pPrChange",
    )
]


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def insert_in_order(parent, element, order) -> None:
    index = order.index(element.tag)
    for child in parent:
        if child.tag in order and order.index(child.tag) > index:
            child.addprevious(element)
            return
    parent.append(element)


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def shade_paragraph(paragraph, fill: str) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    insert_in_order(p_pr, shd, PPR_ORDER)


def shade_run(run, fill: str) -> None:
    r_pr = run._r.get_or_add_rPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    r_pr.append(shd)


def set_paragraph_border(paragraph, side="bottom", color=BORDER, size=8, space=1) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        insert_in_order(p_pr, p_bdr, PPR_ORDER)
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    p_bdr.append(el)


def set_table_borders(table) -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), BORDER)
        borders.append(el)
    tbl_pr.append(borders)


def set_table_cell_margins(table) -> None:
    tbl_pr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side, width in (("top", 55), ("left", 85), ("bottom", 55), ("right", 85)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(width))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tbl_pr.append(mar)


def set_table_fixed_layout(table) -> None:
    tbl_pr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)


def cant_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    tr_pr.append(el)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    tr_pr.append(header)


def add_field(paragraph, instruction: str) -> None:
    begin_run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    begin_run._r.append(fld_begin)

    instr_run = paragraph.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    instr_run._r.append(instr)

    sep_run = paragraph.add_run()
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    sep_run._r.append(fld_sep)

    value_run = paragraph.add_run("1")

    end_run = paragraph.add_run()
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    end_run._r.append(fld_end)

    for run in (begin_run, instr_run, sep_run, value_run, end_run):
        run.font.size = Pt(8.5)
        run.font.color.rgb = GRAY


def add_hyperlink(paragraph, url: str, text: str, bold=False, italic=False, size=None, color=None) -> None:
    if not re.match(r"^(https?://|mailto:)", url):
        if url.endswith(".md"):
            url = GITHUB_DOCS + url
        else:
            add_run(paragraph, text, bold, italic, size, color or BLACK)
            return

    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), "Calibri")
    r_fonts.set(qn("w:hAnsi"), "Calibri")
    r_pr.append(r_fonts)
    if bold:
        r_pr.append(OxmlElement("w:b"))
    if italic:
        r_pr.append(OxmlElement("w:i"))
    c = OxmlElement("w:color")
    c.set(qn("w:val"), str(color or BLACK))
    r_pr.append(c)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int((size or 10.5) * 2)))
    r_pr.append(sz)
    sz_cs = OxmlElement("w:szCs")
    sz_cs.set(qn("w:val"), str(int((size or 10.5) * 2)))
    r_pr.append(sz_cs)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    r_pr.append(u)
    run.append(r_pr)

    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    run.append(t)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_run(paragraph, text: str, bold=False, italic=False, size=None, color=None, font=None):
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    if font:
        run.font.name = font
    return run


def add_inline(paragraph, text: str, bold=False, italic=False, size=None, color=None) -> None:
    pos = 0
    for match in TOKEN_RE.finditer(text):
        if match.start() > pos:
            add_run(paragraph, text[pos:match.start()], bold, italic, size, color)
        token = match.group(0)
        if token.startswith("`") and token.endswith("`"):
            run = add_run(
                paragraph,
                token[1:-1],
                bold,
                italic,
                (size or 10.5) - 1.5,
                BLACK,
                "Consolas",
            )
            shade_run(run, "F2F2F2")
        elif token.startswith("["):
            link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            if link:
                add_hyperlink(
                    paragraph,
                    link.group(2),
                    link.group(1).replace("`", ""),
                    bold,
                    italic,
                    size,
                    color,
                )
        elif token.startswith("<http"):
            url = token[1:-1]
            add_hyperlink(paragraph, url, url, bold, italic, size, color)
        elif token.startswith("http"):
            add_hyperlink(paragraph, token, token, bold, italic, size, color)
        elif token.startswith("**") and token.endswith("**"):
            add_inline(paragraph, token[2:-2], True, italic, size, color)
        elif token.startswith("*") and token.endswith("*"):
            add_inline(paragraph, token[1:-1], bold, True, size, color)
        pos = match.end()
    if pos < len(text):
        add_run(paragraph, text[pos:], bold, italic, size, color)


# ---------------------------------------------------------------------------
# Document setup
# ---------------------------------------------------------------------------

section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(1.7)
section.bottom_margin = Cm(1.7)
section.left_margin = Cm(1.7)
section.right_margin = Cm(1.7)
section.different_first_page_header_footer = True

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(3.5)
normal.paragraph_format.line_spacing = 1.08

for name, size, color, before, after in (
    ("Heading 1", 26, BLACK, 0, 4),
    ("Heading 2", 14.5, BLACK, 12, 4),
    ("Heading 3", 11.5, BLACK, 8, 2),
    ("Heading 4", 10.5, BLACK, 7, 2),
):
    style = doc.styles[name]
    style.font.name = "Calibri"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = color
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True

# Header (pages 2+)
header_p = section.header.paragraphs[0]
header_p.text = "S6 ICT SBA Task 2  Â·  CampusConnect"
header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
for run in header_p.runs:
    run.font.size = Pt(8.5)
    run.font.color.rgb = GRAY
set_paragraph_border(header_p, "bottom", "D9D9D9", 6, 2)

# Footer (pages 2+)
footer_p = section.footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer_p.paragraph_format.space_before = Pt(4)
add_run(footer_p, "Page ", size=8.5, color=GRAY)
add_field(footer_p, "PAGE")
add_run(footer_p, " of ", size=8.5, color=GRAY)
add_field(footer_p, "NUMPAGES")
set_paragraph_border(footer_p, "top", "D9D9D9", 6, 4)

# First-page header/footer are intentionally blank.
section.first_page_header.paragraphs[0].text = ""
section.first_page_footer.paragraphs[0].text = ""

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def add_body_paragraph(text: str) -> None:
    global cover_mode
    p = doc.add_paragraph()
    if cover_mode:
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(8)
        add_inline(p, text, size=10.5, color=GRAY)
    else:
        add_inline(p, text)


def add_heading(text: str, level: int) -> None:
    global first_h1
    if level == 1 and first_h1:
        eyebrow = doc.add_paragraph()
        eyebrow.paragraph_format.space_after = Pt(8)
        add_run(eyebrow, "S6 ICT  Â·  ELECTIVE B1", bold=True, size=10, color=BLACK)
        first_h1 = False

    p = doc.add_paragraph(style=f"Heading {level}")
    add_inline(p, text)
    if level == 1:
        p.paragraph_format.space_after = Pt(2)
        line = doc.add_paragraph()
        line.paragraph_format.space_before = Pt(0)
        line.paragraph_format.space_after = Pt(12)
        set_paragraph_border(line, "bottom", "000000", 14, 1)
    elif level == 2:
        set_paragraph_border(p, "bottom", "D9D9D9", 8, 2)


def add_bullet(text: str, level: int) -> None:
    style = "List Bullet"
    if level == 1:
        style = "List Bullet 2"
    elif level >= 2:
        style = "List Bullet 3"
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.08
    add_inline(p, text)


def add_numbered(number: str, text: str, level: int) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.85 + level * 0.5)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.08
    add_run(p, f"{number}. ", bold=True, color=BLACK)
    add_inline(p, text)


def add_quote_block(lines: list[str]) -> None:
    groups: list[list[str]] = [[]]
    for line in lines:
        if line.strip() == "":
            if groups[-1]:
                groups.append([])
        else:
            groups[-1].append(line.strip())
    groups = [g for g in groups if g]
    for index, group in enumerate(groups):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.45)
        p.paragraph_format.right_indent = Cm(0.15)
        p.paragraph_format.space_before = Pt(6 if index == 0 else 0)
        p.paragraph_format.space_after = Pt(8 if index == len(groups) - 1 else 2)
        p.paragraph_format.line_spacing = 1.1
        add_inline(p, " ".join(group))
        shade_paragraph(p, CALLOUT_FILL)
        set_paragraph_border(p, "left", "000000", 18, 6)


def add_hr() -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(9)
    set_paragraph_border(p, "bottom", "DDE5F0", 6, 1)


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def add_table(block: list[str]) -> bool:
    global cover_mode
    raw_rows = [line for line in block if not is_separator(line)]
    rows = [split_row(line) for line in raw_rows]
    if not rows:
        return False

    metadata = all(cell == "" for cell in rows[0])
    if metadata:
        header = None
        data = rows[1:]
    else:
        header = rows[0]
        data = rows[1:]

    cols = max(len(row) for row in rows)
    for row in rows:
        while len(row) < cols:
            row.append("")

    if metadata:
        table = doc.add_table(rows=len(data), cols=2)
    else:
        table = doc.add_table(rows=1 + len(data), cols=cols)

    table.style = "Light Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    if cols in WIDTHS:
        table.autofit = False
        for index, width in enumerate(WIDTHS[cols]):
            table.columns[index].width = Cm(width)
    else:
        table.autofit = True

    font_size = 9.5 if metadata else (8.5 if cols >= 5 else 9)

    if metadata:
        for row_index, row in enumerate(data):
            cant_split(table.rows[row_index])
            cells = table.rows[row_index].cells
            is_live = row[0].strip() == "Live app"
            for col_index in range(2):
                cell = cells[col_index]
                if is_live:
                    set_cell_shading(cell, LIVE_FILL)
                elif col_index == 0:
                    set_cell_shading(cell, SOFT_GRAY)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.line_spacing = 1.0
                if col_index == 0:
                    add_inline(p, row[col_index], bold=True, size=font_size, color=BLACK)
                else:
                    add_inline(p, row[col_index], size=13 if is_live else font_size)
    else:
        cant_split(table.rows[0])
        header_cells = table.rows[0].cells
        for col_index in range(cols):
            cell = header_cells[col_index]
            set_cell_shading(cell, HEADER_FILL)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            add_inline(p, header[col_index], bold=True, size=font_size, color=WHITE)
        repeat_header(table.rows[0])

        for row_index, row in enumerate(data):
            cant_split(table.rows[row_index + 1])
            cells = table.rows[row_index + 1].cells
            for col_index in range(cols):
                cell = cells[col_index]
                if row_index % 2 == 1:
                    set_cell_shading(cell, BAND_FILL)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.line_spacing = 1.0
                add_inline(p, row[col_index], size=font_size)

    if metadata:
        cover_mode = False
        doc.add_page_break()
        return True
    return False


def add_code_block(code: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.05
    run = add_run(p, code, size=8.5, color=INK, font="Consolas")
    shade_run(run, "F2F2F2")
    set_paragraph_border(p, "left", "BFBFBF", 12, 4)


# ---------------------------------------------------------------------------
# Parse the Markdown
# ---------------------------------------------------------------------------

lines = SRC.read_text(encoding="utf-8").splitlines()
buffer: list[str] = []
i = 0

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if stripped == "":
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        i += 1
        continue

    if stripped.startswith("```"):
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        i += 1
        code_lines = []
        while i < len(lines) and not lines[i].strip().startswith("```"):
            code_lines.append(lines[i])
            i += 1
        i += 1
        add_code_block("\n".join(code_lines))
        continue

    heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if heading:
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        add_heading(heading.group(2).strip(), len(heading.group(1)))
        i += 1
        continue

    if stripped == "---":
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        if skip_next_hr:
            skip_next_hr = False
        else:
            add_hr()
        i += 1
        continue

    if stripped.startswith("|"):
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        block = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            block.append(lines[i].strip())
            i += 1
        if add_table(block):
            skip_next_hr = True
        continue

    if stripped.startswith(">"):
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        block = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            block.append(lines[i].strip()[1:])
            i += 1
        add_quote_block(block)
        continue

    bullet = re.match(r"^(\s*)-\s+(.*)$", line)
    if bullet:
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        add_bullet(bullet.group(2).strip(), len(bullet.group(1)) // 2)
        i += 1
        continue

    numbered = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
    if numbered:
        if buffer:
            add_body_paragraph(" ".join(part.strip() for part in buffer))
            buffer = []
        add_numbered(numbered.group(2), numbered.group(3).strip(), len(numbered.group(1)) // 2)
        i += 1
        continue

    buffer.append(stripped)
    i += 1

if buffer:
    add_body_paragraph(" ".join(part.strip() for part in buffer))

# Document metadata
doc.core_properties.title = "S6 ICT SBA Task 2 â€” CampusConnect"
doc.core_properties.subject = "Testing and Evaluation"
doc.core_properties.author = "S6 ICT"
doc.core_properties.comments = "Student brief for the CampusConnect testing task."

doc.save(OUT)
print(f"Wrote {OUT}")

