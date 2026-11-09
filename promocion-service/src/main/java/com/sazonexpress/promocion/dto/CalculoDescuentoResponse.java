package com.sazonexpress.promocion.dto;

import java.math.BigDecimal;

public class CalculoDescuentoResponse {
    private BigDecimal precioOriginal;
    private int porcentajeDescuentoAplicado;
    private BigDecimal montoDescuento;
    private BigDecimal precioFinal;
    private boolean promocionesHabilitadas;
    private String mensaje;

    public CalculoDescuentoResponse() {
    }

    public CalculoDescuentoResponse(BigDecimal precioOriginal, int porcentajeDescuentoAplicado,
                                    BigDecimal montoDescuento, BigDecimal precioFinal,
                                    boolean promocionesHabilitadas, String mensaje) {
        this.precioOriginal = precioOriginal;
        this.porcentajeDescuentoAplicado = porcentajeDescuentoAplicado;
        this.montoDescuento = montoDescuento;
        this.precioFinal = precioFinal;
        this.promocionesHabilitadas = promocionesHabilitadas;
        this.mensaje = mensaje;
    }

    public BigDecimal getPrecioOriginal() {
        return precioOriginal;
    }

    public void setPrecioOriginal(BigDecimal precioOriginal) {
        this.precioOriginal = precioOriginal;
    }

    public int getPorcentajeDescuentoAplicado() {
        return porcentajeDescuentoAplicado;
    }

    public void setPorcentajeDescuentoAplicado(int porcentajeDescuentoAplicado) {
        this.porcentajeDescuentoAplicado = porcentajeDescuentoAplicado;
    }

    public BigDecimal getMontoDescuento() {
        return montoDescuento;
    }

    public void setMontoDescuento(BigDecimal montoDescuento) {
        this.montoDescuento = montoDescuento;
    }

    public BigDecimal getPrecioFinal() {
        return precioFinal;
    }

    public void setPrecioFinal(BigDecimal precioFinal) {
        this.precioFinal = precioFinal;
    }

    public boolean isPromocionesHabilitadas() {
        return promocionesHabilitadas;
    }

    public void setPromocionesHabilitadas(boolean promocionesHabilitadas) {
        this.promocionesHabilitadas = promocionesHabilitadas;
    }

    public String getMensaje() {
        return mensaje;
    }

    public void setMensaje(String mensaje) {
        this.mensaje = mensaje;
    }
}
