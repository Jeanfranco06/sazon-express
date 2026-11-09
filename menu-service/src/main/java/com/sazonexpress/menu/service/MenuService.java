package com.sazonexpress.menu.service;

import com.sazonexpress.menu.config.MenuProperties;
import com.sazonexpress.menu.model.Plato;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RefreshScope
public class MenuService {

    private final MenuProperties properties;
    private final List<Plato> catalogo = new ArrayList<>();

    public MenuService(MenuProperties properties) {
        this.properties = properties;
        inicializarCatalogo();
    }

    private void inicializarCatalogo() {
        catalogo.add(new Plato(1L, "Lomo saltado", "Fondos", new BigDecimal("38.00"), true));
        catalogo.add(new Plato(2L, "Ají de gallina", "Fondos", new BigDecimal("30.00"), true));
        catalogo.add(new Plato(3L, "Arroz con pollo", "Fondos", new BigDecimal("28.00"), true));
        catalogo.add(new Plato(4L, "Ceviche clásico", "Marinos", new BigDecimal("42.00"), true));
        catalogo.add(new Plato(5L, "Causa limeña", "Entradas", new BigDecimal("24.00"), true));
    }

    public List<Plato> listarPlatos() {
        if (properties.isMostrarDisponibles()) {
            return catalogo.stream()
                    .filter(Plato::isDisponible)
                    .collect(Collectors.toList());
        }
        return new ArrayList<>(catalogo);
    }

    public Optional<Plato> buscarPorNombre(String nombre) {
        return catalogo.stream()
                .filter(p -> p.getNombre().equalsIgnoreCase(nombre.trim()))
                .findFirst();
    }

    public Map<String, Object> obtenerPlatoDestacado() {
        String nombreDestacado = properties.getPlatoDestacado();
        Optional<Plato> platoOpt = buscarPorNombre(nombreDestacado);

        Map<String, Object> resultado = new LinkedHashMap<>();
        resultado.put("mensaje", properties.getMensaje());
        resultado.put("nombreDestacadoConfigurado", nombreDestacado);

        if (platoOpt.isPresent()) {
            resultado.put("plato", platoOpt.get());
        } else {
            // Si el plato configurado dinámicamente es nuevo o especial
            resultado.put("plato", new Plato(999L, nombreDestacado, "Especialidad del Chef", new BigDecimal("35.00"), true));
            resultado.put("nota", "Plato destacado provisto dinámicamente por la configuración centralizada");
        }
        return resultado;
    }

    public Map<String, Object> obtenerConfiguracion() {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("nombre", properties.getNombre());
        config.put("platoDestacado", properties.getPlatoDestacado());
        config.put("mensaje", properties.getMensaje());
        config.put("mostrarDisponibles", properties.isMostrarDisponibles());
        config.put("origen", "Spring Cloud Config Server -> Git: menu-service.yml");
        return config;
    }
}
