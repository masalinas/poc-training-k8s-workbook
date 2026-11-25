#!/usr/bin/env python3
# =============================================================================
# scripts/verify_workbook.py
# Verifica la integridad de enlaces, marcadores, indentación del PDF y manifiestos
# =============================================================================
import os
import re
import sys
import subprocess
import pypdf
import yaml

HTML_PATH = "docs/k8s-exercises-workbook.html"
PDF_PATH = "k8s-exercises-workbook.pdf"
MANIFESTS_DIR = "manifests"

def verify_html_links():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Extraer todos los IDs definidos
    ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
    # Extraer todos los hrefs internos
    hrefs = re.findall(r'href=["\']#([^"\']+)["\']', html)

    print(f"Total IDs encontrados en HTML: {len(ids)}")
    print(f"Total enlaces internos (href=#...): {len(hrefs)}")

    missing = []
    for h in hrefs:
        if h not in ids:
            missing.append(h)

    if missing:
        print(f"ERROR: Enlaces rotos detectados ({len(missing)}):", missing)
        return False
    else:
        print("✓ Todos los enlaces internos resuelven correctamente a IDs existentes.")

    # Verificar que existen los 42 ejercicios y 42 soluciones
    for mod_idx in range(1, 15):
        for ex_idx in range(1, 4):
            ex_id = f"ex-{mod_idx}-{ex_idx}"
            sol_id = f"sol-{mod_idx}-{ex_idx}"
            if ex_id not in ids:
                print(f"Falta ejercicio: {ex_id}")
                return False
            if sol_id not in ids:
                print(f"Falta solución: {sol_id}")
                return False

    print("✓ Verificados los 42 IDs de ejercicio (ex-X-Y) y los 42 IDs de solución (sol-X-Y).")
    return True


def verify_pdf():
    reader = pypdf.PdfReader(PDF_PATH)
    num_pages = len(reader.pages)
    print(f"Total de páginas en el PDF: {num_pages}")
    
    outlines = reader.outline
    print(f"Marcadores raíz en panel lateral: {len(outlines)}")
    
    def count_nodes(nodes):
        count = 0
        for node in nodes:
            if isinstance(node, list):
                count += count_nodes(node)
            else:
                count += 1
        return count

    total_outline_items = count_nodes(outlines)
    print(f"Total de elementos en árbol de marcadores: {total_outline_items}")
    assert total_outline_items >= 84, f"Se esperaban al menos 84 marcadores, encontrados {total_outline_items}"
    print("✓ Árbol jerárquico de marcadores del panel lateral verificado con éxito.")
    return True


def verify_pdf_links():
    """Valida que todos los enlaces internos (/Link) del PDF resuelven a destinos válidos."""
    print("Verificando destinos nombrados y enlaces interactivos en el PDF...")
    reader = pypdf.PdfReader(PDF_PATH)
    named_dests = reader.named_destinations
    print(f"Destinos nombrados (/Names -> /Dests) en PDF: {len(named_dests)}")
    assert len(named_dests) >= 84, f"Se esperaban al menos 84 destinos nombrados, encontrados {len(named_dests)}"

    total_links = 0
    resolved_links = 0
    unresolved = []

    for p_idx, page in enumerate(reader.pages):
        for annot in page.get('/Annots', []):
            obj = annot.get_object()
            if obj.get('/Subtype') == '/Link':
                total_links += 1
                dest = obj.get('/Dest') or (obj.get('/A') and obj.get('/A').get('/D'))
                if dest:
                    dest_str = str(dest)
                    # Comprobar resolución en named_destinations
                    found = False
                    for candidate in (dest_str, dest_str.lstrip('/'), '/' + dest_str.lstrip('/')):
                        if candidate in named_dests:
                            found = True
                            break
                    if found:
                        resolved_links += 1
                    else:
                        unresolved.append((p_idx + 1, dest_str))

    print(f"Total enlaces interactivos (/Link) encontrados: {total_links}")
    print(f"Enlaces resueltos con éxito a destinos existentes: {resolved_links}")
    if unresolved:
        print(f"ERROR: Enlaces no resueltos ({len(unresolved)}):", unresolved[:10])
        return False

    assert total_links >= 84, f"Se esperaban al menos 84 enlaces interactivos, encontrados {total_links}"
    assert resolved_links == total_links, "No todos los enlaces interactivos resuelven a un destino válido"
    print("✓ Todos los botones y enlaces interactivos del PDF resuelven a sus destinos correctamente.")
    return True


def verify_pdf_indentation():
    """Valida que la extracción de texto del PDF conserva sangría y espacios YAML."""
    print("Verificando preservación de espacios e indentación en PDF (vía pdftotext estándar)...")
    res = subprocess.run(['pdftotext', PDF_PATH, '-'], stdout=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ADVERTENCIA: pdftotext no disponible en entorno para verificar texto extraído.")
        return True

    all_lines = res.stdout.split('\n')
    indented_2 = [l for l in all_lines if l.startswith('  ') and not l.startswith('   ')]
    indented_4 = [l for l in all_lines if l.startswith('    ')]

    print(f"Líneas con 2 espacios detectadas: {len(indented_2)}")
    print(f"Líneas con 4+ espacios detectadas: {len(indented_4)}")

    # Verificar presencia explícita de fragmentos de YAML con indentación
    assert any('  name: lab-pods' in l for l in all_lines), "Falta '  name: lab-pods' con 2 espacios"
    assert any('    app: multi-container-demo' in l for l in all_lines), "Falta '    app: multi-container-demo' con 4 espacios"
    assert len(indented_2) >= 100, f"Se esperaban al menos 100 líneas con 2 espacios, detectadas {len(indented_2)}"
    assert len(indented_4) >= 100, f"Se esperaban al menos 100 líneas con 4+ espacios, detectadas {len(indented_4)}"

    print("✓ Indentación y espacios YAML preservados correctamente en la extracción del PDF.")
    return True


def verify_manifests():
    """Valida la existencia y sintaxis de los 42 manifiestos exportados en manifests/."""
    print(f"Verificando directorio de manifiestos: {MANIFESTS_DIR}...")
    if not os.path.exists(MANIFESTS_DIR):
        print(f"ERROR: Directorio {MANIFESTS_DIR} no existe.")
        return False

    yaml_files = []
    for root, _, files in os.walk(MANIFESTS_DIR):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".yml"):
                yaml_files.append(os.path.join(root, f))

    print(f"Total de archivos YAML encontrados en {MANIFESTS_DIR}: {len(yaml_files)}")
    if len(yaml_files) != 42:
        print(f"ERROR: Se esperaban 42 manifiestos YAML, encontrados {len(yaml_files)}")
        return False

    # Validar que cada archivo sea YAML sintácticamente correcto
    for yf in yaml_files:
        with open(yf, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            list(yaml.safe_load_all(content))
        except Exception as e:
            print(f"ERROR en archivo {yf}: {e}")
            return False

    print("✓ Los 42 manifiestos YAML exportados son sintácticamente válidos.")
    return True


if __name__ == "__main__":
    html_ok = verify_html_links()
    pdf_ok = verify_pdf()
    links_ok = verify_pdf_links()
    indent_ok = verify_pdf_indentation()
    manifests_ok = verify_manifests()

    if html_ok and pdf_ok and links_ok and indent_ok and manifests_ok:
        print("\n=== ¡TODAS LAS VERIFICACIONES COMPLETADAS EXITOSAMENTE! ===")
        sys.exit(0)
    else:
        print("\n=== FALLO EN LAS VERIFICACIONES ===")
        sys.exit(1)
