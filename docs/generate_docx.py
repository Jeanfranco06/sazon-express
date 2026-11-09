import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, hex_color):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.8)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        <w:left w:val="single" w:sz="12" w:space="0" w:color="0D9488"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
    </w:tcBorders>
    '''
    tcPr.append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def generate_word_guide(output_path, evidencias_dir):
    doc = Document()

    # Configuración de márgenes de página (2.5 cm = ~0.984 pulgadas)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
        # Header y Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "Sazón Express — Guía de Implementación Spring Cloud Config Server"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(100, 116, 139)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Arquitectura de Software y Sistemas Distribuidos | Microservicios con Spring Boot y Git"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    # Colores corporativos y académicos
    COLOR_PRIMARY = RGBColor(30, 58, 138)   # Navy 900
    COLOR_ACCENT = RGBColor(13, 148, 136)   # Teal 600
    COLOR_DARK = RGBColor(15, 23, 42)       # Slate 900
    COLOR_MUTED = RGBColor(71, 85, 105)     # Slate 600

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Arial"
            r_bold.font.size = Pt(10)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.italic = italic
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Arial"
        r_bold.font.size = Pt(10)
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_DARK
        return p

    # -------------------------------------------------------------------------
    # PORTADA / ENCABEZADO FORMAL
    # -------------------------------------------------------------------------
    p_sup = doc.add_paragraph()
    p_sup.paragraph_format.space_after = Pt(4)
    r_sup = p_sup.add_run("GUÍA DE IMPLEMENTACIÓN Y ARQUITECTURA TÉCNICA")
    r_sup.font.name = "Arial"
    r_sup.font.size = Pt(10)
    r_sup.font.bold = True
    r_sup.font.color.rgb = COLOR_ACCENT

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_after = Pt(6)
    r_tit = p_tit.add_run("Spring Cloud Config Server con Tres Microservicios")
    r_tit.font.name = "Arial"
    r_tit.font.size = Pt(22)
    r_tit.font.bold = True
    r_tit.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Caso Práctico: Sazón Express — Centralización, Trazabilidad en Git y Actualización Dinámica (@RefreshScope)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = COLOR_MUTED

    # Tabla de Metadatos
    t_meta = doc.add_table(rows=4, cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_meta.autofit = False

    meta_rows = [
        ("Curso:", "Arquitectura de Software y Sistemas Distribuidos", "Tecnologías:", "Java 17 LTS, Spring Boot 4.0.9, Spring Cloud 2025.1.4"),
        ("Repositorio Sistema:", "https://github.com/Jeanfranco06/sazon-express", "Repositorio Config:", "https://github.com/Jeanfranco06/sazon-express-config"),
        ("Ecosistema:", "4 Módulos independientes + Git Backend + Actuator", "Persistencia:", "Sin Base de Datos (100% en memoria / RAM)"),
        ("Modalidad:", "Demostración Universitaria desde Cero", "Autoría:", "Equipo de Arquitectura Sazón Express")
    ]

    for i, (k1, v1, k2, v2) in enumerate(meta_rows):
        c1, c2 = t_meta.rows[i].cells[0], t_meta.rows[i].cells[1]
        c1.width = Inches(3.4)
        c2.width = Inches(3.4)
        set_cell_background(c1, "EFF6FF")
        set_cell_background(c2, "EFF6FF")
        set_cell_margins(c1, top=80, bottom=80, left=120, right=120)
        set_cell_margins(c2, top=80, bottom=80, left=120, right=120)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1k = p1.add_run(k1 + " ")
        r1k.bold = True
        r1k.font.size = Pt(9)
        r1k.font.color.rgb = COLOR_PRIMARY
        r1v = p1.add_run(v1)
        r1v.font.size = Pt(9)

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(2)
        r2k = p2.add_run(k2 + " ")
        r2k.bold = True
        r2k.font.size = Pt(9)
        r2k.font.color.rgb = COLOR_PRIMARY
        r2v = p2.add_run(v2)
        r2v.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # 1. OBJETIVO
    # -------------------------------------------------------------------------
    add_h1("1. Objetivo del Proyecto")
    add_p(
        "El propósito de esta guía es documentar de manera práctica, reproducible y formal la arquitectura y pasos "
        "de implementación del sistema gastronómico Sazón Express. El objetivo fundamental no radica en la complejidad "
        "del negocio, sino en demostrar de manera contundente la externalización de configuraciones de tres microservicios "
        "REST independientes utilizando Spring Cloud Config Server conectado a un repositorio Git, permitiendo actualizar "
        "políticas operativas en caliente (hot-reloading) mediante Spring Boot Actuator y @RefreshScope sin tocar una sola "
        "línea de código Java ni requerir bases de datos."
    )

    # -------------------------------------------------------------------------
    # 2. HERRAMIENTAS NECESARIAS
    # -------------------------------------------------------------------------
    add_h1("2. Herramientas y Requisitos del Entorno")
    add_bullet("Java Development Kit (JDK 17 LTS o JDK 21): ", "Requerido para la compilación y ejecución de Spring Boot 4.0.9.")
    add_bullet("Apache Maven 3.9+ (o Maven Wrapper integrado): ", "Gestor de dependencias y constructor del reactor multi-módulo.")
    add_bullet("Git 2.x: ", "Sistema de control de versiones que almacena las propiedades externas en config-repo.")
    add_bullet("PowerShell 5.1+ / 7.x (Windows): ", "Entorno de automatización para los scripts de diagnóstico y demostración.")
    add_bullet("Cliente HTTP (Navegador, cURL, PowerShell Invoke-RestMethod o Postman): ", "Para la verificación de endpoints REST.")

    # -------------------------------------------------------------------------
    # 3. CREACIÓN DE LOS CUATRO PROYECTOS CON SPRING INITIALIZR
    # -------------------------------------------------------------------------
    add_h1("3. Creación de los Cuatro Proyectos con Spring Initializr")
    add_p(
        "Cada módulo fue generado a través del servicio oficial de Spring Initializr (start.spring.io) seleccionando "
        "como base: Proyecto Maven, Lenguaje Java, Versión de Java 17 y Spring Boot 4.0.9:"
    )

    t_mod = doc.add_table(rows=5, cols=4)
    t_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_mod.autofit = False

    mod_data = [
        ("Módulo", "Artifact ID", "Puerto", "Dependencias Seleccionadas"),
        ("Config Server", "config-server", "8888", "Config Server, Test"),
        ("Menú Service", "menu-service", "8081", "Web (WebMVC), Config Client, Actuator, Test"),
        ("Pedido Service", "pedido-service", "8082", "Web (WebMVC), Config Client, Actuator, Test"),
        ("Promoción Service", "promocion-service", "8083", "Web (WebMVC), Config Client, Actuator, Test")
    ]

    widths = [Inches(1.5), Inches(1.5), Inches(0.8), Inches(3.0)]
    for r_idx, row in enumerate(mod_data):
        for c_idx, text in enumerate(row):
            cell = t_mod.rows[r_idx].cells[c_idx]
            cell.width = widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if r_idx == 0:
                set_cell_background(cell, "1E3A8A")
                run = p.add_run(text)
                run.bold = True
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                set_cell_background(cell, "FFFFFF" if r_idx % 2 != 0 else "F8FAFC")
                run = p.add_run(text)
                run.font.size = Pt(8.5)
                run.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Insertar capturas reales de Initializr
    add_h2("Evidencias Reales de Generación en Spring Initializr:")
    
    img_cs = os.path.join(evidencias_dir, "creacion_proyecto_config_server.png")
    img_menu = os.path.join(evidencias_dir, "creacion_proyecto_menu_service.png")
    img_pedido = os.path.join(evidencias_dir, "creacion_proyecto_pedido_service.png")
    img_promo = os.path.join(evidencias_dir, "creacion_proyecto_promocion_service.png")

    if os.path.exists(img_cs) and os.path.exists(img_menu):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_cs, width=Inches(6.0))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_cap1.add_run("Figura 1: Configuración en Spring Initializr de config-server (Puerto 8888)")
        r_c1.font.italic = True
        r_c1.font.size = Pt(8.5)
        r_c1.font.color.rgb = COLOR_MUTED

    if os.path.exists(img_menu):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_menu, width=Inches(6.0))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_cap2.add_run("Figura 2: Configuración en Spring Initializr de menu-service (Web, Config Client, Actuator)")
        r_c2.font.italic = True
        r_c2.font.size = Pt(8.5)
        r_c2.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------------------
    # 4. DEPENDENCIAS MAVEN
    # -------------------------------------------------------------------------
    add_h1("4. Gestión de Dependencias y Compatibilidad Oficial (BOM)")
    add_p(
        "Para garantizar total estabilidad entre Spring Boot 4.0.9 y las librerías de Spring Cloud sin colisiones "
        "de dependencias transitivas, se adoptó el BOM oficial spring-cloud-dependencies:2025.1.4 en todos los pom.xml:"
    )

    bom_xml = """<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>2025.1.4</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>"""
    add_code_block(doc, bom_xml)

    # -------------------------------------------------------------------------
    # 5. ESTRUCTURA GENERAL DEL PROYECTO
    # -------------------------------------------------------------------------
    add_h1("5. Estructura General del Proyecto")
    add_p(
        "El proyecto se organiza bajo una arquitectura modular limpia con separación estricta de responsabilidades:"
    )

    tree_str = """sazon-express/
├── pom.xml                               # Reactor agregador Maven raíz
├── .gitignore                            # Exclusión de binarios (.class, target/)
├── .gitmodules                           # Definición de submódulo de configuración
├── config-server/                        # Servidor Central de Configuraciones (:8888)
├── menu-service/                         # Microservicio de Menú (:8081)
├── pedido-service/                       # Microservicio de Pedidos (:8082)
├── promocion-service/                    # Microservicio de Promociones (:8083)
├── config-repo/                          # Repositorio Git independiente (.git/)
│   ├── application.yml                   # Metadatos globales y Actuator
│   ├── menu-service.yml                  # Carta y plato destacado
│   ├── pedido-service.yml                # max-platos y tiempos
│   └── promocion-service.yml             # Descuentos comerciales
├── scripts/                              # Automatización PowerShell en Windows
│   ├── verificar-entorno.ps1             # Diagnóstico previo de JDK, Maven, Git, Puertos
│   ├── iniciar-config-server.ps1         # Inicio y sondeo de salud de Config Server
│   ├── iniciar-microservicios.ps1        # Despliegue de los 3 microservicios
│   ├── probar-endpoints.ps1              # Pruebas REST y guardado de respuestas JSON
│   ├── actualizar-configuraciones.ps1    # Demostración del ciclo completo de Refresh
│   └── detener-servicios.ps1             # Detención segura de procesos Java
└── docs/                                 # Entregables: Word (.docx), PDF, PPTX y evidencias"""
    add_code_block(doc, tree_str)

    # -------------------------------------------------------------------------
    # 6. CONFIGURACIÓN DEL CONFIG SERVER
    # -------------------------------------------------------------------------
    add_h1("6. Configuración de Spring Cloud Config Server")
    add_p(
        "En ConfigServerApplication.java se habilita el servidor con la anotación @EnableConfigServer:"
    )
    cs_java = """package com.sazonexpress.configserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}"""
    add_code_block(doc, cs_java)

    add_p(
        "En application.yaml se parametriza el backend Git para conectarse a GitHub con alternativa local transparente:"
    )
    cs_yaml = """server:
  port: 8888

spring:
  application:
    name: config-server
  cloud:
    config:
      server:
        git:
          # Repositorio remoto público oficial en GitHub:
          uri: ${CONFIG_REPO_URI:https://github.com/Jeanfranco06/sazon-express-config}
          default-label: main
          clone-on-start: true
          force-pull: true

management:
  endpoints:
    web:
      exposure:
        include: "health,info,env"
"""
    add_code_block(doc, cs_yaml)

    # -------------------------------------------------------------------------
    # 7. CREACIÓN DEL REPOSITORIO GIT DE CONFIGURACIONES
    # -------------------------------------------------------------------------
    add_h1("7. Creación del Repositorio Git (config-repo)")
    add_p(
        "El repositorio config-repo representa un repositorio Git auténtico e independiente con su propio directorio .git/ "
        "y rama main. Se conecta remotamente a GitHub en: https://github.com/Jeanfranco06/sazon-express-config:"
    )

    git_init_cmd = """# Inicialización local en config-repo
cd sazon-express/config-repo
git init
git config user.name "Jeanfranco06"
git config user.email "jeff_20_06@hotmail.com"
git add .
git commit -m "feat(config): configuracion inicial centralizada"
git branch -M main

# Publicación en GitHub público
gh repo create Jeanfranco06/sazon-express-config --public --source=. --remote=origin --push"""
    add_code_block(doc, git_init_cmd)

    # -------------------------------------------------------------------------
    # 8. CONFIGURACIÓN DE LOS TRES CLIENTES
    # -------------------------------------------------------------------------
    add_h1("8. Configuración de los Tres Clientes (Bootstrap)")
    add_p(
        "En Spring Boot 4.x, los microservicios clientes importan su configuración centralizada mediante la directiva "
        "spring.config.import y exponen los endpoints requeridos de Actuator:"
    )
    client_yaml = """spring:
  application:
    name: menu-service    # (o pedido-service, promocion-service)
  config:
    import: "optional:configserver:${CONFIG_SERVER_URL:http://localhost:8888}"

management:
  endpoints:
    web:
      exposure:
        include: "health,info,refresh"
  endpoint:
    health:
      show-details: always"""
    add_code_block(doc, client_yaml)

    # -------------------------------------------------------------------------
    # 9. PROGRAMACIÓN DE ENDPOINTS Y @REFRESHSCOPE
    # -------------------------------------------------------------------------
    add_h1("9. Programación de Endpoints y Anotación @RefreshScope")
    add_p(
        "Para que las clases Bean recarguen dinámicamente sus valores cuando se invoca POST /actuator/refresh, "
        "se anotan con @RefreshScope en conjunto con @ConfigurationProperties:"
    )
    menu_prop_java = """@Component
@RefreshScope
@ConfigurationProperties(prefix = "restaurante.menu")
public class MenuProperties {
    private String nombre = "Carta Sazón Express";
    private String platoDestacado = "Lomo saltado";
    private String mensaje = "Disfruta nuestros sabores";
    private boolean mostrarDisponibles = true;
    // Getters y Setters...
}"""
    add_code_block(doc, menu_prop_java)

    add_p("Endpoints desarrollados para cada microservicio:")
    add_bullet("Menu Service (:8081): ", "GET /api/menu, GET /api/menu/destacado, GET /api/menu/configuracion, POST /actuator/refresh.")
    add_bullet("Pedido Service (:8082): ", "GET /api/pedidos, POST /api/pedidos (valida max-platos), GET /api/pedidos/{id}, GET /api/pedidos/configuracion.")
    add_bullet("Promocion Service (:8083): ", "GET /api/promociones, GET /api/promociones/destacada, GET /api/promociones/calcular?precio=50 (con BigDecimal), GET /api/promociones/configuracion.")

    # -------------------------------------------------------------------------
    # 10. COMPILACIÓN Y EJECUCIÓN
    # -------------------------------------------------------------------------
    add_h1("10. Comandos de Compilación y Ejecución")
    add_h2("Opción A: Ejecución Automatizada con Scripts PowerShell (Recomendado)")
    cmd_auto = """cd D:\\Proyects\\microservicios\\sazon-express

# 1. Comprobar requisitos previos y puertos libres
.\\scripts\\verificar-entorno.ps1

# 2. Iniciar Config Server y esperar disponibilidad en :8888
.\\scripts\\iniciar-config-server.ps1

# 3. Iniciar los 3 microservicios en segundo plano (:8081, :8082, :8083)
.\\scripts\\iniciar-microservicios.ps1

# 4. Probar endpoints y guardar evidencias JSON
.\\scripts\\probar-endpoints.ps1

# 5. Ejecutar demostración en vivo de cambios en caliente
.\\scripts\\actualizar-configuraciones.ps1

# 6. Detener los servicios y liberar puertos al finalizar
.\\scripts\\detener-servicios.ps1"""
    add_code_block(doc, cmd_auto)

    add_h2("Opción B: Ejecución Manual con Maven / Java JAR")
    cmd_manual = """# Compilar todos los módulos desde la raíz:
mvn clean package -DskipTests

# Terminal 1: Iniciar Config Server (:8888)
java -Dspring.cloud.config.server.git.uri=https://github.com/Jeanfranco06/sazon-express-config.git -jar config-server\\target\\config-server-0.0.1-SNAPSHOT.jar

# Terminal 2: Iniciar Menu Service (:8081)
java -jar menu-service\\target\\menu-service-0.0.1-SNAPSHOT.jar

# Terminal 3: Iniciar Pedido Service (:8082)
java -jar pedido-service\\target\\pedido-service-0.0.1-SNAPSHOT.jar

# Terminal 4: Iniciar Promocion Service (:8083)
java -jar promocion-service\\target\\promocion-service-0.0.1-SNAPSHOT.jar"""
    add_code_block(doc, cmd_manual)

    # -------------------------------------------------------------------------
    # 11. PRUEBAS DE FUNCIONAMIENTO Y VERIFICACIÓN
    # -------------------------------------------------------------------------
    add_h1("11. Pruebas Automatizadas (23 Tests Aprobados)")
    add_p(
        "El proyecto cuenta con una cobertura integral de 23 pruebas con JUnit 5 y MockMvc que validan la resolución "
        "de configuración y las reglas de negocio:"
    )
    add_bullet("config-server (4 tests): ", "Inicio de contexto, acceso a JGit y PropertySources para cada microservicio.")
    add_bullet("menu-service (5 tests): ", "Catálogo de platos, plato destacado por defecto ('Lomo saltado') y recarga dinámica.")
    add_bullet("pedido-service (7 tests): ", "Pedido válido con 5 platos, rechazo con 6 platos, cambio dinámico a límite 2 y rechazo de 3 platos, y bloqueo cuando pedidosHabilitados=false.")
    add_bullet("promocion-service (7 tests): ", "Cálculo exacto de descuento del 15% (S/ 42.50), actualización dinámica al 20% (S/ 40.00), validación de precio negativo/cero (HTTP 400).")

    add_code_block(doc, "mvn -f sazon-express/pom.xml test\n# Resultado: Reactor Summary: 5/5 SUCCESS - 23 Tests Run, 0 Failures")

    # -------------------------------------------------------------------------
    # 12. DEMOSTRACIÓN DE MODIFICACIÓN CENTRALIZADA
    # -------------------------------------------------------------------------
    add_h1("12. Demostración en Vivo de Actualización en Caliente")
    add_p(
        "Durante la exposición, se realiza la demostración de los tres cambios en caliente sin reiniciar los microservicios:"
    )
    add_bullet("Demostración 1 (Menú): ", "GET /api/menu/destacado devuelve 'Lomo saltado'. Se modifica a 'Ceviche clásico' en Git, se hace commit, se ejecuta POST /actuator/refresh y el endpoint devuelve 'Ceviche clásico'.")
    add_bullet("Demostración 2 (Pedidos): ", "Regla inicial max-platos=5. Se envía pedido con 3 platos y es ACEPTADO (HTTP 201). Se cambia a max-platos=2 en Git, se hace commit y refresh. El mismo pedido de 3 platos es RECHAZADO (HTTP 400 Bad Request). Un pedido de 2 platos es ACEPTADO.")
    add_bullet("Demostración 3 (Promociones): ", "Cálculo para precio S/ 50 al 15% devuelve S/ 42.50. Se cambia descuento-porcentaje=20 en Git, commit y refresh. La consulta para S/ 50 devuelve inmediatamente S/ 40.00.")

    # -------------------------------------------------------------------------
    # 13. PROBLEMAS FRECUENTES Y SOLUCIONES
    # -------------------------------------------------------------------------
    add_h1("13. Problemas Frecuentes y Soluciones")
    add_bullet("Error HTTP 415 en /actuator/refresh: ", "Ocurre si no se envía cabecera Content-Type. Solución: usar -ContentType 'application/json' -Body '{}' en PowerShell o -H 'Content-Type: application/json' en cURL.")
    add_bullet("Connection Refused en :8888 al iniciar clientes: ", "Ocurre si los clientes inician antes que el Config Server. Solución: usar iniciar-config-server.ps1 que espera la disponibilidad del puerto.")
    add_bullet("Puertos ocupados (Address already in use): ", "Ocurre si quedaron procesos Java activos. Solución: ejecutar detener-servicios.ps1 para liberar los puertos 8888, 8081, 8082 y 8083.")

    # -------------------------------------------------------------------------
    # 14. CONCLUSIONES
    # -------------------------------------------------------------------------
    add_h1("14. Conclusiones")
    add_bullet("Centralización y Gobernanza: ", "Spring Cloud Config Server resuelve definitivamente la dispersión de configuraciones, desacoplando los parámetros de negocio del ciclo de vida del código.")
    add_bullet("Trazabilidad con GitOps: ", "El versionamiento de archivos YAML en Git proporciona auditoría de auditoría, control de versiones e inmutabilidad en las políticas operativas del restaurante.")
    add_bullet("Alta Disponibilidad: ", "La recarga en caliente con @RefreshScope y Actuator permite adaptar promociones y límites de pedidos en tiempo real con cero tiempo de inactividad (Zero Downtime).")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Guía Word generada exitosamente en: {output_path}")

if __name__ == "__main__":
    out_docx = r"D:\Proyects\microservicios\sazon-express\docs\Guia_Implementacion_Sazon_Express.docx"
    evid_dir = r"D:\Proyects\microservicios\sazon-express\docs\evidencias"
    generate_word_guide(out_docx, evid_dir)
