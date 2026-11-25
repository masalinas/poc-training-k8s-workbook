# Cuaderno de Ejercicios y Solucionario Técnico de Kubernetes

<div align="center">

![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.28%2B-326CE5?logo=kubernetes&logoColor=white)
![Certificación](https://img.shields.io/badge/Certificación-CKA_%7C_CKAD-blue?logo=linuxfoundation&logoColor=white)
![Ejercicios](https://img.shields.io/badge/Ejercicios-42_Labs-success)
![Módulos](https://img.shields.io/badge/Módulos-14_Bloques-orange)
![Ecosistema](https://img.shields.io/badge/Ecosistema-Helm_%7C_Kustomize-0F1689?logo=helm&logoColor=white)
![Deliverable](https://img.shields.io/badge/PDF-k8s--exercises--workbook.pdf-red?logo=adobeacrobatreader)

**Cuaderno Práctico y Solucionario Oficial:** 42 ejercicios de laboratorio y resoluciones exhaustivas, 14 módulos temáticos aislados por namespaces (`lab-*`), 42 manifiestos YAML listos para aplicar y guía editorial de 86 páginas con marcado `/ActualText` para preparación rigurosa CKA y CKAD.

</div>

---

Guía práctica intensiva y profesional compuesta por **42 ejercicios de laboratorio y su solucionario técnico completo**, orientada a la capacitación práctica de administradores de sistemas, ingenieros DevOps/SRE y a la preparación rigurosa de las certificaciones oficiales **CKA (Certified Kubernetes Administrator)** y **CKAD (Certified Kubernetes Application Developer)**.

El repositorio incluye el código fuente modular en Python, el documento maquetado en HTML5, el documento compilado final en formato PDF (**86 páginas**) con diseño editorial profesional, doble sistema de navegación interactiva y un directorio estructurado con los **42 manifiestos YAML listos para aplicar**.

---

## 🎯 Aspectos Destacados

- **42 Ejercicios Prácticos y 42 Soluciones Exhaustivas**: Distribuidos uniformemente a razón de 3 ejercicios por cada uno de los 14 bloques temáticos.
- **Cobertura Integral**: Abarca los 12 recursos core esenciales de Kubernetes junto con las herramientas estándar de empaquetado y personalización declarativa (**Helm** y **Kustomize**).
- **Nivel de Dificultad Explícito**: Clasificación visible en cada reto entre `[Intermedio]`, `[Avanzado]` y `[Nivel CKA]`.
- **Aislamiento por Namespaces**: Cada módulo opera en su propio namespace (`lab-*`) para evitar colisiones y permitir entornos limpios y reproducibles.
- **Doble Navegación Interactiva**:
  - Enlaces bidireccionales internos dentro del documento (salto directo del Enunciado a la Solución y retorno al Enunciado).
  - Árbol jerárquico nativo de marcadores (*Document Outlines*) en el panel lateral del visor PDF.
- **Preservación Total de Sangría en PDF**: Integración de marcado semántico ISO 32000-1 (`/ActualText`) que asegura que al copiar cualquier fragmento YAML desde el PDF hacia un editor o fichero local se conserven intactos los espacios de indentación.
- **Directorio de Manifiestos Listos para Desplegar**: Carpeta `manifests/` organizada por módulos temáticos con los 42 YAMLs comentados para su ejecución directa con `kubectl apply`.
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
├── k8s-exercises-workbook.pdf   # Cuaderno final compilado en PDF (86 páginas, marcadores e indentación preservada)
├── README.md                    # Descripción y guía de uso del repositorio
├── docs/
│   └── k8s-exercises-workbook.html # Documento estructurado en HTML5/CSS listo para renderizado
├── manifests/                   # 42 manifiestos YAML de solución listos para aplicar con kubectl
│   ├── 01-pods/
│   ├── 02-replicasets/
│   ├── ...
│   └── 14-kustomize/
├── scripts/
│   ├── content_data.py          # Metadatos del curso y agregador de los 14 módulos
│   ├── modules_fundamentos.py   # Definición de módulos 1 al 4 (Pods, ReplicaSets, Deployments, Services)
│   ├── modules_config_storage.py# Definición de módulos 5 al 7 (ConfigMaps, Secrets, Storage PV/PVC)
│   ├── modules_advanced.py      # Definición de módulos 8 al 10 (Jobs/CronJobs, DaemonSets, StatefulSets)
│   ├── modules_net_sec.py       # Definición de módulos 11 y 12 (Ingress, RBAC)
│   ├── modules_packaging.py     # Definición de módulos 13 y 14 (Helm, Kustomize)
│   ├── generate_html_pdf.py     # Pipeline de compilación HTML -> PDF con /ActualText e inyección de marcadores
│   ├── export_manifests.py      # Generador de los 42 archivos YAML en manifests/
│   └── verify_workbook.py       # Suite de verificación técnica (enlaces, IDs, páginas, indentación y YAML)
└── openspec/                    # Especificaciones formales y trazabilidad de cambios (OpenSpec)
    ├── config.yaml
    ├── specs/                   # Especificaciones de contenido y generación PDF
    └── changes/archive/         # Historial de cambios y propuestas implementadas
```

---

## 🛠️ Requisitos y Dependencias

Para compilar el documento o ejecutar las validaciones técnicas se requiere:

1. **Python 3.8+**
2. **Librerías Python `pypdf` y `pyyaml`**:
   ```bash
   pip install pypdf pyyaml
   ```
3. **Navegador para renderizado Headless**:
   - `google-chrome` o `chromium-browser` instalado en el sistema y disponible en el `PATH`.

---

## 🚀 Guía de Uso

### 1. Compilación del Cuaderno (HTML y PDF)

El script `scripts/generate_html_pdf.py` genera el archivo intermedio en `docs/k8s-exercises-workbook.html`, invoca Chrome Headless para compilar el PDF y utiliza `pypdf` para inyectar tanto el marcado semántico `/ActualText` (garantizando copia fiel de sangrías) como el árbol de marcadores interactivo:

```bash
python3 scripts/generate_html_pdf.py
```

### 2. Exportación de Manifiestos YAML (`manifests/`)

Para regenerar o inspeccionar los 42 archivos YAML organizados por módulos temáticos:

```bash
python3 scripts/export_manifests.py
```

Puedes aplicar directamente cualquier ejercicio en tu clúster de laboratorio:

```bash
kubectl apply -f manifests/01-pods/01-pod-sidecar-logger.yaml
```

### 3. Verificación de Integridad

Para validar que los enlaces internos resuelven, los marcadores están inyectados, la extracción de texto del PDF conserva los espacios de sangría y los 42 manifiestos exportados son sintácticamente válidos:

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
Verificando preservación de espacios e indentación en PDF (vía pdftotext estándar)...
Líneas con 2 espacios detectadas: 308
Líneas con 4+ espacios detectadas: 519
✓ Indentación y espacios YAML preservados correctamente en la extracción del PDF.
Verificando directorio de manifiestos: manifests...
Total de archivos YAML encontrados en manifests: 42
✓ Los 42 manifiestos YAML exportados son sintácticamente válidos.
=== ¡TODAS LAS VERIFICACIONES COMPLETADAS EXITOSAMENTE! ===
```

---

## 📄 Archivos de Referencia

- [k8s-exercises-workbook.pdf](file:///home/miguel/git/poc-training-k8s-workbook/k8s-exercises-workbook.pdf): Documento PDF final con navegación lateral y copia fiel de sangría.
- [manifests/](file:///home/miguel/git/poc-training-k8s-workbook/manifests): Directorio con los 42 manifiestos YAML organizados por módulo.
- [docs/k8s-exercises-workbook.html](file:///home/miguel/git/poc-training-k8s-workbook/docs/k8s-exercises-workbook.html): Maquetación web del cuaderno.
- [scripts/generate_html_pdf.py](file:///home/miguel/git/poc-training-k8s-workbook/scripts/generate_html_pdf.py): Script de generación y compilación con marcado `/ActualText`.
- [scripts/export_manifests.py](file:///home/miguel/git/poc-training-k8s-workbook/scripts/export_manifests.py): Script exportador de manifiestos.
- [scripts/verify_workbook.py](file:///home/miguel/git/poc-training-k8s-workbook/scripts/verify_workbook.py): Suite de verificación y pruebas integradas.
