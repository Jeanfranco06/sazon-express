# Sazón Express — Gestión Centralizada de Microservicios con Spring Cloud Config Server

Proyecto académico universitario orientado a demostrar la **centralización, externalización y actualización dinámica de configuraciones** para una arquitectura de microservicios sin persistencia en base de datos, integrando **Spring Cloud Config Server**, **Git** y **Spring Boot Actuator**.

---

## 1. Descripción General

**Sazón Express** es un sistema backend para la gestión operativa y comercial de un restaurante criollo. El sistema está conformado por tres microservicios de negocio independientes (`menu-service`, `pedido-service` y `promocion-service`) cuyas políticas operativas, parámetros de negocio y puertos de red son gestionados centralizadamente por un servidor `config-server` conectado a un repositorio Git dedicado (`config-repo`).

---

## 2. Objetivos del Proyecto

1. **Centralización total:** Eliminar archivos de propiedades dispersos y duplicados en los microservicios.
2. **Versionamiento y trazabilidad:** Administrar la configuración como código (Configuration-as-Code) utilizando Git como única fuente de la verdad (*Single Source of Truth*).
3. **Actualización dinámica en caliente:** Modificar reglas del negocio en Git y propagarlas a los microservicios en tiempo de ejecución mediante `@RefreshScope` y `POST /actuator/refresh` sin necesidad de reiniciar instancias ni recompilar código Java.
4. **Cero persistencia externa:** Operar en memoria (`Collections`, `ConcurrentHashMap`) sin bases de datos (SQL/NoSQL) para enfocar la evaluación exclusivamente en la gestión de configuración distribuida.
5. **Reproducibilidad absoluta:** Asegurar la compilación, despliegue y demostración desde cero en cualquier computadora mediante scripts de PowerShell y pruebas automatizadas.

---

## 3. Arquitectura del Sistema

```text
               +-------------------------------------------+
               |     Repositorio Git: config-repo          |
               |  (application.yml, menu-service.yml,      |
               |   pedido-service.yml, promocion-service)  |
               +---------------------+---------------------+
                                     |
                                     | JGit / Git Protocol (file:// o https://)
                                     v
               +-------------------------------------------+
               |        Spring Cloud Config Server         |
               |               (:8888)                     |
               +---------------------+---------------------+
                                     |
        +----------------------------+----------------------------+
        | HTTP (spring.config.import)|                            |
        v                            v                            v
+------------------+       +-------------------+       +--------------------+
|   menu-service   |       |  pedido-service   |       | promocion-service  |
|     (:8081)      |       |      (:8082)      |       |      (:8083)       |
| Carta y Platos   |       | Gestión de Pedidos|       | Descuentos y Promos|
|   @RefreshScope  |       |   @RefreshScope   |       |   @RefreshScope    |
+------------------+       +-------------------+       +--------------------+
```

### Flujo de Funcionamiento
1. **Arranque:** `config-server` inicializa en el puerto `8888` y enlaza el repositorio Git local o remoto `config-repo`.
2. **Inicialización de Clientes:** Cada microservicio consulta `http://localhost:8888/{application-name}/default` vía `spring.config.import`.
3. **Enlace de Propiedades:** Las propiedades centralizadas se inyectan en componentes anotados con `@ConfigurationProperties` y `@RefreshScope`.
4. **Modificación en Git:** Se realiza un commit de cambio de configuración en `config-repo`.
5. **Recarga en Caliente:** Se envía una petición `POST` al endpoint `/actuator/refresh` del microservicio afectado. El contexto recarga las propiedades actualizadas inmediatamente.

---

## 4. Tecnologías y Versiones Oficiales

| Tecnología | Versión | Justificación Técnica |
|---|---|---|
| **Java** | 17 LTS / 21 LTS | Versión estándar moderna para plataformas empresariales Spring Boot |
| **Spring Boot** | 4.0.9 | Última generación de Spring Boot con soporte optimizado de Jakarta |
| **Spring Cloud** | 2025.1.4 | Tren de liberación compatible oficial para Spring Boot 4.x |
| **Spring Cloud Config Server** | 2025.1.4 | Servidor central con backend JGit integrado |
| **Spring Cloud Config Client** | 2025.1.4 | Cliente con soporte de importación vía `spring.config.import` |
| **Spring Boot Actuator** | 4.0.9 | Exposición del endpoint de recarga en caliente `/actuator/refresh` |
| **Maven** | 3.9+ | Gestor de ciclo de vida, dependencias y reactor multi-módulo |
| **Git** | 2.x | Sistema de control de versiones base para la externalización |
| **JUnit 5 / MockMvc** | 5.x | Suite de pruebas unitarias y de integración REST |
| **PowerShell** | 5.1+ / 7.x | Automatización multiplataforma en entornos Windows para la exposición |

