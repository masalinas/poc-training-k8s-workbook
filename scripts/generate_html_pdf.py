#!/usr/bin/env python3
# =============================================================================
# scripts/generate_html_pdf.py
# Generador del Cuaderno de Ejercicios y Solucionario de Kubernetes
# Compila HTML5 profesional a PDF con marcadores del panel lateral vía pypdf.
# =============================================================================
import os
import sys
import shutil
import subprocess
import re

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(WORKSPACE_DIR, "docs")
HTML_PATH = os.path.join(DOCS_DIR, "k8s-exercises-workbook.html")
PDF_PATH = os.path.join(WORKSPACE_DIR, "k8s-exercises-workbook.pdf")

# Importar contenido estructurado si existe
try:
    from content_data import MODULES, SUMMARY_TEXT, METADATA
except ImportError:
    # Soporte para ejecutar directamente desde workspace o scripts/
    sys.path.insert(0, os.path.dirname(__file__))
    from content_data import MODULES, SUMMARY_TEXT, METADATA

CSS_STYLES = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

@page {
  size: A4 portrait;
  margin: 18mm 14mm 18mm 14mm;
  @bottom-right {
    content: "Página " counter(page);
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    color: #64748b;
  }
  @bottom-left {
    content: "Curso Kubernetes - Cuaderno de Ejercicios y Solucionario";
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    color: #64748b;
  }
}

* {
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 9.5pt;
  line-height: 1.55;
  color: #1e293b;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
}

/* Portada */
.cover {
  page-break-after: always;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 88vh;
  padding: 40px 20px;
}

.badge-k8s {
  display: inline-block;
  align-self: flex-start;
  background-color: #e0f2fe;
  color: #0369a1;
  font-weight: 700;
  font-size: 8.5pt;
  padding: 6px 14px;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 24px;
}

.cover h1 {
  font-size: 26pt;
  font-weight: 800;
  line-height: 1.15;
  color: #0f172a;
  margin: 0 0 16px 0;
}

.cover h1 span {
  color: #326ce5; /* K8s Blue */
}

.cover .subtitle {
  font-size: 13pt;
  font-weight: 400;
  color: #475569;
  margin-bottom: 35px;
  line-height: 1.45;
}

