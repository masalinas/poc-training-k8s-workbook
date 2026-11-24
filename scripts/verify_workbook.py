#!/usr/bin/env python3
# =============================================================================
# scripts/verify_workbook.py
# Verifica la integridad de enlaces, estructura de marcadores y páginas del PDF
# =============================================================================
import re
import sys
import pypdf

HTML_PATH = "docs/k8s-exercises-workbook.html"
PDF_PATH = "k8s-exercises-workbook.pdf"

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

if __name__ == "__main__":
    html_ok = verify_html_links()
    pdf_ok = verify_pdf()
    if html_ok and pdf_ok:
        print("\n=== ¡TODAS LAS VERIFICACIONES COMPLETADAS EXITOSAMENTE! ===")
        sys.exit(0)
    else:
        print("\n=== FALLO EN LAS VERIFICACIONES ===")
        sys.exit(1)
