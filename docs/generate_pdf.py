import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Omitir header y footer en la portada
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header superior
        self.drawString(54, letter[1] - 36, "Sazón Express — Guía de Implementación Spring Cloud Config Server")
        self.drawRightString(letter[0] - 54, letter[1] - 36, "Caso Práctico Universitario")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer inferior
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.drawString(54, 36, "Arquitectura de Software | 3 Microservicios + Git + Actuator")
        self.line(54, 48, letter[0] - 54, 48)

        self.restoreState()


def build_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    c_primary = colors.HexColor("#1E3A8A")   # Azul marino formal
    c_accent = colors.HexColor("#0D9488")    # Verde azulado moderno
    c_text = colors.HexColor("#0F172A")      # Gris casi negro
    c_muted = colors.HexColor("#475569")     # Gris secundario
    c_code_bg = colors.HexColor("#F8FAFC")   # Fondo código
    c_callout_bg = colors.HexColor("#EFF6FF")# Fondo notas

    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=0,
        spaceAfter=8
    )

    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=15
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_text,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text,
        leftIndent=14,
        spaceAfter=3
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=0
    )

    style_table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_text
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []

    # -------------------------------------------------------------------------
    # PORTADA / ENCABEZADO
    # -------------------------------------------------------------------------
    story.append(Paragraph("GUÍA DE IMPLEMENTACIÓN PRÁCTICA", style_subtitle))
    story.append(Paragraph("Spring Cloud Config Server con Tres Microservicios", style_title))
    story.append(Paragraph("<b>Caso Práctico: Sazón Express — Centralización de Configuraciones y Actualización en Caliente</b>", ParagraphStyle(
        'SubSub', fontName='Helvetica', fontSize=11, leading=14, textColor=c_muted, spaceAfter=15
    )))

    # Metadatos del Trabajo
    meta_data = [
        [Paragraph("<b>Curso:</b> Arquitectura de Software / Microservicios", style_table_text), Paragraph("<b>Tecnologías:</b> Java 17, Spring Boot 4.0.9, Spring Cloud 2025.1.4", style_table_text)],
        [Paragraph("<b>Entorno:</b> Windows / Maven 3.9 / Git", style_table_text), Paragraph("<b>Ecosistema:</b> 4 Módulos + Git config-repo + Actuator", style_table_text)],
        [Paragraph("<b>Integrantes:</b> Equipo de Proyecto Sazón Express", style_table_text), Paragraph("<b>Modalidad:</b> Exposición Académica Universitaria", style_table_text)]
    ]
    t_meta = Table(meta_data, colWidths=[240, 260])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # 1. OBJETIVO
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Objetivo de la Guía", style_h1))
    story.append(Paragraph(
        "El propósito de esta guía es documentar de manera directa, reproducible y paso a paso la "
        "implementación de una arquitectura de microservicios basada en <b>Spring Cloud Config Server</b> "
        "para el sistema gastronómico <b>Sazón Express</b>. El docente y los estudiantes podrán levantar el "
        "sistema desde cero en cualquier computadora, demostrando cómo tres microservicios independientes "
        "(<code>menu-service</code>, <code>pedido-service</code> y <code>promocion-service</code>) obtienen "
        "sus políticas de negocio desde un repositorio <b>Git</b> y aplican actualizaciones dinámicas en "
        "tiempo de ejecución mediante <code>@RefreshScope</code> sin requerir bases de datos ni redespliegues.",
        style_body
    ))

    # -------------------------------------------------------------------------
    # 2. HERRAMIENTAS NECESARIAS
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Herramientas y Requisitos del Entorno", style_h1))
    herramientas = [
        ("Java Development Kit (JDK 17 LTS o 21 LTS)", "Plataforma base para compilación y ejecución de Spring Boot 4.x."),
        ("Apache Maven 3.9+ (o Maven Wrapper mvnw)", "Gestión de dependencias y empaquetado JAR ejecutable."),
        ("Git 2.x", "Sistema de control de versiones que almacena las propiedades externas en config-repo."),
        ("PowerShell 5.1+ / 7.x (Windows)", "Ejecución de los scripts automatizados de diagnóstico y pruebas."),
        ("Navegador web o cURL / Postman / Invoke-RestMethod", "Para consumir los endpoints REST y Actuator.")
    ]
    for h, desc in herramientas:
        story.append(Paragraph(f"• <b>{h}:</b> {desc}", style_bullet))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 3. CREACIÓN DE LOS CUATRO PROYECTOS CON SPRING INITIALIZR
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Creación de Proyectos con Spring Initializr", style_h1))
    story.append(Paragraph(
        "Cada uno de los cuatro módulos fue generado utilizando el servicio oficial <b>start.spring.io</b> "
        "con los siguientes parámetros base: Maven Project, Java 17, Spring Boot 4.0.9 y empaquetado Jar.",
        style_body
    ))

    initializr_data = [
        [Paragraph("<b>Módulo</b>", style_table_header), Paragraph("<b>Artifact ID</b>", style_table_header), Paragraph("<b>Puerto</b>", style_table_header), Paragraph("<b>Dependencias Initializr</b>", style_table_header)],
        [Paragraph("<b>Config Server</b>", style_table_text), Paragraph("config-server", style_table_text), Paragraph("8888", style_table_text), Paragraph("Config Server, Test", style_table_text)],
        [Paragraph("<b>Menú Service</b>", style_table_text), Paragraph("menu-service", style_table_text), Paragraph("8081", style_table_text), Paragraph("Web (WebMVC), Config Client, Actuator", style_table_text)],
        [Paragraph("<b>Pedido Service</b>", style_table_text), Paragraph("pedido-service", style_table_text), Paragraph("8082", style_table_text), Paragraph("Web (WebMVC), Config Client, Actuator", style_table_text)],
        [Paragraph("<b>Promoción Service</b>", style_table_text), Paragraph("promocion-service", style_table_text), Paragraph("8083", style_table_text), Paragraph("Web (WebMVC), Config Client, Actuator", style_table_text)]
    ]
    t_init = Table(initializr_data, colWidths=[110, 110, 50, 230])
    t_init.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_init)
    story.append(Spacer(1, 10))

    # Incluir imágenes reales de evidencia de Initializr
    evidencias_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidencias")
    img_cs = os.path.join(evidencias_dir, "creacion_proyecto_config_server.png")
    img_menu = os.path.join(evidencias_dir, "creacion_proyecto_menu_service.png")

    if os.path.exists(img_cs) and os.path.exists(img_menu):
        story.append(Paragraph("<b>Capturas Reales de Configuración en Spring Initializr:</b>", style_h2))
        img_table_data = [
            [
                Image(img_cs, width=3.3*inch, height=1.7*inch),
                Image(img_menu, width=3.3*inch, height=1.7*inch)
            ],
            [
                Paragraph("<i>Figura 1: Creación de config-server (Config Server)</i>", style_table_text),
                Paragraph("<i>Figura 2: Creación de menu-service (Web, Client, Actuator)</i>", style_table_text)
            ]
        ]
        t_imgs = Table(img_table_data, colWidths=[250, 250])
        t_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_imgs)

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 4. DEPENDENCIAS MAVEN
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Gestión de Dependencias (BOM Spring Cloud)", style_h1))
    story.append(Paragraph(
        "Para garantizar la compatibilidad entre Spring Boot 4.0.9 y Spring Cloud, se utiliza el BOM "
        "(<i>Bill of Materials</i>) oficial <b>spring-cloud-dependencies:2025.1.4</b> en todos los <code>pom.xml</code>:",
        style_body
    ))

    code_bom = (
        "&lt;dependencyManagement&gt;<br/>"
        "  &lt;dependencies&gt;<br/>"
        "    &lt;dependency&gt;<br/>"
        "      &lt;groupId&gt;org.springframework.cloud&lt;/groupId&gt;<br/>"
        "      &lt;artifactId&gt;spring-cloud-dependencies&lt;/artifactId&gt;<br/>"
        "      &lt;version&gt;2025.1.4&lt;/version&gt;<br/>"
        "      &lt;type&gt;pom&lt;/type&gt;<br/>"
        "      &lt;scope&gt;import&lt;/scope&gt;<br/>"
        "    &lt;/dependency&gt;<br/>"
        "  &lt;/dependencies&gt;<br/>"
        "&lt;/dependencyManagement&gt;"
    )
    t_code_bom = Table([[Paragraph(code_bom, style_code)]], colWidths=[500])
    t_code_bom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code_bom)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # 5. ESTRUCTURA GENERAL DEL PROYECTO
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Estructura General del Proyecto", style_h1))
    story.append(Paragraph(
        "El proyecto organiza las responsabilidades en 4 módulos independientes, 1 repositorio Git exclusivo "
        "de configuración y un conjunto de scripts PowerShell de automatización:",
        style_body
    ))

    tree_text = (
        "sazon-express/<br/>"
        "├── pom.xml                               # Reactor agregador Maven raíz<br/>"
        "├── config-server/                        # Servidor Central (:8888)<br/>"
        "├── menu-service/                         # Microservicio de Menú (:8081)<br/>"
        "├── pedido-service/                       # Microservicio de Pedidos (:8082)<br/>"
        "├── promocion-service/                    # Microservicio de Promociones (:8083)<br/>"
        "├── config-repo/                          # Repositorio Git independiente (.git/)<br/>"
        "│   ├── application.yml                   # Metadatos y Actuator común<br/>"
        "│   ├── menu-service.yml                  # Carta y plato destacado<br/>"
        "│   ├── pedido-service.yml                # Límite max-platos y tiempos<br/>"
        "│   └── promocion-service.yml             # Descuentos porcentuales<br/>"
        "├── scripts/                              # Scripts PowerShell (.ps1) de automatización<br/>"
        "└── docs/                                 # PDF, PPTX y evidencias de ejecución"
    )
    t_tree = Table([[Paragraph(tree_text, style_code)]], colWidths=[500])
    t_tree.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tree)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 6. CONFIGURACIÓN DEL CONFIG SERVER
    # -------------------------------------------------------------------------
    story.append(Paragraph("6. Configuración de Spring Cloud Config Server", style_h1))
    story.append(Paragraph(
        "<b>Clase Principal:</b> En <code>ConfigServerApplication.java</code> se incluye la anotación <code>@EnableConfigServer</code>.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Archivo application.yaml:</b> Se enlaza el repositorio Git mediante protocolo <code>file:///</code> o variable de entorno:",
        style_body
    ))

    code_cs_yml = (
        "server:<br/>"
        "  port: 8888<br/>"
        "spring:<br/>"
        "  application:<br/>"
        "    name: config-server<br/>"
        "  cloud:<br/>"
        "    config:<br/>"
        "      server:<br/>"
        "        git:<br/>"
        "          uri: ${CONFIG_REPO_URI:file:///${user.dir}/../config-repo}<br/>"
        "          default-label: main<br/>"
        "          clone-on-start: true"
    )
    t_cs = Table([[Paragraph(code_cs_yml, style_code)]], colWidths=[500])
    t_cs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cs)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 7. CREACIÓN DEL REPOSITORIO GIT DE CONFIGURACIONES
    # -------------------------------------------------------------------------
    story.append(Paragraph("7. Creación del Repositorio Git (config-repo)", style_h1))
    story.append(Paragraph(
        "El repositorio <code>config-repo</code> es un repositorio Git auténtico e independiente. Para inicializarlo:",
        style_body
    ))

    code_git_init = (
        "cd sazon-express/config-repo<br/>"
        "git init<br/>"
        "git config user.name \"Sazon Express Team\"<br/>"
        "git config user.email \"arquitectura@sazonexpress.com\"<br/>"
        "git add .<br/>"
        "git commit -m \"feat(config): configuracion inicial centralizada\"<br/>"
        "git branch -M main"
    )
    t_git = Table([[Paragraph(code_git_init, style_code)]], colWidths=[500])
    t_git.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_git)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 8. CONFIGURACIÓN DE LOS TRES CLIENTES
    # -------------------------------------------------------------------------
    story.append(Paragraph("8. Configuración de los Tres Clientes (Bootstrap)", style_h1))
    story.append(Paragraph(
        "En Spring Boot 4.x, los clientes conectan al Config Server mediante la propiedad <code>spring.config.import</code> "
        "en sus respectivos <code>application.yaml</code> locales:",
        style_body
    ))

    code_client_yml = (
        "spring:<br/>"
        "  application:<br/>"
        "    name: menu-service   # (o pedido-service, promocion-service)<br/>"
        "  config:<br/>"
        "    import: \"optional:configserver:${CONFIG_SERVER_URL:http://localhost:8888}\"<br/>"
        "management:<br/>"
        "  endpoints:<br/>"
        "    web:<br/>"
        "      exposure:<br/>"
        "        include: \"health,info,refresh\""
    )
    t_cl = Table([[Paragraph(code_client_yml, style_code)]], colWidths=[500])
    t_cl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cl)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # 9. PROGRAMACIÓN DE ENDPOINTS Y @REFRESHSCOPE
    # -------------------------------------------------------------------------
    story.append(Paragraph("9. Programación de Endpoints y Uso de @RefreshScope", style_h1))
    story.append(Paragraph(
        "Para que los componentes recarguen sus valores en caliente cuando cambia el YAML en Git, se anotan con "
        "<code>@RefreshScope</code> junto con <code>@ConfigurationProperties</code> o <code>@Service</code>:",
        style_body
    ))

    code_refresh_java = (
        "// MenuProperties.java<br/>"
        "@Component<br/>"
        "@RefreshScope<br/>"
        "@ConfigurationProperties(prefix = \"restaurante.menu\")<br/>"
        "public class MenuProperties {<br/>"
        "    private String nombre = \"Carta Sazón Express\";<br/>"
        "    private String platoDestacado = \"Lomo saltado\";<br/>"
        "    private String mensaje = \"Disfruta nuestros sabores\";<br/>"
        "    private boolean mostrarDisponibles = true;<br/>"
        "    // Getters y Setters...<br/>"
        "}"
    )
    t_rf = Table([[Paragraph(code_refresh_java, style_code)]], colWidths=[500])
    t_rf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_rf)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 10. COMPILACIÓN Y EJECUCIÓN
    # -------------------------------------------------------------------------
    story.append(Paragraph("10. Comandos de Compilación y Ejecución", style_h1))
    story.append(Paragraph(
        "El proyecto puede compilarse integralmente mediante el POM agregador raíz y ejecutarse de dos formas:",
        style_body
    ))
    story.append(Paragraph("<b>Opción A — Mediante Scripts Automatizados PowerShell (Recomendado):</b>", style_h2))
    cmd_ps1 = (
        "cd sazon-express<br/>"
        ".\\scripts\\verificar-entorno.ps1<br/>"
        ".\\scripts\\iniciar-config-server.ps1<br/>"
        ".\\scripts\\iniciar-microservicios.ps1<br/>"
        ".\\scripts\\probar-endpoints.ps1"
    )
    story.append(Table([[Paragraph(cmd_ps1, style_code)]], colWidths=[500], style=[
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Opción B — Manualmente con Maven o Java JAR:</b>", style_h2))
    cmd_man = (
        "# 1. Compilar todo el sistema<br/>"
        "mvn clean package -DskipTests<br/><br/>"
        "# 2. Iniciar Config Server (:8888)<br/>"
        'java "-Dspring.cloud.config.server.git.uri=https://github.com/Jeanfranco06/sazon-express-config.git" -jar config-server\\target\\config-server-0.0.1-SNAPSHOT.jar<br/><br/>'
        "# 3. Iniciar clientes en consolas separadas (:8081, :8082, :8083)<br/>"
        "java -jar menu-service/target/menu-service-0.0.1-SNAPSHOT.jar<br/>"
        "java -jar pedido-service/target/pedido-service-0.0.1-SNAPSHOT.jar<br/>"
        "java -jar promocion-service/target/promocion-service-0.0.1-SNAPSHOT.jar"
    )
    story.append(Table([[Paragraph(cmd_man, style_code)]], colWidths=[500], style=[
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 11. PRUEBAS DE FUNCIONAMIENTO
    # -------------------------------------------------------------------------
    story.append(Paragraph("11. Pruebas de Funcionamiento y Verificación", style_h1))
    story.append(Paragraph(
        "El proyecto incluye <b>23 pruebas automatizadas</b> ejecutadas con éxito con JUnit 5 y MockMvc. "
        "Para ejecutarlas todas:",
        style_body
    ))
    story.append(Table([[Paragraph("mvn clean test", style_code)]], colWidths=[500], style=[
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # 12. EJEMPLO DE MODIFICACIÓN CENTRALIZADA (DEMOSTRACIÓN)
    # -------------------------------------------------------------------------
    story.append(Paragraph("12. Demostración de Modificación Centralizada Dinámica", style_h1))
    story.append(Paragraph(
        "A continuación se presenta el flujo exacto ejecutado en la demostración universitaria:",
        style_body
    ))

    demo_steps = [
        ("Paso 1: Consultar estado actual", "GET http://localhost:8081/api/menu/destacado -> Retorna: 'Lomo saltado'."),
        ("Paso 2: Modificar propiedad en Git", "Editar config-repo/menu-service.yml: restaurante.menu.plato-destacado: 'Ceviche clásico'."),
        ("Paso 3: Confirmar commit en Git", "git add . && git commit -m 'feat: cambiar plato destacado a Ceviche clasico'."),
        ("Paso 4: Verificar en Config Server", "GET http://localhost:8888/menu-service/default -> Muestra el nuevo commit hash."),
        ("Paso 5: Invocar Refresh en Cliente", "POST http://localhost:8081/actuator/refresh con cabecera Content-Type: application/json."),
        ("Paso 6: Validar nuevo comportamiento", "GET http://localhost:8081/api/menu/destacado -> Retorna: 'Ceviche clásico' sin reiniciar Java!")
    ]
    for p, d in demo_steps:
        story.append(Paragraph(f"• <b>{p}:</b> {d}", style_bullet))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 13. PROBLEMAS FRECUENTES Y SOLUCIONES
    # -------------------------------------------------------------------------
    story.append(Paragraph("13. Problemas Frecuentes y Soluciones", style_h1))
    problemas = [
        ("Error 415 al llamar /actuator/refresh", "Al enviar la petición POST, se debe especificar la cabecera -ContentType 'application/json' y el cuerpo -Body '{}'."),
        ("Connection refused en :8888 al arrancar clientes", "Config Server debe haber iniciado completamente antes de que los clientes intenten inicializarse. Utilice el script iniciar-config-server.ps1 que espera la disponibilidad del puerto."),
        ("Address already in use (Puertos 8081-8083 u 8888 ocupados)", "Ejecute el script .\\scripts\\detener-servicios.ps1 para liberar los procesos Java en escucha automáticamente."),
        ("JGit remote null warning en logs", "Es una advertencia normal cuando el repositorio Git es estrictamente local y no cuenta con un remote 'origin' configurado. No afecta el funcionamiento.")
    ]
    for prob, sol in problemas:
        story.append(Paragraph(f"• <b>{prob}:</b><br/>&nbsp;&nbsp;<i>Solución:</i> {sol}", style_bullet))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 14. CONCLUSIONES BREVES
    # -------------------------------------------------------------------------
    story.append(Paragraph("14. Conclusiones", style_h1))
    conclusiones = [
        "Spring Cloud Config Server centraliza eficientemente la gestión de microservicios, eliminando archivos dispersos y desalineaciones entre entornos.",
        "El uso de Git como backend garantiza trazabilidad, inmutabilidad de versiones y alineación con las mejores prácticas de la industria (GitOps / Configuration-as-Code).",
        "La integración con Spring Boot Actuator y @RefreshScope permite actualizar políticas operativas y comerciales en caliente con cero tiempo de inactividad (Zero Downtime).",
        "El diseño en memoria implementado en Sazón Express permite una demostración limpia, pedagógica y 100% reproducible en cualquier máquina académica sin fricción de bases de datos."
    ]
    for c in conclusiones:
        story.append(Paragraph(f"• {c}", style_bullet))

    # Construir documento con NumberedCanvas
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Guía PDF generada exitosamente en: {output_pdf_path}")

if __name__ == "__main__":
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_out = os.path.join(docs_dir, "Guia_Implementacion_Sazon_Express.pdf")
    build_pdf(pdf_out)