.cover-meta {
  border-top: 2px solid #e2e8f0;
  padding-top: 20px;
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.meta-item {
  font-size: 9pt;
}

.meta-label {
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  font-size: 7.5pt;
  letter-spacing: 0.05em;
}

.meta-val {
  color: #0f172a;
  font-weight: 600;
  margin-top: 2px;
}

/* Encabezados y Banners */
.section-banner {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
  color: #ffffff;
  padding: 16px 20px;
  border-radius: 8px;
  margin-top: 24px;
  margin-bottom: 20px;
  page-break-before: always;
  break-before: page;
  page-break-inside: avoid !important;
  break-inside: avoid !important;
  page-break-after: avoid !important;
  break-after: avoid !important;
}

.section-banner-first {
  page-break-before: auto !important;
  break-before: auto !important;
  margin-top: 10px;
}

.section-banner h2 {
  color: #ffffff;
  border: none;
  padding: 0;
  margin: 0;
  font-size: 16pt;
  font-weight: 700;
  page-break-inside: avoid;
  break-inside: avoid;
}

.section-banner p {
  color: #93c5fd;
  margin: 6px 0 0 0;
  font-size: 8.5pt;
  page-break-inside: avoid;
  break-inside: avoid;
}

.module-header {
  border-bottom: 2px solid #326ce5;
  padding-bottom: 6px;
  margin-top: 28px;
  margin-bottom: 16px;
  page-break-after: avoid;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.module-header h3 {
  font-size: 13pt;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.module-namespace {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  background-color: #f1f5f9;
  color: #0369a1;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid #cbd5e1;
}

/* Tarjetas de Ejercicios y Soluciones */
.card-exercise {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 22px;
  page-break-inside: avoid;
}

.card-exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 8px;
}

.card-exercise-title {
  font-size: 10.5pt;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.difficulty-badge {
  font-size: 7.5pt;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 9999px;
  letter-spacing: 0.04em;
}

.diff-intermedio {
  background-color: #dbeafe;
  color: #1d4ed8;
}

.diff-avanzado {
  background-color: #fef3c7;
  color: #b45309;
}

.diff-cka {
  background-color: #fee2e2;
  color: #b91c1c;
}

/* Enlaces y Navegación Cruzada */
.btn-nav {
  display: inline-block;
  background-color: #326ce5;
  color: #ffffff !important;
  text-decoration: none;
  font-weight: 600;
  font-size: 8pt;
  padding: 5px 12px;
  border-radius: 4px;
  margin-top: 10px;
  transition: background-color 0.2s;
}

.btn-nav-return {
  background-color: #475569;
}

.btn-nav:hover {
  background-color: #1d4ed8;
}

/* Bloques de Código */
pre {
  background-color: #0f172a;
  color: #f8fafc;
  font-family: 'JetBrains Mono', monospace;
  font-size: 7.8pt;
  line-height: 1.45;
  padding: 10px 12px;
  border-radius: 6px;
  border-left: 4px solid #326ce5;
  margin-top: 6px;
  margin-bottom: 12px;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
  overflow: visible !important;
  overflow-x: visible !important;
  font-variant-ligatures: none !important;
  font-feature-settings: "liga" 0, "calt" 0 !important;
  page-break-inside: avoid;
  tab-size: 2;
  -moz-tab-size: 2;
}

code {
  font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
  font-size: 8.5pt;
  background-color: #f1f5f9;
  color: #0f172a;
  padding: 2px 4px;
  border-radius: 3px;
  font-variant-ligatures: none !important;
  font-feature-settings: "liga" 0, "calt" 0 !important;
}

pre code {
  background-color: transparent;
  color: inherit;
  padding: 0;
}

/* Callouts / Cajas destacadas */
.callout {
  padding: 10px 14px;
  border-radius: 6px;
  margin-top: 10px;
  margin-bottom: 12px;
  font-size: 8.5pt;
  page-break-inside: avoid;
}

.callout-title {
  font-weight: 700;
  margin-bottom: 4px;
  text-transform: uppercase;
  font-size: 7.5pt;
  letter-spacing: 0.05em;
}

.callout-tip {
  background-color: #ecfdf5;
  border-left: 4px solid #10b981;
  color: #065f46;
}

.callout-tip .callout-title {
  color: #047857;
}

.callout-warning {
  background-color: #fffbeb;
  border-left: 4px solid #f59e0b;
  color: #92400e;
}

.callout-warning .callout-title {
  color: #b45309;
}

.callout-info {
  background-color: #eff6ff;
  border-left: 4px solid #3b82f6;
  color: #1e40af;
}

.callout-info .callout-title {
  color: #1d4ed8;
}

/* Tablas */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
  margin-bottom: 12px;
  font-size: 8.5pt;
}

th, td {
  border: 1px solid #cbd5e1;
  padding: 6px 10px;
  text-align: left;
}

th {
  background-color: #f1f5f9;
  color: #0f172a;
  font-weight: 600;
}

/* Índice General (TOC) */
.toc-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.toc-card {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 12px;
}

.toc-card h4 {
  margin: 0 0 8px 0;
  font-size: 9.5pt;
  color: #0f172a;
  border-bottom: 1px solid #cbd5e1;
  padding-bottom: 4px;
}

.toc-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
  font-size: 8.5pt;
}

.toc-list li {
  margin-bottom: 4px;
}

.toc-list a {
  color: #0369a1;
  text-decoration: none;
}

.toc-list a:hover {
  text-decoration: underline;
}

.page-break {
  page-break-after: always;
  break-after: page;
}

.module-section-break {
  page-break-before: always;
  break-before: page;
}
"""

def generate_html():
    """Genera el código HTML completo combinando estilos, portada, resumen, TOC y módulos."""
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{METADATA['title']} - {METADATA['subtitle']}</title>
  <style>
{CSS_STYLES}
  </style>
</head>
<body>
""")

    # 1. Portada
    html_parts.append(f"""
  <!-- PORTADA -->
  <div class="cover">
    <div class="badge-k8s">Kubernetes Labs &amp; CKA Training</div>
    <h1>{METADATA['title_part1']} <span>{METADATA['title_part2']}</span></h1>
    <div class="subtitle">{METADATA['subtitle']}</div>
    <p style="color: #64748b; font-size: 10pt; max-width: 650px;">
      {METADATA['description']}
    </p>
    <div class="cover-meta">
      <div class="meta-item">
        <div class="meta-label">Total de Ejercicios</div>
        <div class="meta-val">42 Prácticas (3 por Recurso/Herramienta)</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Niveles de Dificultad</div>
        <div class="meta-val">Intermedio, Avanzado y Nivel CKA</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Ecosistema Evaluado</div>
        <div class="meta-val">12 Recursos Core K8s + Helm + Kustomize</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Compatibilidad Clúster</div>
        <div class="meta-val">Kubernetes v1.28+ (Minikube, Kind, Kubeadm)</div>
      </div>
    </div>
  </div>
""")

    # 2. Resumen Ejecutivo y Metodología
    html_parts.append(f"""
  <!-- RESUMEN EJECUTIVO -->
  <div class="section-container">
    <div class="section-banner section-banner-first" id="resumen-ejecutivo">
      <h2>1. Resumen Ejecutivo y Guía Metodológica</h2>
      <p>Organización de los laboratorios, ciclo de resolución y aislamiento por namespaces</p>
    </div>
    {SUMMARY_TEXT}
    
    <h3 style="color: #0f172a; margin-top: 24px; border-bottom: 2px solid #e2e8f0; padding-bottom: 4px;">Índice General de Contenidos (TOC)</h3>
    <div class="toc-grid">
      <div class="toc-card">
        <h4>Sección I: Cuaderno de Ejercicios</h4>
        <ul class="toc-list">
""")
    for mod in MODULES:
        html_parts.append(f"""          <li><a href="#mod-ex-{mod['id']}">{mod['num']}. {mod['name']}</a> ({mod['ns']})</li>\n""")
    html_parts.append("""        </ul>
      </div>
      <div class="toc-card">
        <h4>Sección II: Solucionario Técnico</h4>
        <ul class="toc-list">
""")
    for mod in MODULES:
        html_parts.append(f"""          <li><a href="#mod-sol-{mod['id']}">{mod['num']}. Soluciones {mod['name']}</a></li>\n""")
    html_parts.append("""        </ul>
      </div>
    </div>
  </div>
""")

    # 3. Sección I: Cuaderno de Ejercicios
    html_parts.append("""
  <!-- SECCIÓN I: EJERCICIOS -->
  <div class="section-container">
    <div class="section-banner" id="seccion-ejercicios">
      <h2>2. Sección I: Cuaderno de Ejercicios Prácticos</h2>
      <p>42 Retos técnicos con contexto real, requerimientos estrictos y comandos de comprobación</p>
    </div>
""")
    for idx, mod in enumerate(MODULES):
        break_class = "module-section-break" if idx > 0 else ""
        html_parts.append(f"""
    <div class="{break_class}">
      <div class="module-header" id="mod-ex-{mod['id']}">
        <h3>{mod['num']}. {mod['name']}</h3>
        <span class="module-namespace">Namespace: {mod['ns']}</span>
      </div>
      <p style="font-size: 8.5pt; color: #475569; margin-bottom: 12px;">{mod['description']}</p>
""")
        for ex in mod['exercises']:
            diff_class = f"diff-{ex['difficulty_class']}"
            html_parts.append(f"""
      <div class="card-exercise" id="{ex['id']}">
        <div class="card-exercise-header">
          <h4 class="card-exercise-title">{ex['num']} {ex['title']}</h4>
          <span class="difficulty-badge {diff_class}">{ex['difficulty_label']}</span>
        </div>
        <p><strong>Escenario:</strong> {ex['scenario']}</p>
        <p><strong>Requerimientos Técnicos:</strong></p>
        <ul>
""")
            for req in ex['requirements']:
                html_parts.append(f"          <li>{req}</li>\n")
            html_parts.append(f"""        </ul>
        <div class="callout callout-info">
          <div class="callout-title">Verificación Esperada</div>
          {ex['verification']}
        </div>
        <a class="btn-nav" href="#{ex['sol_id']}">Ver Solución y Manifiesto &rarr;</a>
      </div>
""")
        html_parts.append("    </div>\n")
    html_parts.append("  </div>\n")

    # 4. Sección II: Solucionario Técnico
    html_parts.append("""
  <!-- SECCIÓN II: SOLUCIONARIO -->
  <div class="section-container">
    <div class="section-banner" id="seccion-soluciones">
      <h2>3. Sección II: Solucionario Técnico y Guías de Validación</h2>
      <p>Manifiestos YAML oficiales, one-liners imperativos, salidas esperadas y errores comunes</p>
    </div>
""")
    for idx, mod in enumerate(MODULES):
        break_class = "module-section-break" if idx > 0 else ""
        html_parts.append(f"""
    <div class="{break_class}">
      <div class="module-header" id="mod-sol-{mod['id']}">
        <h3>{mod['num']}. Soluciones Técnicas: {mod['name']}</h3>
        <span class="module-namespace">Namespace: {mod['ns']}</span>
      </div>
""")
        for sol in mod['solutions']:
            html_parts.append(f"""
      <div class="card-exercise" id="{sol['id']}">
        <div class="card-exercise-header">
          <h4 class="card-exercise-title">{sol['num']} Solución: {sol['title']}</h4>
          <a class="btn-nav btn-nav-return" href="#{sol['ex_id']}">&larr; Volver al Enunciado</a>
        </div>
        {sol['content_html']}
      </div>
""")
        html_parts.append("    </div>\n")
    html_parts.append("""
  </div>
</body>
</html>
""")
    return "".join(html_parts)


