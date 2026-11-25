# =============================================================================
# scripts/modules_net_sec.py
# Módulos 11 y 12: Ingress & RBAC
# =============================================================================

MODULE_INGRESS = {
    "id": "ingress",
    "num": "11",
    "name": "Ingress: Controladores de Enrutamiento HTTP/HTTPS",
    "ns": "lab-ingress",
    "description": "El recurso Ingress gestiona el acceso externo a los servicios del clúster proporcionando balanceo de carga HTTP/S, enrutamiento basado en paths/hosts y terminación SSL/TLS mediante un único punto de entrada.",
    "exercises": [
        {
            "id": "ex-11-1",
            "sol_id": "sol-11-1",
            "num": "Ejercicio 11.1:",
            "title": "Enrutamiento Basado en Rutas URL (Path-based Routing)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Una plataforma web dispone de dos microservicios: `/catalog` y `/orders`. Ambos deben ser accesibles a través de la misma dirección IP pública enrutando según el prefijo de la URL.",
            "requirements": [
                "Crear el namespace <code>lab-ingress</code>.",
                "Desplegar dos aplicaciones independientes: <code>deploy-catalog</code> (puerto 80) y <code>deploy-orders</code> (puerto 80).",
                "Crear sus respectivos servicios ClusterIP: <code>svc-catalog</code> y <code>svc-orders</code>.",
                "Crear un recurso Ingress llamado <code>ingress-path-routing</code> con <code>ingressClassName: nginx</code>.",
                "Configurar reglas para redirigir <code>/catalog</code> hacia <code>svc-catalog:80</code> y <code>/orders</code> hacia <code>svc-orders:80</code> usando <code>pathType: Prefix</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl describe ingress -n lab-ingress ingress-path-routing</code> y comprobar que las dos rutas están correctamente mapeadas a sus respectivos servicios y puertos.</p>"
        },
        {
            "id": "ex-11-2",
            "sol_id": "sol-11-2",
            "num": "Ejercicio 11.2:",
            "title": "Enrutamiento Basado en Nombres de Dominio (Virtual Host Routing)",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Una misma empresa aloja dos dominios distintos en el clúster: `tienda.example.com` y `admin.example.com`. El Ingress debe inspeccionar la cabecera HTTP Host y dirigir la petición al servicio correspondiente.",
            "requirements": [
                "Crear un Ingress llamado <code>ingress-vhost-routing</code> en <code>lab-ingress</code>.",
                "Regla 1: host <code>tienda.example.com</code> enruta a <code>svc-catalog:80</code>.",
                "Regla 2: host <code>admin.example.com</code> enruta a <code>svc-orders:80</code>.",
                "Probar la resolución emulando las cabeceras HTTP con <code>curl -H 'Host: tienda.example.com'</code>."
            ],
            "verification": "<p>Ejecutar <code>curl -H 'Host: tienda.example.com' http://&lt;INGRESS-IP&gt;/</code> y comprobar que responde el servicio de catálogo, y con <code>Host: admin.example.com</code> responde el de administración.</p>"
        },
        {
            "id": "ex-11-3",
            "sol_id": "sol-11-3",
            "num": "Ejercicio 11.3:",
            "title": "Terminación TLS Segura en Ingress con Secret Asociado",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Todo el tráfico externo hacia `tienda.example.com` debe viajar cifrado por HTTPS. El Ingress Controller debe encargarse de la terminación TLS utilizando un certificado almacenado en un Secret de Kubernetes.",
            "requirements": [
                "Generar certificado y clave SSL autofirmados para el dominio <code>tienda.example.com</code>.",
                "Crear el Secret TLS <code>sec-ingress-tls</code> en el namespace <code>lab-ingress</code>.",
                "Añadir la sección <code>tls</code> en el recurso Ingress vinculando el host <code>tienda.example.com</code> con el Secret <code>sec-ingress-tls</code>.",
                "Verificar la respuesta segura con <code>curl -k https://tienda.example.com</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl get ingress -n lab-ingress ingress-vhost-routing</code> y comprobar que la columna <code>PORTS</code> muestra <code>80, 443</code> y que curl conecta por el puerto 443.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-11-1",
            "ex_id": "ex-11-1",
            "num": "Solución 11.1:",
            "title": "Enrutamiento Basado en Rutas URL (Path-based Routing)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los Ingress utilizan controladores (como ingress-nginx o traefik). Con <code>pathType: Prefix</code>, cualquier ruta que comience por el prefijo indicado es capturada y redirigida al backend correspondiente.</p>

<p><strong>Manifiesto YAML Completo:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-ingress
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-catalog
  namespace: lab-ingress
spec:
  replicas: 1
  selector:
    matchLabels: { app: catalog }
  template:
    metadata: { labels: { app: catalog } }
    spec:
      containers:
        - name: web
          image: hashicorp/http-echo:latest
          args: ["-text=Modulo Catalogo", "-listen=:80"]
---
apiVersion: v1
kind: Service
metadata:
  name: svc-catalog
  namespace: lab-ingress
spec:
  selector: { app: catalog }
  ports: [{ port: 80, targetPort: 80 }]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-orders
  namespace: lab-ingress
spec:
  replicas: 1
  selector:
    matchLabels: { app: orders }
  template:
    metadata: { labels: { app: orders } }
    spec:
      containers:
        - name: web
          image: hashicorp/http-echo:latest
          args: ["-text=Modulo Pedidos", "-listen=:80"]
---
apiVersion: v1
kind: Service
metadata:
  name: svc-orders
  namespace: lab-ingress
spec:
  selector: { app: orders }
  ports: [{ port: 80, targetPort: 80 }]
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-path-routing
  namespace: lab-ingress
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /catalog
            pathType: Prefix
            backend:
              service:
                name: svc-catalog
                port:
                  number: 80
          - path: /orders
            pathType: Prefix
            backend:
              service:
                name: svc-orders
                port:
                  number: 80</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f ingress-path.yaml
kubectl describe ingress -n lab-ingress ingress-path-routing</code></pre>
"""
        },
        {
            "id": "sol-11-2",
            "ex_id": "ex-11-2",
            "num": "Solución 11.2:",
            "title": "Enrutamiento Basado en Nombres de Dominio (Virtual Host Routing)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Al incluir la clave <code>host</code> en cada regla, el Ingress Controller examina el encabezado HTTP <code>Host</code> de la petición HTTP/1.1 o la extensión SNI en conexiones TLS.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-vhost-routing
  namespace: lab-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: tienda.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: svc-catalog
                port:
                  number: 80
    - host: admin.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: svc-orders
                port:
                  number: 80</code></pre>

<p><strong>Validación con curl:</strong></p>
<pre><code>kubectl apply -f ingress-vhost.yaml
# Obtener IP del Ingress
INGRESS_IP=$(kubectl get ingress -n lab-ingress ingress-vhost-routing \\
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
# Si estás en un lab sin LoadBalancer, usa localhost o la IP de tu nodo
curl -H "Host: tienda.example.com" http://${INGRESS_IP:-localhost}/
curl -H "Host: admin.example.com" http://${INGRESS_IP:-localhost}/</code></pre>
"""
        },
        {
            "id": "sol-11-3",
            "ex_id": "ex-11-3",
            "num": "Solución 11.3:",
            "title": "Terminación TLS Segura en Ingress con Secret Asociado",
            "content_html": """
<p><strong>Explicación Técnica:</strong> La sección <code>tls</code> mapea hosts específicos a un Secret de tipo <code>kubernetes.io/tls</code>. El Ingress Controller se encarga del handshake SSL, descargando de esa tarea de cómputo a los microservicios backend.</p>

<p><strong>Comandos y Manifiesto YAML:</strong></p>
<pre><code># 1. Crear certificado SSL autofirmado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\
  -keyout /tmp/tienda.key -out /tmp/tienda.crt -subj "/CN=tienda.example.com"

# 2. Crear Secret en el mismo namespace del Ingress
kubectl create secret tls sec-ingress-tls -n lab-ingress \\
  --cert=/tmp/tienda.crt --key=/tmp/tienda.key</code></pre>

<p><strong>Manifiesto con TLS habilitado:</strong></p>
<pre><code>apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-tls-secure
  namespace: lab-ingress
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - tienda.example.com
      secretName: sec-ingress-tls
  rules:
    - host: tienda.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: svc-catalog
                port:
                  number: 80</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f ingress-tls.yaml
curl -k -v --resolve tienda.example.com:443:127.0.0.1 https://tienda.example.com/</code></pre>
"""
        }
    ]
}

MODULE_RBAC = {
    "id": "rbac",
    "num": "12",
    "name": "RBAC: Control de Acceso Basado en Roles y Cuentas de Servicio",
    "ns": "lab-rbac",
    "description": "RBAC (Role-Based Access Control) regula el acceso a los endpoints del API Server de Kubernetes aplicando el principio de mínimo privilegio mediante ServiceAccounts, Roles, ClusterRoles y RoleBindings.",
    "exercises": [
        {
            "id": "ex-12-1",
            "sol_id": "sol-12-1",
            "num": "Ejercicio 12.1:",
            "title": "Creación de ServiceAccount Dedicada y Endurecimiento de Tokens",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Por directivas del CIS Benchmark para Kubernetes, los Pods que no requieran consultar el API Server deben tener deshabilitado el montaje automático de credenciales para evitar que atacantes exploten el token de la cuenta de servicio.",
            "requirements": [
                "Crear el namespace <code>lab-rbac</code>.",
                "Crear una ServiceAccount llamada <code>sa-limited-app</code> en <code>lab-rbac</code>.",
                "Configurar en la ServiceAccount <code>automountServiceAccountToken: false</code>.",
                "Desplegar un Pod <code>pod-secure-sa</code> que utilice dicha ServiceAccount.",
                "Comprobar que el directorio <code>/var/run/secrets/kubernetes.io/serviceaccount</code> NO existe dentro del contenedor."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-rbac pod-secure-sa -- ls -d /var/run/secrets/kubernetes.io/serviceaccount</code> y verificar que devuelve error 'No such file or directory'.</p>"
        },
        {
            "id": "ex-12-2",
            "sol_id": "sol-12-2",
            "num": "Ejercicio 12.2:",
            "title": "Definición de Role con Privilegios Mínimos (Least Privilege)",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Un operador júnior sólo debe tener permisos para inspeccionar y ver logs de Pods y consultar Deployments dentro del namespace `lab-rbac`, pero tiene terminantemente prohibido crear, modificar o eliminar recursos.",
            "requirements": [
                "Crear un recurso <code>Role</code> llamado <code>role-pod-viewer</code> en <code>lab-rbac</code>.",
                "Permitir sobre el apiGroup <code>\"\"</code> (core) y recursos <code>[\"pods\", \"pods/log\"]</code> exclusivamente los verbos: <code>[\"get\", \"list\", \"watch\"]</code>.",
                "Permitir sobre el apiGroup <code>\"apps\"</code> y recursos <code>[\"deployments\"]</code> exclusivamente los verbos: <code>[\"get\", \"list\"]</code>.",
                "Verificar la correcta sintaxis y validación en el clúster."
            ],
            "verification": "<p>Ejecutar <code>kubectl describe role -n lab-rbac role-pod-viewer</code> y verificar la tabla de reglas y permisos asignados.</p>"
        },
        {
            "id": "ex-12-3",
            "sol_id": "sol-12-3",
            "num": "Ejercicio 12.3:",
            "title": "RoleBinding y Comprobación con kubectl auth can-i",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Vincular la ServiceAccount creada en el ejercicio 12.1 con el Role del ejercicio 12.2 mediante un RoleBinding y certificar formalmente los permisos utilizando la herramienta de simulación de identidad `kubectl auth can-i`.",
            "requirements": [
                "Crear un <code>RoleBinding</code> llamado <code>rb-pod-viewer-binding</code> en <code>lab-rbac</code>.",
                "Vincular el Role <code>role-pod-viewer</code> con la ServiceAccount <code>sa-limited-app</code> en <code>lab-rbac</code>.",
                "Verificar si la ServiceAccount puede listar Pods en <code>lab-rbac</code> (debe devolver 'yes').",
                "Verificar si la ServiceAccount puede eliminar Pods en <code>lab-rbac</code> (debe devolver 'no').",
                "Verificar si la ServiceAccount tiene permisos en otro namespace como <code>default</code> (debe devolver 'no')."
            ],
            "verification": "<p>Ejecutar <code>kubectl auth can-i list pods -n lab-rbac --as=system:serviceaccount:lab-rbac:sa-limited-app</code> y verificar que responde <code>yes</code>.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-12-1",
            "ex_id": "ex-12-1",
            "num": "Solución 12.1:",
            "title": "Creación de ServiceAccount Dedicada y Endurecimiento de Tokens",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Por defecto, cada Pod monta automáticamente el token JWT de su ServiceAccount. Si un Pod sufre una vulnerabilidad de ejecución remota de código (RCE), el atacante podría utilizar dicho token para hablar con el API Server. Deshabilitarlo con <code>automountServiceAccountToken: false</code> mitiga este vector de ataque.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-rbac
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sa-limited-app
  namespace: lab-rbac
automountServiceAccountToken: false
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-secure-sa
  namespace: lab-rbac
spec:
  serviceAccountName: sa-limited-app
  containers:
    - name: app
      image: alpine:3.19
      command: ["/bin/sh", "-c", "sleep 3600"]</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f sa-hardened.yaml
kubectl exec -n lab-rbac pod-secure-sa -- \\
  ls -la /var/run/secrets/kubernetes.io/serviceaccount 2&gt;&amp;1
# Confirmar que la ruta no existe</code></pre>
"""
        },
        {
            "id": "sol-12-2",
            "ex_id": "ex-12-2",
            "num": "Solución 12.2:",
            "title": "Definición de Role con Privilegios Mínimos (Least Privilege)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los Roles se circunscriben estrictamente a un namespace específico (a diferencia de los ClusterRoles que abarcan todo el clúster o recursos sin namespace como Nodos o PVs). Los sub-recursos (como <code>pods/log</code> o <code>pods/exec</code>) deben especificarse explícitamente.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-pod-viewer
  namespace: lab-rbac
rules:
  - apiGroups: [""] # "" indica el apiGroup core
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list"]</code></pre>

<p><strong>Comando Imperativo Rápido (Truco CKA):</strong></p>
<pre><code>kubectl create role role-pod-viewer -n lab-rbac \\
  --verb=get,list,watch --resource=pods,pods/log \\
  --dry-run=client -o yaml &gt; role.yaml</code></pre>
"""
        },
        {
            "id": "sol-12-3",
            "ex_id": "ex-12-3",
            "num": "Solución 12.3:",
            "title": "RoleBinding y Comprobación con kubectl auth can-i",
            "content_html": """
<p><strong>Explicación Técnica:</strong> El <code>RoleBinding</code> une el sujeto (usuario, grupo o ServiceAccount) con el <code>Role</code> deseado. El comando <code>kubectl auth can-i</code> permite validar autorizaciones impersonando a cualquier identidad del sistema mediante la sintaxis <code>system:serviceaccount:&lt;namespace&gt;:&lt;nombre-sa&gt;</code>.</p>

<p><strong>Manifiesto YAML del RoleBinding:</strong></p>
<pre><code>apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rb-pod-viewer-binding
  namespace: lab-rbac
subjects:
  - kind: ServiceAccount
    name: sa-limited-app
    namespace: lab-rbac
roleRef:
  kind: Role
  name: role-pod-viewer
  apiGroup: rbac.authorization.k8s.io</code></pre>

<p><strong>Auditoría de Permisos con kubectl auth can-i (Fundamental en CKA):</strong></p>
<pre><code># 1. Aplicar RoleBinding
kubectl apply -f rb-viewer.yaml

# 2. Comprobar que PUEDE listar pods en lab-rbac -> Devuelve "yes"
kubectl auth can-i list pods -n lab-rbac \\
  --as=system:serviceaccount:lab-rbac:sa-limited-app

# 3. Comprobar que NO PUEDE borrar pods en lab-rbac -> Devuelve "no"
kubectl auth can-i delete pods -n lab-rbac \\
  --as=system:serviceaccount:lab-rbac:sa-limited-app

# 4. Comprobar que NO TIENE acceso en default -> Devuelve "no"
kubectl auth can-i list pods -n default \\
  --as=system:serviceaccount:lab-rbac:sa-limited-app</code></pre>
"""
        }
    ]
}

MODULES_NET_SEC = [MODULE_INGRESS, MODULE_RBAC]
