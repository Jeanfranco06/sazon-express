package com.sazonexpress.menu;

import com.sazonexpress.menu.config.MenuProperties;
import com.sazonexpress.menu.service.MenuService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
    "restaurante.menu.nombre=Carta Sazón Express Test",
    "restaurante.menu.plato-destacado=Lomo saltado",
    "restaurante.menu.mensaje=Prueba de menú",
    "restaurante.menu.mostrar-disponibles=true"
})
@AutoConfigureMockMvc
class MenuServiceApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private MenuService menuService;

    @Autowired
    private MenuProperties menuProperties;

    @Test
    @DisplayName("El contexto de menu-service debe cargar correctamente")
    void contextLoads() {
        assertNotNull(menuService);
        assertNotNull(menuProperties);
    }

    @Test
    @DisplayName("GET /api/menu debe retornar la lista de platos")
    void testListarPlatos() throws Exception {
        mockMvc.perform(get("/api/menu"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(4))))
                .andExpect(jsonPath("$[0].nombre", notNullValue()));
    }

    @Test
    @DisplayName("GET /api/menu/destacado debe retornar el plato destacado configurado")
    void testPlatoDestacado() throws Exception {
        mockMvc.perform(get("/api/menu/destacado"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nombreDestacadoConfigurado", is("Lomo saltado")))
                .andExpect(jsonPath("$.plato.nombre", is("Lomo saltado")))
                .andExpect(jsonPath("$.mensaje", is("Prueba de menú")));
    }

    @Test
    @DisplayName("GET /api/menu/configuracion debe mostrar los valores centralizados")
    void testConfiguracion() throws Exception {
        mockMvc.perform(get("/api/menu/configuracion"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nombre", is("Carta Sazón Express Test")))
                .andExpect(jsonPath("$.platoDestacado", is("Lomo saltado")))
                .andExpect(jsonPath("$.mostrarDisponibles", is(true)));
    }

    @Test
    @DisplayName("Modificación dinámica de platoDestacado debe reflejarse en el servicio")
    void testActualizacionDinamicaPlatoDestacado() {
        // Simulamos el efecto de refresh actualizando la propiedad
        menuProperties.setPlatoDestacado("Ceviche clásico");
        var resultado = menuService.obtenerPlatoDestacado();
        assertEquals("Ceviche clásico", resultado.get("nombreDestacadoConfigurado"));

        // Restauramos
        menuProperties.setPlatoDestacado("Lomo saltado");
    }
}