---

## 5. Estructura del Directorio

```text
sazon-express/
├── pom.xml                               # POM agregador raíz (Reactor Maven)
├── .gitignore                            # Exclusión de binarios y temporales
├── config-server/                        # Módulo Servidor de Configuración (:8888)
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/sazonexpress/configserver/
│       │   └── ConfigServerApplication.java
│       ├── main/resources/application.yaml
│       └── test/java/com/sazonexpress/configserver/
│           └── ConfigServerApplicationTests.java
├── menu-service/                         # Microservicio de Menú (:8081)
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/sazonexpress/menu/
│       │   ├── config/MenuProperties.java
│       │   ├── controller/MenuController.java
│       │   ├── model/Plato.java
│       │   ├── service/MenuService.java
│       │   └── MenuServiceApplication.java
│       ├── main/resources/application.yaml
│       └── test/java/com/sazonexpress/menu/
│           └── MenuServiceApplicationTests.java
├── pedido-service/                       # Microservicio de Pedidos (:8082)
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/sazonexpress/pedido/
│       │   ├── config/PedidoProperties.java
│       │   ├── controller/PedidoController.java
│       │   ├── dto/CrearPedidoRequest.java
│       │   ├── model/ItemPedido.java
│       │   ├── model/Pedido.java
│       │   ├── service/PedidoService.java
│       │   └── PedidoServiceApplication.java
│       ├── main/resources/application.yaml
│       └── test/java/com/sazonexpress/pedido/
│           └── PedidoServiceApplicationTests.java
├── promocion-service/                    # Microservicio de Promociones (:8083)
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/sazonexpress/promocion/
│       │   ├── config/PromocionProperties.java
│       │   ├── controller/PromocionController.java
│       │   ├── dto/CalculoDescuentoResponse.java
│       │   ├── model/Promocion.java
│       │   ├── service/PromocionService.java
│       │   └── PromocionServiceApplication.java
│       ├── main/resources/application.yaml
│       └── test/java/com/sazonexpress/promocion/
│           └── PromocionServiceApplicationTests.java
├── config-repo/                          # Repositorio Git independiente
│   ├── .git/                             # Historial de versiones y ramas
│   ├── application.yml                   # Configuración compartida (Actuator/Info)
│   ├── menu-service.yml                  # Configuración de Menú (:8081)
│   ├── pedido-service.yml                # Configuración de Pedidos (:8082)
│   └── promocion-service.yml             # Configuración de Promociones (:8083)
├── scripts/                              # Automatización PowerShell en Windows
│   ├── verificar-entorno.ps1             # Diagnóstico de JDK, Maven, Git y Puertos
│   ├── iniciar-config-server.ps1         # Inicio y sondeo de Config Server
│   ├── iniciar-microservicios.ps1        # Inicio secuencial de los 3 clientes
│   ├── probar-endpoints.ps1              # Pruebas REST completas y guardado de JSON
│   ├── actualizar-configuraciones.ps1    # Demostración del ciclo completo de Refresh
│   └── detener-servicios.ps1             # Detención segura de procesos
└── docs/                                 # Documentación formal y entregables
    ├── Guia_Implementacion_Sazon_Express.pdf
    ├── Presentacion_Sazon_Express.pptx
    └── evidencias/                       # Logs de ejecución y respuestas HTTP reales
```

---

## 6. Endpoints Disponibles y Ejemplos JSON

### 6.1. Spring Cloud Config Server (:8888)
* `GET http://localhost:8888/menu-service/default`
* `GET http://localhost:8888/pedido-service/default`
* `GET http://localhost:8888/promocion-service/default`

**Ejemplo de Respuesta (`GET /menu-service/default`):**
```json
{
  "name": "menu-service",
  "profiles": ["default"],
  "version": "d84a4c1ca80bf249e03b01f85af21675e2358f21",
  "propertySources": [
    {
      "name": "file:///.../config-repo/menu-service.yml",
      "source": {
        "server.port": 8081,
        "restaurante.menu.nombre": "Carta Sazón Express",
        "restaurante.menu.plato-destacado": "Lomo saltado",
        "restaurante.menu.mensaje": "Disfruta nuestros sabores",
        "restaurante.menu.mostrar-disponibles": true
      }
    }
  ]
}
```

### 6.2. Microservicio de Menú (:8081)
* `GET http://localhost:8081/api/menu`: Lista de platos disponibles.
* `GET http://localhost:8081/api/menu/destacado`: Plato destacado configurado centralmente.
* `GET http://localhost:8081/api/menu/configuracion`: Inspección de propiedades inyectadas.
* `POST http://localhost:8081/actuator/refresh`: Endpoint Actuator para recarga en caliente.

