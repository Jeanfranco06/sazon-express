package com.sazonexpress.configserver;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.config.environment.Environment;
import org.springframework.cloud.config.server.environment.EnvironmentRepository;

import java.io.File;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(properties = {
    // Apunta dinámicamente al directorio config-repo para la ejecución del test
    "spring.cloud.config.server.git.uri=file:///${user.dir}/../config-repo"
})
class ConfigServerApplicationTests {

    @Autowired
    private EnvironmentRepository environmentRepository;

    @Test
    @DisplayName("El contexto de Config Server debe iniciar correctamente")
    void contextLoads() {
        assertNotNull(environmentRepository, "EnvironmentRepository debe estar inyectado y disponible");
    }

    @Test
    @DisplayName("Debe recuperar las propiedades centralizadas de menu-service desde Git")
    void testRecuperarPropiedadesMenuService() {
        Environment env = environmentRepository.findOne("menu-service", "default", "main");
        assertNotNull(env, "El ambiente retornado por Config Server no debe ser nulo");
        assertFalse(env.getPropertySources().isEmpty(), "Debe contener PropertySources desde el repositorio Git");

        // Validar que contiene la fuente de propiedades de menu-service
        boolean contieneMenu = env.getPropertySources().stream()
                .anyMatch(ps -> ps.getName().contains("menu-service") || ps.getSource().containsKey("restaurante.menu.plato-destacado"));
        assertTrue(contieneMenu, "Debe incluir las propiedades de menu-service");
    }

    @Test
    @DisplayName("Debe recuperar las propiedades centralizadas de pedido-service desde Git")
    void testRecuperarPropiedadesPedidoService() {
        Environment env = environmentRepository.findOne("pedido-service", "default", "main");
        assertNotNull(env);
        assertFalse(env.getPropertySources().isEmpty());

        boolean contienePedido = env.getPropertySources().stream()
                .anyMatch(ps -> ps.getName().contains("pedido-service") || ps.getSource().containsKey("restaurante.pedidos.max-platos"));
        assertTrue(contienePedido, "Debe incluir las propiedades de pedido-service");
    }

    @Test
    @DisplayName("Debe recuperar las propiedades centralizadas de promocion-service desde Git")
    void testRecuperarPropiedadesPromocionService() {
        Environment env = environmentRepository.findOne("promocion-service", "default", "main");
        assertNotNull(env);
        assertFalse(env.getPropertySources().isEmpty());

        boolean contienePromo = env.getPropertySources().stream()
                .anyMatch(ps -> ps.getName().contains("promocion-service") || ps.getSource().containsKey("restaurante.promociones.descuento-porcentaje"));
        assertTrue(contienePromo, "Debe incluir las propiedades de promocion-service");
    }
}
