package com.sazonexpress.menu.controller;

import com.sazonexpress.menu.model.Plato;
import com.sazonexpress.menu.service.MenuService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/menu")
public class MenuController {

    private final MenuService menuService;

    public MenuController(MenuService menuService) {
        this.menuService = menuService;
    }

    @GetMapping
    public ResponseEntity<List<Plato>> listarPlatos() {
        return ResponseEntity.ok(menuService.listarPlatos());
    }

    @GetMapping("/destacado")
    public ResponseEntity<Map<String, Object>> obtenerPlatoDestacado() {
        return ResponseEntity.ok(menuService.obtenerPlatoDestacado());
    }

    @GetMapping("/configuracion")
    public ResponseEntity<Map<String, Object>> obtenerConfiguracion() {
        return ResponseEntity.ok(menuService.obtenerConfiguracion());
    }
}
