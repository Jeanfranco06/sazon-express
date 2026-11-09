package com.sazonexpress.promocion.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Component;

/**
 * Propiedades centralizadas del microservicio de Promociones.
 * Obtenidas dinámicamente de Spring Cloud Config Server y refrescables con @RefreshScope.
 */
@Component
@RefreshScope
@ConfigurationProperties(prefix = "restaurante.promociones")
public class PromocionProperties {

    private boolean habilitadas = true;
    private int descuentoPorcentaje = 15;
    private String promocionDestacada = "Combo familiar";
    private String mensaje = "Aprovecha nuestras promociones";

    public boolean isHabilitadas() {
        return habilitadas;
    }

    public void setHabilitadas(boolean habilitadas) {
        this.habilitadas = habilitadas;
    }

    public int getDescuentoPorcentaje() {
        return descuentoPorcentaje;
    }

    public void setDescuentoPorcentaje(int descuentoPorcentaje) {
        this.descuentoPorcentaje = descuentoPorcentaje;
    }

    public String getPromocionDestacada() {
        return promocionDestacada;
    }

    public void setPromocionDestacada(String promocionDestacada) {
        this.promocionDestacada = promocionDestacada;
    }

    public String getMensaje() {
        return mensaje;
    }

    public void setMensaje(String mensaje) {
        this.mensaje = mensaje;
    }
}