**Ejemplo de Respuesta (`GET /api/menu/destacado`):**
```json
{
  "mensaje": "Disfruta nuestros sabores",
  "nombreDestacadoConfigurado": "Lomo saltado",
  "plato": {
    "id": 1,
    "nombre": "Lomo saltado",
    "categoria": "Fondos",
    "precio": 38.00,
    "disponible": true
  }
}
```

### 6.3. Microservicio de Pedidos (:8082)
* `GET http://localhost:8082/api/pedidos`: Lista de pedidos en memoria.
* `POST http://localhost:8082/api/pedidos`: Registro de nuevo pedido con validación de límite centralizado.
* `GET http://localhost:8082/api/pedidos/{id}`: Detalle de pedido por ID.
* `GET http://localhost:8082/api/pedidos/configuracion`: Reglas activas (`max-platos`, `tiempo-estimado-minutos`).
* `POST http://localhost:8082/actuator/refresh`: Endpoint Actuator para recarga en caliente.

**Ejemplo de Solicitud (`POST /api/pedidos`):**
```json
{
  "cliente": "Carlos Ramírez",
  "items": [
    { "plato": "Lomo saltado", "cantidad": 2, "precioUnitario": 38.00 },
    { "plato": "Ceviche clásico", "cantidad": 1, "precioUnitario": 42.00 }
  ]
}
```
**Respuesta Exitosa (HTTP 201 Created):**
```json
{
  "id": 2,
  "cliente": "Carlos Ramírez",
  "totalPlatos": 3,
  "totalMonto": 118.00,
  "estado": "EN_PREPARACION",
  "tiempoEstimadoMinutos": 20,
  "mensajeEstado": "Tu pedido está siendo preparado"
}
```

### 6.4. Microservicio de Promociones (:8083)
* `GET http://localhost:8083/api/promociones`: Catálogo de promociones comerciales.
* `GET http://localhost:8083/api/promociones/destacada`: Promoción destacada configurada.
* `GET http://localhost:8083/api/promociones/calcular?precio=50`: Cálculo monetario con `BigDecimal`.
* `GET http://localhost:8083/api/promociones/configuracion`: Parámetros de descuento centralizados.
* `POST http://localhost:8083/actuator/refresh`: Endpoint Actuator para recarga en caliente.

**Ejemplo de Respuesta (`GET /api/promociones/calcular?precio=50` con 15%):**
```json
{
  "precioOriginal": 50.00,
  "porcentajeDescuentoAplicado": 15,
  "montoDescuento": 7.50,
  "precioFinal": 42.50,
  "promocionesHabilitadas": true,
  "mensaje": "Aprovecha nuestras promociones"
}
```

---

## 7. Demostración de Actualización Dinámica (Paso a Paso)

### Demostración 1: Cambio de Plato Destacado
1. Consultar estado inicial: `GET http://localhost:8081/api/menu/destacado` -> Devuelve `"Lomo saltado"`.
2. Modificar `config-repo/menu-service.yml`:
   ```yaml
   restaurante.menu.plato-destacado: "Ceviche clásico"
   ```
3. Registrar commit en Git:
   ```bash
   git commit -am "feat(menu): cambiar plato destacado a Ceviche clasico"
   ```
4. Aplicar recarga en caliente:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8081/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}"
   ```
5. Consultar de nuevo: `GET http://localhost:8081/api/menu/destacado` -> Devuelve `"Ceviche clásico"`.

### Demostración 2: Reducción del Límite de Platos por Pedido
1. Estado inicial: `max-platos: 5`. Un pedido con 3 platos es aceptado con HTTP 201.
2. Modificar `config-repo/pedido-service.yml` a `max-platos: 2` y hacer commit en Git.
3. Invocar `POST http://localhost:8082/actuator/refresh`.
4. Repetir el pedido de 3 platos -> Es **RECHAZADO con HTTP 400 Bad Request**.
5. Enviar pedido con 2 platos -> Es **ACEPTADO con HTTP 201 Created**.

### Demostración 3: Ajuste Comercial de Porcentaje de Descuento
1. Estado inicial: `descuento-porcentaje: 15`. Consulta `GET /api/promociones/calcular?precio=50` -> Precio final: S/ 42.50.
2. Modificar en Git a `descuento-porcentaje: 20` y hacer commit.
3. Invocar `POST http://localhost:8083/actuator/refresh`.
4. Consultar `GET /api/promociones/calcular?precio=50` -> Precio final calculado: **S/ 40.00**.

---

## 8. Guía de Ejecución Rápida con PowerShell

Para la exposición universitaria, se incluyen scripts listos para ser ejecutados en orden:

