package com.sazonexpress.pedido.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class Pedido {
    private Long id;
    private String cliente;
    private List<ItemPedido> items = new ArrayList<>();
    private int totalPlatos;
    private BigDecimal totalMonto;
    private String estado;
    private int tiempoEstimadoMinutos;
    private String mensajeEstado;
    private LocalDateTime fechaRegistro;

    public Pedido() {
        this.fechaRegistro = LocalDateTime.now();
    }

    public Pedido(Long id, String cliente, List<ItemPedido> items, int totalPlatos, BigDecimal totalMonto,
                  String estado, int tiempoEstimadoMinutos, String mensajeEstado) {
        this.id = id;
        this.cliente = cliente;
        this.items = items;
        this.totalPlatos = totalPlatos;
        this.totalMonto = totalMonto;
        this.estado = estado;
        this.tiempoEstimadoMinutos = tiempoEstimadoMinutos;
        this.mensajeEstado = mensajeEstado;
        this.fechaRegistro = LocalDateTime.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCliente() {
        return cliente;
    }

    public void setCliente(String cliente) {
        this.cliente = cliente;
    }

    public List<ItemPedido> getItems() {
        return items;
    }

    public void setItems(List<ItemPedido> items) {
        this.items = items;
    }

    public int getTotalPlatos() {
        return totalPlatos;
    }

    public void setTotalPlatos(int totalPlatos) {
        this.totalPlatos = totalPlatos;
    }

    public BigDecimal getTotalMonto() {
        return totalMonto;
    }

    public void setTotalMonto(BigDecimal totalMonto) {
        this.totalMonto = totalMonto;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public int getTiempoEstimadoMinutos() {
        return tiempoEstimadoMinutos;
    }

    public void setTiempoEstimadoMinutos(int tiempoEstimadoMinutos) {
        this.tiempoEstimadoMinutos = tiempoEstimadoMinutos;
    }

    public String getMensajeEstado() {
        return mensajeEstado;
    }

    public void setMensajeEstado(String mensajeEstado) {
        this.mensajeEstado = mensajeEstado;
    }

    public LocalDateTime getFechaRegistro() {
        return fechaRegistro;
    }

    public void setFechaRegistro(LocalDateTime fechaRegistro) {
        this.fechaRegistro = fechaRegistro;
    }
}
