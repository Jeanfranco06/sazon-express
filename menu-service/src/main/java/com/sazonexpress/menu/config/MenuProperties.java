package com.sazonexpress.menu.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Component;

/**
 * Propiedades centralizadas del microservicio de Menú.
 * Se obtienen desde Spring Cloud Config Server y soportan actualización dinámica con @RefreshScope.
 */
@Component
@RefreshScope
@ConfigurationProperties(prefix = "restaurante.menu")
public class MenuProperties {

    private String nombre = "Carta Sazón Express";
    private String platoDestacado = "Lomo saltado";
    private String mensaje = "Disfruta nuestros sabores";
    private boolean mostrarDisponibles = true;

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getPlatoDestacado() {
        return platoDestacado;
    }

    public void setPlatoDestacado(String platoDestacado) {
        this.platoDestacado = platoDestacado;
    }

    public String getMensaje() {
        return mensaje;
    }

    public void setMensaje(String mensaje) {
        this.mensaje = mensaje;
    }

    public boolean isMostrarDisponibles() {
        return mostrarDisponibles;
    }

    public void setMostrarDisponibles(boolean mostrarDisponibles) {
        this.mostrarDisponibles = mostrarDisponibles;
    }
}
