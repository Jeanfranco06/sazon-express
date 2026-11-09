package com.sazonexpress.pedido.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Component;

/**
 * Propiedades centralizadas del microservicio de Pedidos.
 * Gobernadas por Spring Cloud Config Server con recarga dinámica (@RefreshScope).
 */
@Component
@RefreshScope
@ConfigurationProperties(prefix = "restaurante.pedidos")
public class PedidoProperties {

    private int maxPlatos = 5;
    private boolean pedidosHabilitados = true;
    private int tiempoEstimadoMinutos = 20;
    private String mensaje = "Tu pedido está siendo preparado";

    public int getMaxPlatos() {
        return maxPlatos;
    }

    public void setMaxPlatos(int maxPlatos) {
        this.maxPlatos = maxPlatos;
    }

    public boolean isPedidosHabilitados() {
        return pedidosHabilitados;
    }

    public void setPedidosHabilitados(boolean pedidosHabilitados) {
        this.pedidosHabilitados = pedidosHabilitados;
    }

    public int getTiempoEstimadoMinutos() {
        return tiempoEstimadoMinutos;
    }

    public void setTiempoEstimadoMinutos(int tiempoEstimadoMinutos) {
        this.tiempoEstimadoMinutos = tiempoEstimadoMinutos;
    }

    public String getMensaje() {
        return mensaje;
    }

    public void setMensaje(String mensaje) {
        this.mensaje = mensaje;
    }
}