```powershell
# 1. Diagnosticar requisitos y puertos
.\scripts\verificar-entorno.ps1

# 2. Iniciar Config Server y esperar disponibilidad
.\scripts\iniciar-config-server.ps1

# 3. Iniciar los 3 microservicios en segundo plano
.\scripts\iniciar-microservicios.ps1

# 4. Probar todos los endpoints y almacenar respuestas JSON
.\scripts\probar-endpoints.ps1

# 5. Ejecutar la demostración de cambios dinámicos desde Git
.\scripts\actualizar-configuraciones.ps1

# 6. (Opcional) Restaurar configuraciones a su estado inicial
.\scripts\actualizar-configuraciones.ps1 -Restaurar

# 7. Detener todos los procesos del sistema al terminar
.\scripts\detener-servicios.ps1
```

---

## 9. Pruebas Automatizadas

El proyecto cuenta con **23 pruebas automatizadas con JUnit 5 y MockMvc** que validan tanto el comportamiento en aislamiento como la integración con las propiedades centralizadas:

* **`config-server` (4 pruebas):** Inicio de contexto, acceso a repositorio Git, resolución de fuentes y recuperación de propiedades de los 3 clientes.
* **`menu-service` (5 pruebas):** Catálogo de platos, plato destacado, endpoint de configuración y recarga dinámica.
* **`pedido-service` (7 pruebas):** Creación válida, rechazo por superar límite, bloqueo por pedidos deshabilitados, recarga de límite y consultas.
* **`promocion-service` (7 pruebas):** Catálogo promocional, cálculo exacto de 15% (S/ 42.50), actualización a 20% (S/ 40.00), validaciones de precios inválidos y estado inactivo.

Para ejecutar todas las pruebas del reactor:
```bash
mvn clean test
```

---

## 10. Problemas Frecuentes y Soluciones

1. **Error `Connection refused: http://localhost:8888` en los clientes:**
   * *Causa:* Los clientes intentaron arrancar antes de que `config-server` estuviese completamente listo.
   * *Solución:* Asegurarse de ejecutar `iniciar-config-server.ps1` primero o verificar que responda en `:8888` antes de iniciar los clientes.
2. **Error `415 Unsupported Media Type` en `/actuator/refresh`:**
   * *Causa:* Llamar a `POST /actuator/refresh` sin cabecera `Content-Type`.
   * *Solución:* Incluir `-ContentType "application/json" -Body "{}"` en PowerShell o `-H "Content-Type: application/json"` en `curl`.
3. **Conflicto de Puertos (`Address already in use`):**
   * *Causa:* Instancias previas de Java quedaron escuchando en los puertos `8888`, `8081`, `8082` u `8083`.
   * *Solución:* Ejecutar `.\scripts\detener-servicios.ps1` para liberar todos los puertos automáticamente.

---

## 11. Limitaciones del Proyecto Académico

1. **Almacenamiento volátil:** Los pedidos registrados residen en memoria RAM (`ConcurrentHashMap`); al reiniciar un microservicio se restablecen al estado inicial.
2. **Puertos estáticos en tiempo de ejecución:** Cambiar el puerto `server.port` en Git requiere reiniciar el proceso cliente, ya que el servidor Tomcat embebido se enlaza durante la fase de inicialización.
3. **Seguridad deshabilitada:** Para efectos didácticos y de exposición ágil, no se requiere autenticación ni tokens OAuth2/JWT para invocar `/actuator/refresh`.

---

## 12. Entregables Académicos y Documentación

En la carpeta [`docs/`](docs/) se encuentran disponibles los materiales oficiales para la presentación y evaluación del proyecto:

1. **Guía de Implementación en Word:** [`docs/Guia_Implementacion_Sazon_Express.docx`](docs/Guia_Implementacion_Sazon_Express.docx) — Miniguía paso a paso en formato editable (.docx) con diagramas, tablas comparativas, fragmentos de código y capturas oficiales de Spring Initializr.
2. **Guía de Implementación en PDF:** [`docs/Guia_Implementacion_Sazon_Express.pdf`](docs/Guia_Implementacion_Sazon_Express.pdf) — Documento imprimible formal con tipografía corporativa y diseño editorial de alta calidad.
3. **Presentación de Diapositivas:** [`docs/Presentacion_Sazon_Express.pptx`](docs/Presentacion_Sazon_Express.pptx) — Presentación oficial de exactamente **8 diapositivas** para la exposición universitaria ante el docente.
4. **Evidencias Reales de Ejecución:** [`docs/evidencias/`](docs/evidencias/) — Respuestas JSON reales y logs generados durante la prueba completa de endpoints y recarga dinámica en caliente.
