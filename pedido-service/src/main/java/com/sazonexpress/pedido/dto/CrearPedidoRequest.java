package com.sazonexpress.pedido.dto;

import com.sazonexpress.pedido.model.ItemPedido;

import java.util.ArrayList;
import java.util.List;

public class CrearPedidoRequest {
    private String cliente;
    private List<ItemPedido> items = new ArrayList<>();

    public CrearPedidoRequest() {
    }

    public CrearPedidoRequest(String cliente, List<ItemPedido> items) {
        this.cliente = cliente;
        this.items = items;
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
}
