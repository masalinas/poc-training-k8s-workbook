#!/usr/bin/env python3
# =============================================================================
# scripts/export_manifests.py
# Exportador de los 42 manifiestos YAML de solución a la carpeta manifests/
# =============================================================================
import os
import sys
import re
import yaml

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIFESTS_DIR = os.path.join(WORKSPACE_DIR, "manifests")

try:
    from content_data import MODULES
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from content_data import MODULES

# Nombres de fichero normalizados para cada uno de los 42 ejercicios
MANIFEST_FILENAMES = {
    # Módulo 1: Pods
    (1, 1): "01-pod-sidecar-logger.yaml",
    (1, 2): "02-pod-backend-init.yaml",
    (1, 3): "03-pod-health-hardened.yaml",
    # Módulo 2: ReplicaSets
    (2, 1): "01-rs-payment.yaml",
    (2, 2): "02-rs-scaling.yaml",
    (2, 3): "03-rs-quarantine.yaml",
    # Módulo 3: Deployments
    (3, 1): "01-deploy-web-secured.yaml",
    (3, 2): "02-deploy-rolling-update.yaml",
    (3, 3): "03-deploy-ecommerce-rollback.yaml",
    # Módulo 4: Services
    (4, 1): "01-svc-multi-port.yaml",
    (4, 2): "02-svc-nodeport.yaml",
    (4, 3): "03-svc-headless.yaml",
    # Módulo 5: ConfigMaps
    (5, 1): "01-cm-env.yaml",
    (5, 2): "02-cm-volume.yaml",
    (5, 3): "03-cm-subpath.yaml",
    # Módulo 6: Secrets
    (6, 1): "01-sec-env.yaml",
    (6, 2): "02-sec-volume-perms.yaml",
    (6, 3): "03-sec-tls.yaml",
    # Módulo 7: Storage
    (7, 1): "01-pv-hostpath.yaml",
    (7, 2): "02-pvc-claim.yaml",
    (7, 3): "03-pod-storage-writer-reader.yaml",
    # Módulo 8: Jobs
    (8, 1): "01-job-single.yaml",
    (8, 2): "02-job-parallel.yaml",
    (8, 3): "03-cronjob-cleanup.yaml",
    # Módulo 9: DaemonSets
    (9, 1): "01-ds-log-collector.yaml",
    (9, 2): "02-ds-tolerations.yaml",
    (9, 3): "03-ds-rolling-update.yaml",
    # Módulo 10: StatefulSets
    (10, 1): "01-sts-basic.yaml",
    (10, 2): "02-sts-storage.yaml",
    (10, 3): "03-sts-scale-down.yaml",
    # Módulo 11: Ingress
    (11, 1): "01-ingress-path-routing.yaml",
    (11, 2): "02-ingress-vhost.yaml",
    (11, 3): "03-ingress-tls.yaml",
    # Módulo 12: RBAC
    (12, 1): "01-sa-hardened.yaml",
    (12, 2): "02-role-pod-viewer.yaml",
    (12, 3): "03-rolebinding-app.yaml",
    # Módulo 13: Helm
    (13, 1): "01-helm-chart-metadata.yaml",
    (13, 2): "02-values-production.yaml",
    (13, 3): "03-helm-release-spec.yaml",
    # Módulo 14: Kustomize
    (14, 1): "01-kustomization-base.yaml",
    (14, 2): "02-kustomization-cm-generator.yaml",
    (14, 3): "03-kustomization-overlay-prod.yaml",
}

