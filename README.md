# Cuaderno de Ejercicios y Solucionario Técnico de Kubernetes

Guía práctica intensiva y profesional compuesta por **42 ejercicios de laboratorio y su solucionario técnico completo**, orientada a la capacitación práctica de administradores de sistemas, ingenieros DevOps/SRE y a la preparación rigurosa de las certificaciones oficiales **CKA (Certified Kubernetes Administrator)** y **CKAD (Certified Kubernetes Application Developer)**.

El repositorio incluye el código fuente modular en Python, el documento maquetado en HTML5 y el documento compilado final en formato PDF (**86 páginas**) con diseño editorial profesional y doble sistema de navegación interactiva.

---

## 🎯 Aspectos Destacados

- **42 Ejercicios Prácticos y 42 Soluciones Exhaustivas**: Distribuidos uniformemente a razón de 3 ejercicios por cada uno de los 14 bloques temáticos.
- **Cobertura Integral**: Abarca los 12 recursos core esenciales de Kubernetes junto con las herramientas estándar de empaquetado y personalización declarativa (**Helm** y **Kustomize**).
- **Nivel de Dificultad Explícito**: Clasificación visible en cada reto entre `[Intermedio]`, `[Avanzado]` y `[Nivel CKA]`.
- **Aislamiento por Namespaces**: Cada módulo opera en su propio namespace (`lab-*`) para evitar colisiones y permitir entornos limpios y reproducibles.
- **Doble Navegación Interactiva**:
  - Enlaces bidireccionales internos dentro del documento (salto directo del Enunciado a la Solución y retorno al Enunciado).
  - Árbol jerárquico nativo de marcadores (*Document Outlines*) en el panel lateral del visor PDF.
- **Enfoque Práctico de Certificación**: Cada solución incluye manifiestos YAML comentados línea a línea, atajos imperativos con `kubectl` y `helm`, procedimientos de verificación con salidas esperadas y un apartado específico de **Trampas CKA / Errores Comunes ("Gotchas")**.

---

## 📚 Estructura de Módulos y Namespaces

| Nº | Módulo / Recurso | Namespace Asignado | Ejercicios y Temáticas Destacadas |
|:--:|:---|:---|:---|
| **01** | **Pods** | `lab-pods` | Multi-contenedor (Sidecar pattern), Liveness/Readiness probes, Recursos y límites (QoS Burstable/Guaranteed). |
| **02** | **ReplicaSets** | `lab-replicasets` | Selectores de coincidencia (`matchExpressions`), auto-sanación de Pods y reconciliación de réplicas. |
| **03** | **Deployments** | `lab-deployments` | Rolling updates, `maxSurge`/`maxUnavailable`, pausas, rollbacks a revisiones específicas. |
| **04** | **Services** | `lab-services` | ClusterIP multi-puerto, NodePort con puertos estáticos, Headless Services para descubrimiento DNS. |
| **05** | **ConfigMaps** | `lab-configmaps` | Inyección como variables de entorno, carga masiva (`envFrom`), montaje como volumen con `subPath`. |
| **06** | **Secrets** | `lab-secrets` | Opaque Secrets codificados en Base64, TLS Secrets con certificados SSL, proyecciones seguras en volúmenes. |
| **07** | **Almacenamiento (PV & PVC)** | `lab-storage` | Modos de acceso (`ReadWriteOnce`), políticas de reciclaje (`Retain`), StorageClasses dinámicas. |
| **08** | **Jobs y CronJobs** | `lab-jobs` | Tareas paralelas con completion count, expresiones cron recurrentes, políticas de concurrencia (`Forbid`). |
| **09** | **DaemonSets** | `lab-daemonsets` | Despliegue por nodo, selectores de nodo (`nodeSelector`), tolerancias a taints de control-plane. |
| **10** | **StatefulSets** | `lab-statefulsets` | Identidad de red persistente, `volumeClaimTemplates` independientes por réplica, escalado ordenado. |
| **11** | **Ingress** | `lab-ingress` | Reglas de enrutamiento basadas en rutas y subdominios (`host`), terminación TLS con ingress-nginx. |
| **12** | **RBAC** | `lab-rbac` | Roles y RoleBindings, ClusterRoles y ClusterRoleBindings, ServiceAccounts restringidas (`kubectl auth can-i`). |
| **13** | **Helm** | `lab-helm` | Creación de charts, inyección de variables (`values.yaml`), gestión de versiones, rollbacks e inspección de releases. |
| **14** | **Kustomize** | `lab-kustomize` | Estructura base/overlays (`dev` / `prod`), parches estratégicos JSON6902, transformaciones sin plantillas. |