def build_outline_structure():
    """Construye la estructura jerárquica para marcadores de panel lateral de PDF."""
    outlines = [
        {"title": "1. Portada y Metadatos", "id": "resumen-ejecutivo"},
        {"title": "2. Resumen Ejecutivo y Guía Metodológica", "id": "resumen-ejecutivo"},
        {
            "title": "3. Sección I: Cuaderno de Ejercicios",
            "id": "seccion-ejercicios",
            "children": []
        },
        {
            "title": "4. Sección II: Solucionario Técnico",
            "id": "seccion-soluciones",
            "children": []
        }
    ]

    for mod in MODULES:
        mod_ex_node = {
            "title": f"{mod['num']}. {mod['name']}",
            "id": f"mod-ex-{mod['id']}",
            "children": []
        }
        for ex in mod['exercises']:
            mod_ex_node["children"].append({
                "title": f"{ex['num']} {ex['title']} [{ex['difficulty_label']}]",
                "id": ex['id']
            })
        outlines[2]["children"].append(mod_ex_node)

        mod_sol_node = {
            "title": f"{mod['num']}. Soluciones {mod['name']}",
            "id": f"mod-sol-{mod['id']}",
            "children": []
        }
        for sol in mod['solutions']:
            mod_sol_node["children"].append({
                "title": f"{sol['num']} Solución: {sol['title']}",
                "id": sol['id']
            })
        outlines[3]["children"].append(mod_sol_node)

    return outlines


