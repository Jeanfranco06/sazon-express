package com.sazonexpress.pedido;

import com.sazonexpress.pedido.config.PedidoProperties;
import com.sazonexpress.pedido.service.PedidoService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
    "restaurante.pedidos.max-platos=5",
    "restaurante.pedidos.pedidos-habilitados=true",
    "restaurante.pedidos.tiempo-estimado-minutos=20",
    "restaurante.pedidos.mensaje=Tu pedido está siendo preparado"
})
@AutoConfigureMockMvc
class PedidoServiceApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private PedidoService pedidoService;

    @Autowired
    private PedidoProperties pedidoProperties;

    @Test
    @DisplayName("El contexto de pedido-service debe iniciar correctamente")
    void contextLoads() {
        assertNotNull(pedidoService);
        assertNotNull(pedidoProperties);
    }

    @Test
    @DisplayName("GET /api/pedidos debe listar pedidos existentes")
    void testListarPedidos() throws Exception {
        mockMvc.perform(get("/api/pedidos"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(1))));
    }

    @Test
    @DisplayName("POST /api/pedidos con 5 platos debe ser aceptado exitosamente")
    void testCrearPedidoValidoLimiteCinco() throws Exception {
        String json = """
            {
                "cliente": "Carlos Ramírez",
                "items": [
                    { "plato": "Lomo saltado", "cantidad": 3, "precioUnitario": 38.00 },
                    { "plato": "Ceviche clásico", "cantidad": 2, "precioUnitario": 42.00 }
                ]
            }
            """;

        mockMvc.perform(post("/api/pedidos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", notNullValue()))
                .andExpect(jsonPath("$.totalPlatos", is(5)))
                .andExpect(jsonPath("$.tiempoEstimadoMinutos", is(20)))
                .andExpect(jsonPath("$.mensajeEstado", is("Tu pedido está siendo preparado")));
    }

    @Test
    @DisplayName("POST /api/pedidos con 6 platos debe ser rechazado por exceder max-platos=5")
    void testRechazarPedidoExcedeLimite() throws Exception {
        String json = """
            {
                "cliente": "Cliente Excesivo",
                "items": [
                    { "plato": "Lomo saltado", "cantidad": 6, "precioUnitario": 38.00 }
                ]
            }
            """;

        mockMvc.perform(post("/api/pedidos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("Actualización dinámica: cambiar max-platos a 2 debe rechazar un pedido de 3 platos")
    void testCambioDinamicoMaxPlatos() throws Exception {
        pedidoProperties.setMaxPlatos(2);

        String json = """
            {
                "cliente": "Cliente Tres Platos",
                "items": [
                    { "plato": "Arroz con pollo", "cantidad": 3, "precioUnitario": 28.00 }
                ]
            }
            """;

        mockMvc.perform(post("/api/pedidos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isBadRequest());

        // Restaurar estado
        pedidoProperties.setMaxPlatos(5);
    }

    @Test
    @DisplayName("Cuando pedidos-habilitados=false los pedidos deben ser rechazados")
    void testPedidosDeshabilitados() throws Exception {
        pedidoProperties.setPedidosHabilitados(false);

        String json = """
            {
                "cliente": "Cliente Desesperado",
                "items": [
                    { "plato": "Lomo saltado", "cantidad": 1, "precioUnitario": 38.00 }
                ]
            }
            """;

        mockMvc.perform(post("/api/pedidos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isBadRequest());

        // Restaurar estado
        pedidoProperties.setPedidosHabilitados(true);
    }

    @Test
    @DisplayName("GET /api/pedidos/configuracion debe devolver reglas centralizadas")
    void testConsultarConfiguracion() throws Exception {
        mockMvc.perform(get("/api/pedidos/configuracion"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.maxPlatos", is(5)))
                .andExpect(jsonPath("$.pedidosHabilitados", is(true)))
                .andExpect(jsonPath("$.tiempoEstimadoMinutos", is(20)));
    }
}