# Manifiestos complementarios para ejercicios orientados a procedimientos
SPECIAL_MANIFESTS = {
    (2, 3): """apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-quarantine-demo
  namespace: lab-replicasets
  labels:
    app: order-processor
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-processor
  template:
    metadata:
      labels:
        app: order-processor
        tier: backend
    spec:
      containers:
        - name: processor
          image: busybox:1.36
          command: ["sh", "-c", "echo Procesando pedidos...; while true; do sleep 10; done"]
""",
    (3, 3): """apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-ecommerce
  namespace: lab-deployments
  labels:
    app: ecommerce
  annotations:
    kubernetes.io/change-cause: "v1.0: Despliegue inicial estable nginx-1.24"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ecommerce
  template:
    metadata:
      labels:
        app: ecommerce
    spec:
      containers:
        - name: web
          image: nginx:1.24-alpine
          ports:
            - containerPort: 80
""",
    (6, 3): """apiVersion: v1
kind: Secret
metadata:
  name: sec-tls-cert
  namespace: lab-secrets
type: kubernetes.io/tls
data:
  # Certificado y clave codificados en Base64 para test.local
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCg==
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQo=
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-tls-web
  namespace: lab-secrets
spec:
  containers:
    - name: nginx-ssl
      image: nginx:1.25-alpine
      ports:
        - containerPort: 443
      volumeMounts:
        - name: certs-vol
          mountPath: /etc/nginx/certs
          readOnly: true
  volumes:
    - name: certs-vol
      secret:
        secretName: sec-tls-cert
""",
    (9, 3): """apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ds-node-log-collector
  namespace: lab-daemonsets
spec:
  selector:
    matchLabels:
      name: node-log-collector
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  template:
    metadata:
      labels:
        name: node-log-collector
    spec:
      containers:
        - name: collector
          image: busybox:1.36
          command: ["sh", "-c", "while true; do sleep 3600; done"]
""",
    (10, 3): """apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: sts-web
  namespace: lab-statefulsets
spec:
  serviceName: "sts-web-service"
  replicas: 3
  selector:
    matchLabels:
      app: sts-web
  template:
    metadata:
      labels:
        app: sts-web
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
""",
    (13, 1): """apiVersion: v2
name: web-app
description: Un Helm chart de produccion para web-app en Kubernetes
type: application
version: 0.1.0
appVersion: "1.25.0"
maintainers:
  - name: Laboratorio K8s
    email: lab@ejemplo.local
dependencies: []
""",
    (13, 3): """apiVersion: v2
name: web-app-lifecycle
description: Chart para pruebas de ciclo de vida, upgrade y rollback
type: application
version: 1.1.0
appVersion: "2.0.0"
values:
  replicaCount: 3
  image:
    repository: nginx
    tag: "1.25-alpine"
    pullPolicy: IfNotPresent
""",
}


def extract_yaml_from_solution(mod_idx, sol_idx, sol_content):
    """Extrae el bloque YAML declarativo del HTML de la solución."""
    key = (mod_idx, sol_idx)
    if key in SPECIAL_MANIFESTS:
        return SPECIAL_MANIFESTS[key].strip()

    blocks = re.findall(r'<pre><code>(.*?)</code></pre>', sol_content, re.DOTALL)
    
    # 1. Buscar bloques que contengan apiVersion o kind
    for b in blocks:
        # Decodificar entidades HTML básicas
        raw = b.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        # Si contiene heredoc 'cat <<EOF | kubectl apply -f -\n...'
        if "cat <<EOF" in raw or "cat <<'EOF'" in raw:
            eof_match = re.search(r'cat\s+<<[\'\"]?EOF[\'\"]?\s*(?:\|\s*kubectl[^\n]*)?\n(.*?)\nEOF', raw, re.DOTALL)
            if eof_match:
                return eof_match.group(1).strip()
        if "apiVersion:" in raw and "kind:" in raw:
            return raw.strip()

    # 2. Si no tiene apiVersion explícito (ej. values.yaml o kustomize)
    for b in blocks:
        raw = b.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        if not raw.strip().startswith("#") and ":" in raw:
            return raw.strip()

    # Fallback al primer bloque no de comentarios
    for b in blocks:
        raw = b.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        if not raw.strip().startswith("#"):
            return raw.strip()

    return blocks[0].strip() if blocks else ""


def export_all_manifests():
    """Genera la estructura de carpetas y los 42 archivos YAML."""
    os.makedirs(MANIFESTS_DIR, exist_ok=True)
    exported_count = 0
    errors = []

    print(f"Exportando 42 manifiestos YAML a {MANIFESTS_DIR}...")

    for mod in MODULES:
        mod_num = int(mod['num'])
        mod_slug = mod['id']
        dir_name = f"{mod_num:02d}-{mod_slug}"
        mod_dir = os.path.join(MANIFESTS_DIR, dir_name)
        os.makedirs(mod_dir, exist_ok=True)

        for s_idx, sol in enumerate(mod['solutions'], start=1):
            ex_num = s_idx
            filename = MANIFEST_FILENAMES.get((mod_num, ex_num), f"{ex_num:02d}-exercise.yaml")
            filepath = os.path.join(mod_dir, filename)

            yaml_content = extract_yaml_from_solution(mod_num, ex_num, sol['content_html'])

            # Validar con PyYAML
            try:
                list(yaml.safe_load_all(yaml_content))
            except Exception as e:
                errors.append(f"Error parseando YAML en {dir_name}/{filename}: {e}")

            # Agregar encabezado explicativo con metadatos
            header = f"""# =============================================================================
# Modulo {mod_num:02d}: {mod['name']}
# Ejercicio {mod_num}.{ex_num}: {sol['title']}
# Namespace Asignado: {mod['ns']}
# =============================================================================
"""
            full_file_content = header + yaml_content + "\n"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_file_content)

            exported_count += 1

    print(f"✓ Total de manifiestos generados exitosamente: {exported_count}/42 en 14 módulos.")
    if errors:
        print(f"ADVERTENCIAS DE SINTAXIS YAML ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("✓ Todos los 42 archivos YAML fueron validados sintácticamente con éxito.")
        return True


if __name__ == "__main__":
    success = export_all_manifests()
    sys.exit(0 if success else 1)
