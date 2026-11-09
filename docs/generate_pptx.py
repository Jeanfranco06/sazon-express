import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Paleta de colores formal y moderna (Fondo claro / Minimalista universitario)
    COLOR_BG = RGBColor(248, 250, 252)        # Slate 50
    COLOR_PRIMARY = RGBColor(30, 58, 138)      # Deep Blue 900
    COLOR_ACCENT = RGBColor(13, 148, 136)      # Teal 600
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)     # Slate 900
    COLOR_TEXT_MUTED = RGBColor(71, 85, 105)   # Slate 600
    COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
    COLOR_CARD_BORDER = RGBColor(226, 232, 240) # Slate 200
    COLOR_HIGHLIGHT = RGBColor(239, 246, 255)  # Blue 50

    def add_header(slide, title_text, category_text="ARQUITECTURA DE SOFTWARE"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY
        p_title.space_before = Pt(4)

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # =========================================================================
    # SLIDE 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = add_card(s1, Inches(0), Inches(0), Inches(13.333), Inches(7.5), COLOR_BG, COLOR_BG)

    # Card principal de portada
    card_portada = add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), COLOR_CARD_BG, COLOR_CARD_BORDER)
    
    tb1 = s1.shapes.add_textbox(Inches(1.8), Inches(1.4), Inches(9.7), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "ARQUITECTURA DE MICROSERVICIOS Y GESTIÓN EXTERNALIZADA"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    p = tf1.add_paragraph()
    p.text = "Spring Cloud Config Server"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Caso Práctico: Sazón Express — Centralización y Actualización Dinámica"
    p.font.size = Pt(18)
    p.font.bold = False
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "\n" + "—"*48
    p.font.color.rgb = COLOR_CARD_BORDER
    p.space_before = Pt(10)

    # Campos editables requeridos
    p = tf1.add_paragraph()
    p.text = "• Curso: Arquitectura de Microservicios y Sistemas Distribuidos\n" \
             "• Integrantes: [Nombre de los Integrantes del Grupo]\n" \
             "• Docente: [Nombre del Docente del Curso]\n" \
             "• Fecha: Noviembre 2026 | Universidad"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 2: PROBLEMA Y SOLUCIÓN
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_header(s2, "Problema y Solución: La Dispersión de Configuraciones")

    # Card Izquierda: Problema
    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0))
    tb2_left = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.5))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "⚠️ El Problema: Configuraciones Dispersas"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(220, 38, 38) # Red 600

    items_prob = [
        ("Acoplamiento estático:", "Cada microservicio empaqueta sus propios archivos de propiedades (.properties o .yml) dentro del binario JAR."),
        ("Dificultad de escalamiento:", "Cambiar una regla comercial en N microservicios exige N modificaciones, N compilaciones y N redespliegues."),
        ("Riesgo de inconsistencia:", "Discrepancias entre entornos (desarrollo, pruebas, producción) debido a parámetros locales desincronizados."),
        ("Falta de auditoría:", "Imposibilidad de auditar quién modificó qué parámetro, cuándo y con qué justificación técnica.")
    ]
    for tit, desc in items_prob:
        p = tf2_l.add_paragraph()
        p.text = f"• {tit} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    # Card Derecha: Solución
    add_card(s2, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0), COLOR_HIGHLIGHT, COLOR_ACCENT)
    tb2_right = s2.shapes.add_textbox(Inches(7.2), Inches(1.9), Inches(5.0), Inches(4.5))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "✅ La Solución: Spring Cloud Config"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    items_sol = [
        ("Servidor Centralizado:", "Un único punto de acceso autorizado que provee configuración externa vía HTTP a todos los clientes."),
        ("Repositorio Git:", "Versionamiento estricto, ramas, pull requests, historial de commits y trazabilidad total de cambios."),
        ("Recarga en Caliente (@RefreshScope):", "Modificación de parámetros sin reiniciar servidores ni detener la atención al cliente."),
        ("Independencia del código:", "La lógica de negocio Java permanece inalterada; las políticas operativas residen en YAML.")
    ]
    for tit, desc in items_sol:
        p = tf2_r.add_paragraph()
        p.text = f"• {tit} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: ¿QUÉ ES SPRING CLOUD CONFIG SERVER?
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_header(s3, "¿Qué es Spring Cloud Config Server?")

    # 3 Cards horizontales
    cards_s3 = [
        ("Definición y Rol", "Componente central del ecosistema Spring Cloud diseñado para gestionar las configuraciones de aplicaciones distribuidas de manera horizontal y agnóstica a la infraestructura."),
        ("Integración Nativa con Git", "Utiliza Git como almacenamiento primario (backend JGit). Cada commit representa una nueva versión inmutable de configuración con historial completo."),
        ("Beneficios Operativos", "• Centralización de políticas\n• Auditoría y control de versiones\n• Soporte de perfiles (dev, prod)\n• Cero tiempo de inactividad con Actuator")
    ]
    for i, (tit, desc) in enumerate(cards_s3):
        left_pos = Inches(0.8 + i * 4.0)
        add_card(s3, left_pos, Inches(1.8), Inches(3.7), Inches(4.8))
        tb = s3.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 4: ARQUITECTURA DEL PROYECTO
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_header(s4, "Arquitectura de Sazón Express: Flujo de Configuración")

    # Diagrama de Bloques
    # Bloque 1: Git
    add_card(s4, Inches(4.5), Inches(1.6), Inches(4.3), Inches(1.1), COLOR_HIGHLIGHT, COLOR_PRIMARY)
    tb_git = s4.shapes.add_textbox(Inches(4.6), Inches(1.7), Inches(4.1), Inches(0.9))
    tf_g = tb_git.text_frame
    tf_g.word_wrap = True
    p = tf_g.paragraphs[0]
    p.text = "📂 Repositorio Git Independiente (config-repo)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_PRIMARY
    p = tf_g.add_paragraph()
    p.text = "application.yml | menu-service.yml | pedido-service.yml | promocion-service.yml"
    p.font.size = Pt(10)
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Flecha hacia Config Server
    arrow_box = s4.shapes.add_textbox(Inches(6.3), Inches(2.7), Inches(1.0), Inches(0.4))
    p = arrow_box.text_frame.paragraphs[0]
    p.text = "▼  (JGit Fetch)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    # Bloque 2: Config Server
    add_card(s4, Inches(3.8), Inches(3.2), Inches(5.7), Inches(1.1), COLOR_CARD_BG, COLOR_PRIMARY)
    tb_cs = s4.shapes.add_textbox(Inches(3.9), Inches(3.3), Inches(5.5), Inches(0.9))
    tf_cs = tb_cs.text_frame
    tf_cs.word_wrap = True
    p = tf_cs.paragraphs[0]
    p.text = "⚙️ Spring Cloud Config Server (:8888)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_PRIMARY
    p = tf_cs.add_paragraph()
    p.text = "@EnableConfigServer | Expone HTTP REST con PropertySources extraídos de Git"
    p.font.size = Pt(11)
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Bloques Clientes (3 columnas abajo)
    servicios_s4 = [
        ("🍽️ Menu Service (:8081)", "Carta y platos disponibles\nPlato destacado: 'Lomo saltado'\n@RefreshScope en catálogo"),
        ("📋 Pedido Service (:8082)", "Registro y reglas de pedidos\nLímite: max-platos = 5\nValidación en memoria"),
        ("🏷️ Promocion Service (:8083)", "Cálculo de precios y combos\nDescuento: 15% (BigDecimal)\nPromoción destacada")
    ]
    for i, (tit, desc) in enumerate(servicios_s4):
        left_pos = Inches(0.8 + i * 4.0)
        add_card(s4, left_pos, Inches(4.7), Inches(3.7), Inches(2.1))
        tb = s4.shapes.add_textbox(left_pos + Inches(0.15), Inches(4.8), Inches(3.4), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        p = tf.add_paragraph()
        p.text = "▲ spring.config.import (:8888)"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: IMPLEMENTACIÓN TÉCNICA
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_header(s5, "Implementación Técnica y Compatibilidad")

    # 4 Cards Técnicas
    tech_cards = [
        ("Tecnologías y Versiones", [
            ("Java", "Java 17 LTS / 21 LTS"),
            ("Spring Boot", "4.0.9 (Jakarta EE)"),
            ("Spring Cloud", "2025.1.4 Oficial"),
            ("Maven", "Reactor multi-módulo raíz")
        ]),
        ("Config Server (:8888)", [
            ("@EnableConfigServer", "Activa el servidor"),
            ("Git Backend", "JGit conectado a config-repo"),
            ("Rama", "main como etiqueta por defecto"),
            ("Endpoints", "/{app}/default")
        ]),
        ("Configuración Clientes", [
            ("Importación", "spring.config.import"),
            ("Precedencia", "Git > local application.yaml"),
            ("Actuator", "health, info, refresh expuestos"),
            ("Zero Database", "Totalmente en memoria")
        ]),
        ("Archivos YAML en Git", [
            ("application.yml", "Actuator y metadata común"),
            ("menu-service.yml", "Carta y plato destacado"),
            ("pedido-service.yml", "max-platos y habilitación"),
            ("promocion-service.yml", "descuento-porcentaje")
        ])
    ]
    for i, (tit, rows) in enumerate(tech_cards):
        left_pos = Inches(0.8 + i * 3.0)
        add_card(s5, left_pos, Inches(1.8), Inches(2.8), Inches(4.8))
        tb = s5.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.0), Inches(2.5), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        for k, v in rows:
            p = tf.add_paragraph()
            p.text = f"• {k}:\n  {v}"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: FUNCIONAMIENTO DE LOS MICROSERVICIOS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_header(s6, "Funcionamiento de los Tres Microservicios REST")

    micro_cards = [
        ("🍽️ Menu Service (:8081)", [
            ("Objetivo:", "Consulta de catálogo y recomendaciones"),
            ("Colección:", "List<Plato> en memoria (Lomo saltado, Ají de gallina, Ceviche)"),
            ("Propiedad Clave:", "restaurante.menu.plato-destacado"),
            ("Endpoints:", "GET /api/menu\nGET /api/menu/destacado\nGET /api/menu/configuracion")
        ]),
        ("📋 Pedido Service (:8082)", [
            ("Objetivo:", "Registro y validación de comandas"),
            ("Regla Negocio:", "Rechaza pedidos si totalPlatos > max-platos o si pedidos deshabilitados"),
            ("Propiedad Clave:", "restaurante.pedidos.max-platos: 5"),
            ("Endpoints:", "GET /api/pedidos\nPOST /api/pedidos\nGET /api/pedidos/{id}")
        ]),
        ("🏷️ Promocion Service (:8083)", [
            ("Objetivo:", "Cálculo financiero de ofertas comerciales"),
            ("Regla Negocio:", "Cálculo con BigDecimal y RoundingMode.HALF_UP (S/ 50 al 15% = S/ 42.50)"),
            ("Propiedad Clave:", "restaurante.promociones.descuento-porcentaje: 15"),
            ("Endpoints:", "GET /api/promociones\nGET /api/promociones/calcular?precio=X")
        ])
    ]
    for i, (tit, details) in enumerate(micro_cards):
        left_pos = Inches(0.8 + i * 4.0)
        add_card(s6, left_pos, Inches(1.8), Inches(3.7), Inches(4.8))
        tb = s6.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        for k, v in details:
            p = tf.add_paragraph()
            p.text = f"{k} {v}"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: DEMOSTRACIÓN DE CONFIGURACIÓN CENTRALIZADA
    # =========================================================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_header(s7, "Demostración de Actualización en Caliente (@RefreshScope)")

    # Banner del Flujo
    add_card(s7, Inches(0.8), Inches(1.6), Inches(11.7), Inches(0.8), COLOR_HIGHLIGHT, COLOR_ACCENT)
    tb_flow = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(0.6))
    p = tb_flow.text_frame.paragraphs[0]
    p.text = "Flujo Real: 1. Modificar YAML en Git ➔ 2. git commit ➔ 3. POST /actuator/refresh ➔ 4. Cambio Inmediato en API"
    p.font.size = Pt(13)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = COLOR_PRIMARY

    # 3 Casos Demostrados
    casos = [
        ("Demo 1: Menú", "Plato Destacado", "Lomo saltado", "Ceviche clásico", 
         "El endpoint /api/menu/destacado actualiza el plato recomendado y el mensaje promocional sin reiniciar Tomcat."),
        ("Demo 2: Pedidos", "Límite max-platos", "5 platos máx.", "2 platos máx.", 
         "Un pedido de 3 platos era aceptado (HTTP 201). Tras el refresh, es rechazado (HTTP 400 Bad Request) por superar la nueva regla."),
        ("Demo 3: Promociones", "Descuento en S/ 50", "15% -> S/ 42.50", "20% -> S/ 40.00", 
         "El endpoint /api/promociones/calcular?precio=50 recalcula dinámicamente con BigDecimal a S/ 40.00.")
    ]
    for i, (tit, param, antes, despues, impacto) in enumerate(casos):
        left_pos = Inches(0.8 + i * 4.0)
        add_card(s7, left_pos, Inches(2.7), Inches(3.7), Inches(4.0))
        tb = s7.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.9), Inches(3.3), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        p = tf.add_paragraph()
        p.text = f"Parámetro: {param}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = f"• Antes (Git Inicial):\n   {antes}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = f"• Después (Commit + Refresh):\n   {despues}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = f"Impacto: {impacto}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 8: RESULTADOS Y CONCLUSIONES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_header(s8, "Resultados, Lecciones y Conclusiones")

    add_card(s8, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0))
    tb8_l = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.5))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "🎯 Logros y Resultados Clave"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    resultados = [
        ("Centralización Exitosa:", "4 módulos integrados (1 Config Server + 3 Microservicios) gobernados por 1 repositorio Git independiente."),
        ("Trazabilidad y GitOps:", "Cada modificación de parámetros queda registrada con hash de commit, fecha y autor."),
        ("Actualización Inmediata:", "Propagación de cambios en caliente vía /actuator/refresh sin caídas del servicio."),
        ("23 Pruebas Automatizadas:", "100% de tests unitarios y de integración aprobados en JUnit 5 y MockMvc.")
    ]
    for tit, desc in resultados:
        p = tf8_l.add_paragraph()
        p.text = f"• {tit} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    add_card(s8, Inches(6.9), Inches(1.7), Inches(5.6), Inches(5.0), COLOR_HIGHLIGHT, COLOR_ACCENT)
    tb8_r = s8.shapes.add_textbox(Inches(7.2), Inches(1.9), Inches(5.0), Inches(4.5))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True

    p = tf8_r.paragraphs[0]
    p.text = "💡 Lecciones y Limitaciones"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    lecciones = [
        ("Alcance de @RefreshScope:", "Afecta a beans Spring administrados; las propiedades del contenedor como el puerto de Tomcat exigen reinicio."),
        ("Cabeceras en Actuator:", "POST /actuator/refresh requiere Content-Type application/json para evitar HTTP 415."),
        ("Orden de Despliegue:", "Config Server debe ser el primer servicio en levantar para que los clientes puedan inicializarse."),
        ("Simplicidad Académica:", "El enfoque en memoria permitió centrar la atención en la arquitectura de configuración sin fricción de BD.")
    ]
    for tit, desc in lecciones:
        p = tf8_r.add_paragraph()
        p.text = f"• {tit} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentación generada exitosamente con {len(prs.slides)} diapositivas en: {output_path}")

if __name__ == "__main__":
    out_file = r"D:\Proyects\microservicios\sazon-express\docs\Presentacion_Sazon_Express.pptx"
    create_presentation(out_file)
