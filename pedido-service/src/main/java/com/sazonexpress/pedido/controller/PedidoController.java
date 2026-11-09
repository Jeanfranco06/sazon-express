package com.sazonexpress.pedido.controller;

import com.sazonexpress.pedido.dto.CrearPedidoRequest;
import com.sazonexpress.pedido.model.Pedido;
import com.sazonexpress.pedido.service.PedidoService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/pedidos")
public class PedidoController {

    private final PedidoService pedidoService;

    public PedidoController(PedidoService pedidoService) {
        this.pedidoService = pedidoService;
    }

    @GetMapping
    public ResponseEntity<List<Pedido>> listarPedidos() {
        return ResponseEntity.ok(pedidoService.listarPedidos());
    }

    @PostMapping
    public ResponseEntity<Pedido> registrarPedido(@RequestBody CrearPedidoRequest request) {
        Pedido creado = pedidoService.registrarPedido(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(creado);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Pedido> buscarPorId(@PathVariable Long id) {
        return ResponseEntity.ok(pedidoService.buscarPorId(id));
    }

    @GetMapping("/configuracion")
    public ResponseEntity<Map<String, Object>> obtenerConfiguracion() {
        return ResponseEntity.ok(pedidoService.obtenerConfiguracion());
    }
}
