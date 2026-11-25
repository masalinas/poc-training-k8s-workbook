# =============================================================================
# scripts/modules_config_storage.py
# Módulos 5 a 7: ConfigMaps, Secrets, PersistentVolumes & PVCs
# =============================================================================

MODULE_CONFIGMAPS = {
    "id": "configmaps",
    "num": "5",
    "name": "ConfigMaps: Desacoplamiento de la Configuración",
    "ns": "lab-configmaps",
    "description": "Los ConfigMaps permiten inyectar parámetros de configuración no confidenciales en los Pods, ya sea como variables de entorno, argumentos de línea de comandos o archivos montados en el sistema de ficheros.",
    "exercises": [
        {
            "id": "ex-5-1",
            "sol_id": "sol-5-1",
            "num": "Ejercicio 5.1:",
            "title": "Inyección de Parámetros como Variables de Entorno (individuales y envFrom)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Una aplicación de backend lee sus parámetros de conexión y modo de ejecución desde variables de entorno del sistema. Se deben inyectar parámetros clave de forma limpia usando ConfigMaps.",
            "requirements": [
                "Crear el namespace <code>lab-configmaps</code>.",
                "Crear un ConfigMap llamado <code>cm-app-config</code> con las claves: <code>APP_ENV=production</code>, <code>LOG_LEVEL=info</code> y <code>MAX_CONNECTIONS=100</code>.",
                "Crear un segundo ConfigMap llamado <code>cm-feature-flags</code> con <code>BETA_FEATURE=true</code>.",
                "Crear un Pod <code>pod-config-env</code> que consuma todas las claves de <code>cm-app-config</code> masivamente con <code>envFrom</code> y la clave <code>BETA_FEATURE</code> de forma individual con <code>valueFrom.configMapKeyRef</code>.",
                "El Pod debe usar la imagen <code>busybox:1.36</code> y ejecutar <code>env && sleep 3600</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-configmaps pod-config-env -- env</code> y confirmar que todas las variables (APP_ENV, LOG_LEVEL, MAX_CONNECTIONS y BETA_FEATURE) están presentes con sus valores exactos.</p>"
        },
        {
            "id": "ex-5-2",
            "sol_id": "sol-5-2",
            "num": "Ejercicio 5.2:",
            "title": "Montaje de Archivos de Configuración Completos mediante Volumen",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Se requiere desplegar un servidor Nginx con una configuración virtual host personalizada (`custom-site.conf`) inyectada mediante un ConfigMap sin reconstruir la imagen Docker.",
            "requirements": [
                "Crear un ConfigMap <code>cm-nginx-conf</code> en <code>lab-configmaps</code> que contenga el archivo <code>custom.conf</code> configurando un server en el puerto 8080 con una cabecera personalizada <code>add_header X-Custom-Header 'K8s-Course';</code>.",
                "Crear un Pod <code>pod-nginx-custom</code> montando el ConfigMap como volumen en el directorio <code>/etc/nginx/conf.d</code>.",
                "Verificar que Nginx arranca en el puerto 8080 y responde con la cabecera solicitada."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-configmaps pod-nginx-custom -- wget -S -O - http://localhost:8080</code> y comprobar en la salida que aparece <code>X-Custom-Header: K8s-Course</code>.</p>"
        },
        {
            "id": "ex-5-3",
            "sol_id": "sol-5-3",
            "num": "Ejercicio 5.3:",
            "title": "Montaje Granular con subPath sin Sobreescribir Directorios",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Un contenedor requiere sobreescribir únicamente el archivo `/etc/timezone` o `/etc/resolv.conf.custom` sin borrar ni ocultar los archivos existentes en `/etc`. Un montaje normal de volumen vacía el contenido nativo del directorio en el contenedor.",
            "requirements": [
                "Crear un ConfigMap <code>cm-single-file</code> con una clave llamada <code>my-config.ini</code> con contenido <code>mode=fast</code>.",
                "Crear un Pod <code>pod-subpath-test</code> con imagen <code>alpine:3.19</code>.",
                "Montar únicamente la clave <code>my-config.ini</code> dentro de <code>/etc/my-config.ini</code> utilizando <code>subPath</code>.",
                "Comprobar que <code>/etc/my-config.ini</code> existe y que el resto de archivos estándar de Alpine en <code>/etc</code> (como <code>/etc/hosts</code>, <code>/etc/os-release</code>) permanecen intactos."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-configmaps pod-subpath-test -- ls -la /etc/my-config.ini /etc/os-release</code> y verificar que ambos archivos existen correctamente.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-5-1",
            "ex_id": "ex-5-1",
            "num": "Solución 5.1:",
            "title": "Inyección de Parámetros como Variables de Entorno (individuales y envFrom)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> La directiva <code>envFrom</code> importa automáticamente todas las claves de un ConfigMap como variables de entorno. Cuando se necesita renombrar la variable o extraer una sola clave, se utiliza <code>valueFrom.configMapKeyRef</code>.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-configmaps
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cm-app-config
  namespace: lab-configmaps
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cm-feature-flags
  namespace: lab-configmaps
data:
  BETA_FEATURE: "true"
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-config-env
  namespace: lab-configmaps
spec:
  containers:
    - name: app
      image: busybox:1.36
      command: ["/bin/sh", "-c", "env && sleep 3600"]
      # Importación masiva
      envFrom:
        - configMapRef:
            name: cm-app-config
      # Importación individual
      env:
        - name: BETA_FEATURE
          valueFrom:
            configMapKeyRef:
              name: cm-feature-flags
              key: BETA_FEATURE</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f cm-env.yaml
kubectl exec -n lab-configmaps pod-config-env -- printenv | grep -E "APP_ENV|LOG_LEVEL|MAX_CONNECTIONS|BETA_FEATURE"</code></pre>
"""
        },
        {
            "id": "sol-5-2",
            "ex_id": "ex-5-2",
            "num": "Solución 5.2:",
            "title": "Montaje de Archivos de Configuración Completos mediante Volumen",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Cada clave del diccionario <code>data</code> en un ConfigMap se convierte en un archivo con el mismo nombre dentro del directorio donde se monta el volumen. Las actualizaciones del ConfigMap se sincronizan automáticamente en el Pod cuando se monta como volumen (a diferencia de las variables de entorno, que son estáticas al arranque).</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: ConfigMap
metadata:
  name: cm-nginx-conf
  namespace: lab-configmaps
data:
  custom.conf: |
    server {
        listen 8080;
        location / {
            add_header X-Custom-Header "K8s-Course" always;
            return 200 "Configuracion inyectada exitosamente\\n";
        }
    }
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-nginx-custom
  namespace: lab-configmaps
spec:
  volumes:
    - name: nginx-config-vol
      configMap:
        name: cm-nginx-conf
  containers:
    - name: nginx
      image: nginx:1.25-alpine
      ports:
        - containerPort: 8080
      volumeMounts:
        - name: nginx-config-vol
          mountPath: /etc/nginx/conf.d</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f cm-volume.yaml
# Probar la respuesta HTTP y verificar cabecera
kubectl exec -n lab-configmaps pod-nginx-custom -- wget -S -O - http://localhost:8080</code></pre>
"""
        },
        {
            "id": "sol-5-3",
            "ex_id": "ex-5-3",
            "num": "Solución 5.3:",
            "title": "Montaje Granular con subPath sin Sobreescribir Directorios",
            "content_html": """
<p><strong>Explicación Técnica:</strong> La directiva <code>subPath</code> monta un archivo específico del volumen en lugar de todo el volumen como un directorio. Esto evita el 'enmascaramiento' (shadowing) de los archivos preexistentes en la imagen del contenedor.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: ConfigMap
metadata:
  name: cm-single-file
  namespace: lab-configmaps
data:
  my-config.ini: "mode=fast\\nthreads=4\\n"
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-subpath-test
  namespace: lab-configmaps
spec:
  volumes:
    - name: config-vol
      configMap:
        name: cm-single-file
  containers:
    - name: app
      image: alpine:3.19
      command: ["/bin/sh", "-c", "sleep 3600"]
      volumeMounts:
        - name: config-vol
          mountPath: /etc/my-config.ini
          subPath: my-config.ini</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f cm-subpath.yaml
# Comprobar el contenido del archivo montado
kubectl exec -n lab-configmaps pod-subpath-test -- cat /etc/my-config.ini
# Comprobar que /etc/os-release sigue intacto
kubectl exec -n lab-configmaps pod-subpath-test -- head -n 3 /etc/os-release</code></pre>

<div class="callout callout-warning">
  <div class="callout-title">Gotcha de subPath</div>
  Los archivos montados con <code>subPath</code> NO reciben actualizaciones automáticas en vivo cuando se modifica el ConfigMap en el clúster. El Pod debe ser reiniciado para ver los cambios.
</div>
"""
        }
    ]
}

MODULE_SECRETS = {
    "id": "secrets",
    "num": "6",
    "name": "Secrets: Gestión Segura de Datos Sensibles",
    "ns": "lab-secrets",
    "description": "Los Secrets almacenan datos confidenciales como contraseñas, tokens y claves privadas en Base64 o encriptados en etcd. Se abordan Secrets Opaque, permisos restrictivos de archivos y certificados TLS.",
    "exercises": [
        {
            "id": "ex-6-1",
            "sol_id": "sol-6-1",
            "num": "Ejercicio 6.1:",
            "title": "Creación de Secret Opaque (Base64) y Consumo Seguro en Variables",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Para conectar un microservicio a una base de datos MySQL se deben almacenar el usuario y la contraseña sin exponerlos en texto plano en los manifiestos públicos.",
            "requirements": [
                "Crear el namespace <code>lab-secrets</code>.",
                "Crear un Secret tipo <code>Opaque</code> llamado <code>sec-db-credentials</code>.",
                "Codificar en Base64: <code>DB_USER=app_admin</code> y <code>DB_PASSWORD=S3cr3t_P@ssw0rd!</code>.",
                "Crear un Pod <code>pod-db-client</code> que consuma ambas credenciales como variables de entorno con <code>valueFrom.secretKeyRef</code>.",
                "Probar la decodificación en caliente desde el contenedor."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-secrets pod-db-client -- printenv DB_USER DB_PASSWORD</code> y comprobar que los valores impresos corresponden a los datos originales decodificados.</p>"
        },
        {
            "id": "ex-6-2",
            "sol_id": "sol-6-2",
            "num": "Ejercicio 6.2:",
            "title": "Montaje de Secret como Volumen con Permisos Restringidos (0400)",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Una clave privada SSH o API Key debe montarse como archivo en `/etc/keys/api-key.pem`. Por auditoría de seguridad bancaria, el archivo debe ser de solo lectura para el propietario (`chmod 400`), bloqueando el acceso a otros usuarios.",
            "requirements": [
                "Crear un Secret <code>sec-api-token</code> en <code>lab-secrets</code> con la clave <code>api-token.key</code> conteniendo un token ficticio.",
                "Montar el Secret en un Pod <code>pod-restricted-secret</code> en la ruta <code>/etc/keys</code>.",
                "Configurar en el volumen la propiedad <code>defaultMode: 0400</code> (equivalente a 256 en decimal).",
                "Verificar los permisos del archivo dentro del contenedor con <code>ls -l</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-secrets pod-restricted-secret -- ls -la /etc/keys/api-token.key</code> y verificar que los permisos son exactamente <code>-r--------</code>.</p>"
        },
        {
            "id": "ex-6-3",
            "sol_id": "sol-6-3",
            "num": "Ejercicio 6.3:",
            "title": "Secret de Certificado TLS (kubernetes.io/tls) para Servidor Seguro",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Para habilitar HTTPS en un Ingress o en un servidor web propio, Kubernetes estandariza el tipo de Secret `kubernetes.io/tls`, el cual exige obligatoriamente las claves `tls.crt` y `tls.key`.",
            "requirements": [
                "Generar un par de certificado y clave privada autofirmados usando <code>openssl</code> para el dominio <code>test.local</code>.",
                "Crear un Secret llamado <code>sec-tls-cert</code> en <code>lab-secrets</code> de tipo <code>kubernetes.io/tls</code> usando <code>kubectl create secret tls</code>.",
                "Desplegar un Pod Nginx configurado con SSL que monte dicho Secret en <code>/etc/nginx/certs</code>.",
                "Realizar una petición HTTPS con curl verificando el certificado."
            ],
            "verification": "<p>Ejecutar <code>kubectl describe secret -n lab-secrets sec-tls-cert</code> y comprobar que el tipo es <code>kubernetes.io/tls</code> y contiene las claves <code>tls.crt</code> y <code>tls.key</code>.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-6-1",
            "sol_id": "sol-6-1",
            "ex_id": "ex-6-1",
            "num": "Solución 6.1:",
            "title": "Creación de Secret Opaque (Base64) y Consumo Seguro en Variables",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los valores en un Secret Opaque deben codificarse con <code>base64</code> (o bien utilizar <code>stringData</code> en el manifiesto para que Kubernetes los codifique automáticamente).</p>

<p><strong>Generación Imperativa y Manifiesto YAML:</strong></p>
<pre><code># 1. Crear namespace y Secret de forma imperativa (Truco CKA)
kubectl create namespace lab-secrets
kubectl create secret generic sec-db-credentials -n lab-secrets \\
  --from-literal=DB_USER='app_admin' \\
  --from-literal=DB_PASSWORD='S3cr3t_P@ssw0rd!'</code></pre>

<p><strong>Manifiesto del Pod Consumidor:</strong></p>
<pre><code>apiVersion: v1
kind: Pod
metadata:
  name: pod-db-client
  namespace: lab-secrets
spec:
  containers:
    - name: client
      image: busybox:1.36
      command: ["/bin/sh", "-c", "sleep 3600"]
      env:
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: sec-db-credentials
              key: DB_USER
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: sec-db-credentials
              key: DB_PASSWORD</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f pod-secret-env.yaml
kubectl exec -n lab-secrets pod-db-client -- env | grep DB_</code></pre>
"""
        },
        {
            "id": "sol-6-2",
            "ex_id": "ex-6-2",
            "num": "Solución 6.2:",
            "title": "Montaje de Secret como Volumen con Permisos Restringidos (0400)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> En YAML, los números que empiezan por 0 se interpretan en base octal en especificaciones POSIX. Con <code>defaultMode: 0400</code>, sólo el usuario UID del proceso contenedor tendrá permisos de lectura (<code>r--------</code>), previniendo fugas entre usuarios del sistema operativo.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Secret
metadata:
  name: sec-api-token
  namespace: lab-secrets
type: Opaque
stringData:
  api-token.key: >-
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.token-secreto-de-produccion
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-restricted-secret
  namespace: lab-secrets
spec:
  volumes:
    - name: secret-volume
      secret:
        secretName: sec-api-token
        defaultMode: 0400 # Permiso de solo lectura para el dueño
  containers:
    - name: secure-app
      image: alpine:3.19
      command: ["/bin/sh", "-c", "sleep 3600"]
      volumeMounts:
        - name: secret-volume
          mountPath: /etc/keys
          readOnly: true</code></pre>

<p><strong>Validación de Permisos:</strong></p>
<pre><code>kubectl apply -f secret-permissions.yaml
kubectl exec -n lab-secrets pod-restricted-secret -- \\
  ls -la /etc/keys/api-token.key
# Salida esperada: -r--------    1 root     root</code></pre>
"""
        },
        {
            "id": "sol-6-3",
            "ex_id": "ex-6-3",
            "num": "Solución 6.3:",
            "title": "Secret de Certificado TLS (kubernetes.io/tls) para Servidor Seguro",
            "content_html": """
<p><strong>Explicación Técnica:</strong> El tipo <code>kubernetes.io/tls</code> valida automáticamente que los datos proporcionados correspondan a una clave privada y un certificado X.509 válidos.</p>

<p><strong>Generación del Certificado y Creación del Secret:</strong></p>
<pre><code># 1. Generar par de certificados SSL autofirmados
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\
  -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=test.local/O=k8s-lab"

# 2. Crear el Secret nativo TLS en Kubernetes
kubectl create secret tls sec-tls-cert -n lab-secrets \\
  --cert=/tmp/tls.crt \\
  --key=/tmp/tls.key

# 3. Comprobar metadata y formato del secret
kubectl get secret -n lab-secrets sec-tls-cert -o yaml</code></pre>

<div class="callout callout-tip">
  <div class="callout-title">Atajo Imperativo CKA</div>
  Nunca codifiques manualmente en Base64 certificados multilínea en YAML en un examen: el comando imperativo <code>kubectl create secret tls &lt;nombre&gt; --cert=... --key=...</code> es 10 veces más rápido y libre de errores de sangrado.
</div>
"""
        }
    ]
}

MODULE_STORAGE = {
    "id": "storage",
    "num": "7",
    "name": "Almacenamiento Persistente: PV y PVC",
    "ns": "lab-storage",
    "description": "El subsistema PersistentVolume (PV) y PersistentVolumeClaim (PVC) desacopla la infraestructura física de almacenamiento del consumo realizado por las aplicaciones de los desarrolladores.",
    "exercises": [
        {
            "id": "ex-7-1",
            "sol_id": "sol-7-1",
            "num": "Ejercicio 7.1:",
            "title": "Definición de PersistentVolume Estático (HostPath) con Política Retain",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "El administrador de sistemas necesita aprovisionar estáticamente un volumen de almacenamiento en disco local de 2Gi en el nodo con política de reciclado Retain para salvaguardar los datos ante eventuales borrados del claim.",
            "requirements": [
                "Crear un PersistentVolume llamado <code>pv-local-2gi</code> a nivel de clúster.",
                "Capacidad: <code>2Gi</code>, AccessModes: <code>ReadWriteOnce</code>.",
                "Tipo de almacenamiento: <code>hostPath</code> apuntando a <code>/mnt/k8s-data</code> en el nodo.",
                "Configurar <code>persistentVolumeReclaimPolicy: Retain</code> y <code>storageClassName: manual</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pv pv-local-2gi</code> y comprobar que su estado es <code>Available</code> y su política es <code>Retain</code>.</p>"
        },
        {
            "id": "ex-7-2",
            "sol_id": "sol-7-2",
            "num": "Ejercicio 7.2:",
            "title": "Enlace Exitoso de PersistentVolumeClaim (Bound) por Atributos",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Un desarrollador necesita reclamar 1Gi de almacenamiento en el namespace `lab-storage` que enlace contra el volumen estático aprovisionado por el administrador.",
            "requirements": [
                "Crear el namespace <code>lab-storage</code>.",
                "Crear un PersistentVolumeClaim <code>pvc-data-claim</code> en <code>lab-storage</code>.",
                "Petición de almacenamiento: <code>1Gi</code>, AccessModes: <code>ReadWriteOnce</code>.",
                "Especificar <code>storageClassName: manual</code> para forzar el binding con el PV manual.",
                "Verificar la transición de estado del PVC de <code>Pending</code> a <code>Bound</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pvc -n lab-storage pvc-data-claim</code> y verificar que el status es <code>Bound</code> y apunta al volumen <code>pv-local-2gi</code>.</p>"
        },
        {
            "id": "ex-7-3",
            "sol_id": "sol-7-3",
            "num": "Ejercicio 7.3:",
            "title": "Persistencia de Datos entre el Ciclo de Vida de Pods Diferentes",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Demostrar que los datos almacenados en el PVC sobreviven al ciclo de vida efímero de los Pods. Un primer Pod escribirá un archivo con la fecha, se eliminará el Pod, y un segundo Pod leerá el archivo verificando su persistencia.",
            "requirements": [
                "Crear un Pod <code>pod-writer</code> en <code>lab-storage</code> montando <code>pvc-data-claim</code> en <code>/data</code>. Debe escribir un archivo <code>/data/persist.txt</code> con el texto 'DATOS_PERSISTIDOS_OK'.",
                "Eliminar el Pod <code>pod-writer</code> y esperar a su completa terminación.",
                "Crear un nuevo Pod <code>pod-reader</code> en <code>lab-storage</code> montando el mismo PVC en <code>/data</code>.",
                "Leer el contenido de <code>/data/persist.txt</code> desde el nuevo Pod."
            ],
            "verification": "<p>Ejecutar <code>kubectl exec -n lab-storage pod-reader -- cat /data/persist.txt</code> y verificar que devuelve 'DATOS_PERSISTIDOS_OK'.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-7-1",
            "ex_id": "ex-7-1",
            "num": "Solución 7.1:",
            "title": "Definición de PersistentVolume Estático (HostPath) con Política Retain",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los PersistentVolumes son recursos a nivel de clúster (no pertenecen a ningún namespace). La política <code>Retain</code> garantiza que cuando el PVC se elimine, el PV pasa al estado <code>Released</code> y los datos no se borran del disco físico.</p>

<p><strong>Manifiesto YAML del PV:</strong></p>
<pre><code>apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-local-2gi
spec:
  capacity:
    storage: 2Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /mnt/k8s-data
    type: DirectoryOrCreate</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f pv-hostpath.yaml
kubectl get pv pv-local-2gi</code></pre>
"""
        },
        {
            "id": "sol-7-2",
            "ex_id": "ex-7-2",
            "num": "Solución 7.2:",
            "title": "Enlace Exitoso de PersistentVolumeClaim (Bound) por Atributos",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Kubernetes enlaza un PVC con un PV cuando coinciden: la <code>storageClassName</code>, los <code>accessModes</code> y el PV ofrece una capacidad igual o superior a la requerida por el PVC.</p>

<p><strong>Manifiesto YAML del PVC:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-storage
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-data-claim
  namespace: lab-storage
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  resources:
    requests:
      storage: 1Gi</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f pvc.yaml
kubectl get pvc -n lab-storage pvc-data-claim
# STATUS debe ser Bound y VOLUME debe indicar pv-local-2gi</code></pre>
"""
        },
        {
            "id": "sol-7-3",
            "ex_id": "ex-7-3",
            "num": "Solución 7.3:",
            "title": "Persistencia de Datos entre el Ciclo de Vida de Pods Diferentes",
            "content_html": """
<p><strong>Explicación Técnica:</strong> A diferencia de <code>emptyDir</code>, los volúmenes respaldados por PVCs son independientes de los Pods y desacoplan los datos del ciclo de vida del contenedor.</p>

<p><strong>Fase 1: Pod de Escritura:</strong></p>
<pre><code>cat &lt;&lt;EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-writer
  namespace: lab-storage
spec:
  volumes:
    - name: storage-vol
      persistentVolumeClaim:
        claimName: pvc-data-claim
  containers:
    - name: writer
      image: busybox:1.36
      command: ["/bin/sh", "-c"]
      args:
        - "echo 'DATOS_PERSISTIDOS_OK' &gt; /data/persist.txt; sleep 3600"
      volumeMounts:
        - name: storage-vol
          mountPath: /data
EOF</code></pre>

<p><strong>Fase 2: Eliminación y Pod de Lectura:</strong></p>
<pre><code># 1. Eliminar pod-writer
kubectl delete pod pod-writer -n lab-storage

# 2. Desplegar pod-reader montando el mismo PVC
cat &lt;&lt;EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-reader
  namespace: lab-storage
spec:
  volumes:
    - name: storage-vol
      persistentVolumeClaim:
        claimName: pvc-data-claim
  containers:
    - name: reader
      image: busybox:1.36
      command: ["/bin/sh", "-c", "sleep 3600"]
      volumeMounts:
        - name: storage-vol
          mountPath: /data
EOF

# 3. Comprobar que los datos persisten
kubectl exec -n lab-storage pod-reader -- cat /data/persist.txt</code></pre>
"""
        }
    ]
}

MODULES_CONFIG_STORAGE = [MODULE_CONFIGMAPS, MODULE_SECRETS, MODULE_STORAGE]
