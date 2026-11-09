package com.sazonexpress.promocion.controller;

import com.sazonexpress.promocion.dto.CalculoDescuentoResponse;
import com.sazonexpress.promocion.model.Promocion;
import com.sazonexpress.promocion.service.PromocionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/promociones")
public class PromocionController {

    private final PromocionService promocionService;

    public PromocionController(PromocionService promocionService) {
        this.promocionService = promocionService;
    }

    @GetMapping
    public ResponseEntity<List<Promocion>> listarPromociones() {
        return ResponseEntity.ok(promocionService.listarPromociones());
    }

    @GetMapping("/destacada")
    public ResponseEntity<Map<String, Object>> obtenerPromocionDestacada() {
        return ResponseEntity.ok(promocionService.obtenerPromocionDestacada());
    }

    @GetMapping("/configuracion")
    public ResponseEntity<Map<String, Object>> obtenerConfiguracion() {
        return ResponseEntity.ok(promocionService.obtenerConfiguracion());
    }

    @GetMapping("/calcular")
    public ResponseEntity<CalculoDescuentoResponse> calcularPrecio(
            @RequestParam(name = "precio") BigDecimal precio) {
        return ResponseEntity.ok(promocionService.calcularPrecioConDescuento(precio));
    }
}
