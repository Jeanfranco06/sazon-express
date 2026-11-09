package com.sazonexpress.pedido.service;

import com.sazonexpress.pedido.config.PedidoProperties;
import com.sazonexpress.pedido.dto.CrearPedidoRequest;
import com.sazonexpress.pedido.model.ItemPedido;
import com.sazonexpress.pedido.model.Pedido;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Service
@RefreshScope
public class PedidoService {

    private final PedidoProperties properties;
    private final Map<Long, Pedido> pedidos = new ConcurrentHashMap<>();
    private final AtomicLong contadorId = new AtomicLong(1);

    public PedidoService(PedidoProperties properties) {
        this.properties = properties;
        // Pedido inicial de ejemplo
        inicializarEjemplo();
    }

    private void inicializarEjemplo() {
        List<ItemPedido> items = new ArrayList<>();
        items.add(new ItemPedido("Lomo saltado", 2, new BigDecimal("38.00")));
        items.add(new ItemPedido("Ceviche clásico", 1, new BigDecimal("42.00")));

        Pedido pedidoInicial = new Pedido(
                contadorId.getAndIncrement(),
                "Cliente Inicial",
                items,
                3,
                new BigDecimal("118.00"),
                "PREPARANDO",
                properties.getTiempoEstimadoMinutos(),
                properties.getMensaje()
        );
        pedidos.put(pedidoInicial.getId(), pedidoInicial);
    }

    public Pedido registrarPedido(CrearPedidoRequest request) {
        // Validación 1: Verificar si los pedidos están habilitados centralmente
        if (!properties.isPedidosHabilitados()) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Los pedidos están deshabilitados temporalmente por política del restaurante."
            );
        }

        // Validación 2: Cliente y lista de items
        if (request == null || request.getItems() == null || request.getItems().isEmpty()) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "El pedido debe contener al menos un plato."
            );
        }

        String cliente = (request.getCliente() != null && !request.getCliente().trim().isEmpty())
                ? request.getCliente().trim()
                : "Cliente Mostrador";

        // Validación 3: Cantidad total de platos respecto al límite centralizado
        int totalPlatos = request.getItems().stream()
                .mapToInt(ItemPedido::getCantidad)
                .sum();

        if (totalPlatos <= 0) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "La cantidad total de platos debe ser mayor a cero."
            );
        }

        if (totalPlatos > properties.getMaxPlatos()) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    String.format(
                            "El pedido contiene %d platos, superando el límite máximo configurado de %d platos.",
                            totalPlatos,
                            properties.getMaxPlatos()
                    )
            );
        }

        // Cálculo de montos
        BigDecimal totalMonto = BigDecimal.ZERO;
        for (ItemPedido item : request.getItems()) {
            if (item.getPrecioUnitario() == null || item.getPrecioUnitario().compareTo(BigDecimal.ZERO) < 0) {
                item.setPrecioUnitario(new BigDecimal("30.00")); // Precio referencial por defecto
            }
            totalMonto = totalMonto.add(item.getSubtotal());
        }

        Long nuevoId = contadorId.getAndIncrement();
        Pedido nuevoPedido = new Pedido(
                nuevoId,
                cliente,
                request.getItems(),
                totalPlatos,
                totalMonto,
                "EN_PREPARACION",
                properties.getTiempoEstimadoMinutos(),
                properties.getMensaje()
        );

        pedidos.put(nuevoId, nuevoPedido);
        return nuevoPedido;
    }

    public List<Pedido> listarPedidos() {
        return new ArrayList<>(pedidos.values());
    }

    public Pedido buscarPorId(Long id) {
        Pedido pedido = pedidos.get(id);
        if (pedido == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Pedido no encontrado con ID: " + id);
        }
        return pedido;
    }

    public Map<String, Object> obtenerConfiguracion() {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("maxPlatos", properties.getMaxPlatos());
        config.put("pedidosHabilitados", properties.isPedidosHabilitados());
        config.put("tiempoEstimadoMinutos", properties.getTiempoEstimadoMinutos());
        config.put("mensaje", properties.getMensaje());
        config.put("origen", "Spring Cloud Config Server -> Git: pedido-service.yml");
        return config;
    }
}