def parse_cmap(cmap_str):
    mapping = {}
    for line in cmap_str.split('\n'):
        line = line.strip()
        m = re.match(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', line)
        if m:
            src = int(m.group(1), 16)
            dst_hex = m.group(2)
            chars = []
            for j in range(0, len(dst_hex), 4):
                chunk = dst_hex[j:j+4]
                if chunk:
                    chars.append(chr(int(chunk, 16)))
            mapping[src] = ''.join(chars)
        m2 = re.match(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', line)
        if m2:
            s, e, d = int(m2.group(1), 16), int(m2.group(2), 16), int(m2.group(3), 16)
            for code in range(s, e + 1):
                mapping[code] = chr(d + (code - s))
    return mapping


def decode_bt_block(block, cmaps, default_font=None):
    cur_font = default_font
    chars = []
    tokens = re.split(r'(\s+)', block)
    i = 0
    while i < len(tokens):
        tok = tokens[i].strip()
        if re.match(r'^/F\d+$', tok):
            if i + 4 < len(tokens) and tokens[i+4].strip() == 'Tf':
                cur_font = tok
        m = re.match(r'^<([0-9A-Fa-f]+)>$', tok)
        if m and i + 2 < len(tokens) and tokens[i+2].strip() == 'Tj':
            cmap = cmaps.get(cur_font, {})
            chars.append(cmap.get(int(m.group(1), 16), ''))
        i += 1
    return ''.join(chars)


def inject_actualtext_indentation(reader):
    """
    Inyecta marcado semántico ISO 32000-1 (/ActualText) en bloques de código monoespaciados
    directamente sobre los objetos de página del reader antes de clonar/anexar al writer.
    Esto permite usar writer.append(reader), conservando intactos los destinos nombrados
    (/Names -> /Dests) y los enlaces internos de navegación generados por el motor HTML/PDF.
    """
    modified_pages = 0
    total_wrapped = 0

    for page in reader.pages:
        try:
            contents = page.get('/Contents')
            if not contents:
                continue
            contents_obj = contents.get_object()
            data = contents_obj.get_data().decode('latin1')
        except Exception:
            continue

        fonts = page.get('/Resources', {}).get('/Font', {})
        cmaps = {}
        mono_fonts = set()

        for fname, fobj in fonts.items():
            if '/ToUnicode' in fobj:
                cmaps[fname] = parse_cmap(fobj['/ToUnicode'].get_data().decode('latin1'))
            widths = fobj.get('/Widths')
            if widths:
                non_zero = set([round(float(w), 1) for w in widths if float(w) > 0])
                if len(non_zero) == 1:
                    mono_fonts.add(fname)
            base_font = str(fobj.get('/BaseFont', ''))
            if 'Mono' in base_font or 'Courier' in base_font:
                mono_fonts.add(fname)

        if not mono_fonts:
            continue

        bt_blocks = list(re.finditer(r'BT\s*(.*?)\s*ET', data, re.DOTALL))
        code_xs = []
        for m in bt_blocks:
            b = m.group(0)
            fm = re.search(r'(/F\d+)\s+[\d\.]+\s+Tf', b)
            if fm and fm.group(1) in mono_fonts:
                tm_match = re.search(r'1\s+0\s+0\s+-1\s+([\d\.]+)\s+([\d\.]+)\s+Tm', b)
                if tm_match:
                    code_xs.append(float(tm_match.group(1)))

        if not code_xs:
            continue

        pre_xs = [x for x in code_xs if x >= 30.0]
        base_x = min(pre_xs) if pre_xs else min(code_xs)
        char_w = 6.796936
        for fname in mono_fonts:
            fobj = fonts[fname]
            widths = fobj.get('/Widths')
            if widths:
                for w in widths:
                    if float(w) > 0:
                        char_w = (float(w) * 11.33) / 1000.0
                        break
                break

        new_data = data
        page_wrapped = 0
        for m in reversed(bt_blocks):
            block = m.group(0)
            f_match = re.search(r'(/F\d+)\s+[\d\.]+\s+Tf', block)
            if not f_match or f_match.group(1) not in mono_fonts:
                continue
            tm_match = re.search(r'1\s+0\s+0\s+-1\s+([\d\.]+)\s+([\d\.]+)\s+Tm', block)
            if not tm_match:
                continue
            x = float(tm_match.group(1))
            txt = decode_bt_block(block, cmaps, default_font=f_match.group(1))
            if not txt.strip():
                continue
            leading_from_txt = len(txt) - len(txt.lstrip(' '))
            leading_from_x = int(round((x - base_x) / char_w)) if x > base_x else 0
            num_spaces = max(leading_from_txt, leading_from_x)
            if num_spaces > 0:
                actual_line = (' ' * num_spaces) + txt.lstrip(' ')
            else:
                actual_line = txt
            hex_content = 'FEFF' + actual_line.encode('utf-16-be').hex().upper()
            wrapped = f'/Span <</ActualText <{hex_content}>>> BDC\n{block}\nEMC'
            new_data = new_data[:m.start()] + wrapped + new_data[m.end():]
            page_wrapped += 1

        if page_wrapped > 0:
            contents_obj.set_data(new_data.encode('latin1'))
            modified_pages += 1
            total_wrapped += page_wrapped

    print(f"Marcado semántico /ActualText inyectado en {modified_pages} páginas ({total_wrapped} líneas con sangría preservadas).")


def add_pdf_bookmarks(pdf_path):
    """Inyecta el árbol de marcadores (Document Outlines) y /ActualText en el PDF usando pypdf."""
    try:
        import pypdf
    except ImportError:
        print("Error: 'pypdf' no está disponible. No se pueden inyectar los marcadores.")
        return False

    print("Procesando PDF con pypdf (Inyección de /ActualText e índices de marcadores)...")
    reader = pypdf.PdfReader(pdf_path)
    inject_actualtext_indentation(reader)

    writer = pypdf.PdfWriter()
    writer.append(reader)

    def get_page(target_id):
        if not target_id:
            return None
        for key in (target_id, "/" + target_id):
            if key in reader.named_destinations:
                return reader.get_destination_page_number(reader.named_destinations[key])
        return None

    outlines = build_outline_structure()
    # Asignar páginas iniciales seguras para las secciones de nivel superior
    outlines[0]["page"] = 0   # Portada
    outlines[1]["page"] = 1   # Resumen y Metodología
    outlines[2]["page"] = get_page("mod-ex-pods") or 2   # Sección I: Ejercicios
    outlines[3]["page"] = get_page("mod-sol-pods") or 25 # Sección II: Soluciones

    def add_items(items, parent=None):
        for item in items:
            p_num = item.get("page")
            if p_num is None and "id" in item:
                p_num = get_page(item["id"])
            if p_num is not None:
                node = writer.add_outline_item(item["title"], p_num, parent=parent)
                if "children" in item:
                    add_items(item["children"], parent=node)

    add_items(outlines)

    temp_path = pdf_path + ".tmp"
    with open(temp_path, "wb") as f:
        writer.write(f)
    os.replace(temp_path, pdf_path)
    return True


def compile_pdf():
    """Genera el HTML y compila con Chrome Headless."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    html_content = generate_html()
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML generado exitosamente en: {HTML_PATH} ({len(html_content)} caracteres)")

    chrome_candidates = [
        "/opt/google/chrome/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser"
    ]
    chrome_bin = None
    for cand in chrome_candidates:
        if os.path.exists(cand):
            chrome_bin = cand
            break
        found = shutil.which(cand)
        if found:
            chrome_bin = found
            break

    if not chrome_bin:
        chrome_bin = "google-chrome-stable"

    cmd = [
        chrome_bin,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-local-file-accesses",
        "--user-data-dir=/tmp/chrome-user-data-k8s",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        f"file://{HTML_PATH}"
    ]
    print(f"Compilando PDF con {chrome_bin} hacia: {PDF_PATH}...")
    if os.path.exists(PDF_PATH):
        os.remove(PDF_PATH)

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.exists(PDF_PATH):
        add_pdf_bookmarks(PDF_PATH)
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"¡Éxito! Archivo PDF generado con marcadores del panel lateral: {PDF_PATH} ({size_kb:.1f} KB)")
        return True
    else:
        print("Error generando PDF:")
        print(res.stderr)
        return False


if __name__ == "__main__":
    success = compile_pdf()
    sys.exit(0 if success else 1)