---

## 🗂️ Estructura del Repositorio

```text
.
├── k8s-exercises-workbook.pdf   # Cuaderno final compilado en PDF (86 páginas, marcadores y enlaces interactivos)
├── README.md                    # Descripción y guía de uso del repositorio
├── docs/
│   └── k8s-exercises-workbook.html # Documento estructurado en HTML5/CSS listo para renderizado
├── scripts/
│   ├── content_data.py          # Metadatos del curso y agregador de los 14 módulos
│   ├── modules_fundamentos.py   # Definición de módulos 1 al 4 (Pods, ReplicaSets, Deployments, Services)
│   ├── modules_config_storage.py# Definición de módulos 5 al 7 (ConfigMaps, Secrets, Storage PV/PVC)
│   ├── modules_advanced.py      # Definición de módulos 8 al 10 (Jobs/CronJobs, DaemonSets, StatefulSets)
│   ├── modules_net_sec.py       # Definición de módulos 11 y 12 (Ingress, RBAC)
│   ├── modules_packaging.py     # Definición de módulos 13 y 14 (Helm, Kustomize)
│   ├── generate_html_pdf.py     # Pipeline de compilación HTML -> PDF vía Headless Chrome + pypdf
│   └── verify_workbook.py       # Suite de verificación técnica (enlaces, IDs, páginas y marcadores)
└── openspec/                    # Especificaciones formales y trazabilidad de cambios (OpenSpec)
    ├── config.yaml
    ├── specs/                   # Especificaciones de contenido y generación PDF
    └── changes/archive/         # Historial de cambios y propuestas implementadas
```

---

## 🛠️ Requisitos y Dependencias

Para compilar el documento o ejecutar las validaciones técnicas se requiere:

1. **Python 3.8+**
2. **Librería Python `pypdf`**:
   ```bash
   pip install pypdf
   ```
3. **Navegador para renderizado Headless**:
   - `google-chrome` o `chromium-browser` instalado en el sistema y disponible en el `PATH`.

---

## 🚀 Guía de Uso

### 1. Compilación del Cuaderno (HTML y PDF)

El script `scripts/generate_html_pdf.py` genera el archivo intermedio en `docs/k8s-exercises-workbook.html`, invoca Chrome Headless para compilar el PDF y finalmente utiliza `pypdf` para inyectar los metadatos y el árbol jerárquico de marcadores:

```bash
python3 scripts/generate_html_pdf.py
```

### 2. Verificación de Integridad

Para validar que no existen enlaces rotos, que los 42 ejercicios y 42 soluciones tienen identificadores válidos y que el árbol de marcadores del PDF se ha generado correctamente:

```bash
python3 scripts/verify_workbook.py
```

Salida esperada:
```text
Total IDs encontrados en HTML: 115
Total enlaces internos (href=#...): 112
✓ Todos los enlaces internos resuelven correctamente a IDs existentes.
✓ Verificados los 42 IDs de ejercicio (ex-X-Y) y los 42 IDs de solución (sol-X-Y).
Total de páginas en el PDF: 86
Marcadores raíz en panel lateral: 6
Total de elementos en árbol de marcadores: 116
✓ Árbol jerárquico de marcadores del panel lateral verificado con éxito.
=== ¡TODAS LAS VERIFICACIONES COMPLETADAS EXITOSAMENTE! ===
```

---

## 📄 Archivos de Referencia

- [k8s-exercises-workbook.pdf](file:///home/miguel/git/poc-training-k8s-workbook/k8s-exercises-workbook.pdf): Documento PDF final.
- [docs/k8s-exercises-workbook.html](file:///home/miguel/git/poc-training-k8s-workbook/docs/k8s-exercises-workbook.html): Maquetación web del cuaderno.
- [scripts/generate_html_pdf.py](file:///home/miguel/git/poc-training-k8s-workbook/scripts/generate_html_pdf.py): Script de generación y compilación.
- [scripts/verify_workbook.py](file:///home/miguel/git/poc-training-k8s-workbook/scripts/verify_workbook.py): Script de verificación y pruebas.
