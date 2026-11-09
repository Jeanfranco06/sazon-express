package com.sazonexpress.promocion;

import com.sazonexpress.promocion.config.PromocionProperties;
import com.sazonexpress.promocion.service.PromocionService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
    "restaurante.promociones.habilitadas=true",
    "restaurante.promociones.descuento-porcentaje=15",
    "restaurante.promociones.promocion-destacada=Combo familiar",
    "restaurante.promociones.mensaje=Aprovecha nuestras promociones"
})
@AutoConfigureMockMvc
class PromocionServiceApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private PromocionService promocionService;

    @Autowired
    private PromocionProperties promocionProperties;

    @Test
    @DisplayName("El contexto de promocion-service debe iniciar correctamente")
    void contextLoads() {
        assertNotNull(promocionService);
        assertNotNull(promocionProperties);
    }

    @Test
    @DisplayName("GET /api/promociones debe retornar el listado de promociones activas")
    void testListarPromociones() throws Exception {
        mockMvc.perform(get("/api/promociones"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(2))));
    }

    @Test
    @DisplayName("GET /api/promociones/destacada debe retornar la promoción configurada")
    void testPromocionDestacada() throws Exception {
        mockMvc.perform(get("/api/promociones/destacada"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.promocionDestacada", is("Combo familiar")))
                .andExpect(jsonPath("$.descuentoGeneralPorcentaje", is(15)))
                .andExpect(jsonPath("$.mensaje", is("Aprovecha nuestras promociones")));
    }

    @Test
    @DisplayName("GET /api/promociones/calcular?precio=50 con 15% de descuento debe resultar en 42.50")
    void testCalcularDescuentoQuincePorCiento() throws Exception {
        mockMvc.perform(get("/api/promociones/calcular?precio=50"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.precioOriginal", is(50.00)))
                .andExpect(jsonPath("$.porcentajeDescuentoAplicado", is(15)))
                .andExpect(jsonPath("$.montoDescuento", is(7.50)))
                .andExpect(jsonPath("$.precioFinal", is(42.50)))
                .andExpect(jsonPath("$.promocionesHabilitadas", is(true)));
    }

    @Test
    @DisplayName("Demostración dinámica: al cambiar descuento a 20%, S/ 50 debe calcularse en S/ 40.00")
    void testCalculoDescuentoVeintePorCiento() throws Exception {
        // Simulamos actualización dinámica desde Git
        promocionProperties.setDescuentoPorcentaje(20);

        mockMvc.perform(get("/api/promociones/calcular?precio=50"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.precioOriginal", is(50.00)))
                .andExpect(jsonPath("$.porcentajeDescuentoAplicado", is(20)))
                .andExpect(jsonPath("$.montoDescuento", is(10.00)))
                .andExpect(jsonPath("$.precioFinal", is(40.00)));

        // Restauramos
        promocionProperties.setDescuentoPorcentaje(15);
    }

    @Test
    @DisplayName("GET /api/promociones/calcular con precio cero o negativo debe responder 400 Bad Request")
    void testValidacionPrecioInvalido() throws Exception {
        mockMvc.perform(get("/api/promociones/calcular?precio=-10"))
                .andExpect(status().isBadRequest());

        mockMvc.perform(get("/api/promociones/calcular?precio=0"))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("GET /api/promociones/configuracion debe reflejar propiedades centralizadas")
    void testConsultarConfiguracion() throws Exception {
        mockMvc.perform(get("/api/promociones/configuracion"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.habilitadas", is(true)))
                .andExpect(jsonPath("$.descuentoPorcentaje", is(15)))
                .andExpect(jsonPath("$.promocionDestacada", is("Combo familiar")));
    }
}
