# =============================================================================
# scripts/content_data.py
# Unificación de Metadatos, Resumen Metodológico y los 14 Módulos de Ejercicios
# =============================================================================
from modules_fundamentos import MODULES_FUNDAMENTOS
from modules_config_storage import MODULES_CONFIG_STORAGE
from modules_advanced import MODULES_ADVANCED
from modules_net_sec import MODULES_NET_SEC
from modules_packaging import MODULES_PACKAGING

METADATA = {
    "title": "Cuaderno de Ejercicios y Solucionario Técnico de Kubernetes",
    "title_part1": "Guía Práctica Avanzada de",
    "title_part2": "Kubernetes",
    "subtitle": "42 Ejercicios Prácticos y Solucionario Técnico para Administradores y Preparación CKA/CKAD",
    "description": "Manual intensivo de laboratorio diseñado para la capacitación práctica y resolución de problemas en clústeres de Kubernetes. Cubre los 12 recursos core esenciales del orquestador junto a las herramientas estándar de empaquetado y personalización declarativa (Helm y Kustomize), con niveles de dificultad explícitos, aislamiento por namespaces y navegación cruzada bidireccional.",
    "author": "Curso de Especialización Kubernetes & CKA Labs",
    "version": "1.28+",
    "date": "Noviembre 2026"
}

SUMMARY_TEXT = """
<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; margin-top: 15px;">
  <h3 style="color: #0f172a; margin-top: 0; font-size: 11pt;">Enfoque Pedagógico y Metodología de Resolución</h3>
  <p>
    Este cuaderno de ejercicios ha sido estructurado para ofrecer una inmersión técnica directa en la administración, configuración, aseguramiento y despliegue de cargas de trabajo sobre <strong>Kubernetes</strong>.
  </p>
  <p>
    El documento se divide estrictamente en dos secciones complementarias:
  </p>
  <ol>
    <li>
      <strong>Sección I (Cuaderno de Ejercicios):</strong> Presenta los 42 retos organizados en 14 bloques temáticos. Cada ejercicio expone un escenario de negocio o arquitectura real, la lista de requerimientos técnicos formales (nombres, puertos, etiquetas, políticas) y un procedimiento de verificación esperado. Al final de cada reto, el alumno dispone de un enlace interactivo directo hacia su solución.
    </li>
    <li>
      <strong>Sección II (Solucionario Técnico y Guías de Validación):</strong> Proporciona la resolución exhaustiva de cada problema, incluyendo los manifiestos YAML oficiales y comentados línea por línea, atajos imperativos con <code>kubectl</code> / <code>helm</code> para exámenes de certificación, pasos de comprobación y una sección especial de <em>Trampas CKA / Errores Comunes</em>. Cada solución incluye un enlace de retorno al enunciado original.
    </li>
  </ol>

  <h4 style="color: #1e3a8a; margin-top: 14px; margin-bottom: 6px; font-size: 9.5pt;">Aislamiento por Namespaces Temáticos</h4>
  <p>
    Para evitar conflictos entre recursos, garantizar la reproducibilidad y permitir que varios alumnos o módulos convivan en un mismo clúster, cada bloque temático opera en su propio namespace aislado:
  </p>
  <table style="margin-top: 6px;">
    <thead>
      <tr>
        <th>Módulo / Recurso</th>
        <th>Namespace Asignado</th>
        <th>Comando de Creación Rápida</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>1. Pods</td><td><code>lab-pods</code></td><td><code>kubectl create ns lab-pods</code></td></tr>
      <tr><td>2. ReplicaSets</td><td><code>lab-replicasets</code></td><td><code>kubectl create ns lab-replicasets</code></td></tr>
      <tr><td>3. Deployments</td><td><code>lab-deployments</code></td><td><code>kubectl create ns lab-deployments</code></td></tr>
      <tr><td>4. Services</td><td><code>lab-services</code></td><td><code>kubectl create ns lab-services</code></td></tr>
      <tr><td>5. ConfigMaps</td><td><code>lab-configmaps</code></td><td><code>kubectl create ns lab-configmaps</code></td></tr>
      <tr><td>6. Secrets</td><td><code>lab-secrets</code></td><td><code>kubectl create ns lab-secrets</code></td></tr>
      <tr><td>7. PersistentVolumes & PVCs</td><td><code>lab-storage</code></td><td><code>kubectl create ns lab-storage</code></td></tr>
      <tr><td>8. Jobs & CronJobs</td><td><code>lab-jobs</code></td><td><code>kubectl create ns lab-jobs</code></td></tr>
      <tr><td>9. DaemonSets</td><td><code>lab-daemonsets</code></td><td><code>kubectl create ns lab-daemonsets</code></td></tr>
      <tr><td>10. StatefulSets</td><td><code>lab-statefulsets</code></td><td><code>kubectl create ns lab-statefulsets</code></td></tr>
      <tr><td>11. Ingress</td><td><code>lab-ingress</code></td><td><code>kubectl create ns lab-ingress</code></td></tr>
      <tr><td>12. RBAC & ServiceAccounts</td><td><code>lab-rbac</code></td><td><code>kubectl create ns lab-rbac</code></td></tr>
      <tr><td>13. Helm Charts</td><td><code>lab-helm</code></td><td><code>kubectl create ns lab-helm</code></td></tr>
      <tr><td>14. Kustomize Overlays</td><td><code>lab-kustomize</code></td><td><code>kubectl create ns lab-kustomize</code></td></tr>
    </tbody>
  </table>

  <h4 style="color: #1e3a8a; margin-top: 14px; margin-bottom: 6px; font-size: 9.5pt;">Categorías de Dificultad</h4>
  <ul>
    <li><span class="difficulty-badge diff-intermedio">Intermedio</span>: Casos de uso comunes de administración, configuración declarativa e imperativa básica.</li>
    <li><span class="difficulty-badge diff-avanzado">Avanzado</span>: Coordinación entre múltiples recursos, ciclo de vida distribuido, mutaciones y overlays complejos.</li>
    <li><span class="difficulty-badge diff-cka">Nivel CKA</span>: Escenarios de examen de certificación CKA/CKAD con alta exigencia de velocidad, resolución de problemas (troubleshooting) y restricciones de seguridad.</li>
  </ul>
</div>
"""

MODULES = (
    MODULES_FUNDAMENTOS +
    MODULES_CONFIG_STORAGE +
    MODULES_ADVANCED +
    MODULES_NET_SEC +
    MODULES_PACKAGING
)
