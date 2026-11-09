package com.sazonexpress.promocion.service;

import com.sazonexpress.promocion.config.PromocionProperties;
import com.sazonexpress.promocion.dto.CalculoDescuentoResponse;
import com.sazonexpress.promocion.model.Promocion;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

@Service
@RefreshScope
public class PromocionService {

    private final PromocionProperties properties;
    private final List<Promocion> promociones = new ArrayList<>();

    public PromocionService(PromocionProperties properties) {
        this.properties = properties;
        inicializarPromociones();
    }

    private void inicializarPromociones() {
        promociones.add(new Promocion(1L, "COMBO_FAMILIAR", "Combo familiar",
                "1 Pollo a la brasa + papas familiares + gaseosa 1.5L", 15, true));
        promociones.add(new Promocion(2L, "DUO_CRIOLLO", "Dúo Criollo",
                "Lomo saltado + Ají de gallina para 2 personas", 10, true));
        promociones.add(new Promocion(3L, "ALMUERZO_EJECUTIVO", "Almuerzo Ejecutivo",
                "Entrada + Plato de fondo + Bebida del día", 5, true));
    }

    public List<Promocion> listarPromociones() {
        if (!properties.isHabilitadas()) {
            return Collections.emptyList();
        }
        return new ArrayList<>(promociones);
    }

    public Map<String, Object> obtenerPromocionDestacada() {
        Map<String, Object> resultado = new LinkedHashMap<>();
        resultado.put("promocionesHabilitadas", properties.isHabilitadas());
        resultado.put("mensaje", properties.getMensaje());
        resultado.put("promocionDestacada", properties.getPromocionDestacada());
        resultado.put("descuentoGeneralPorcentaje", properties.getDescuentoPorcentaje());

        Optional<Promocion> promoOpt = promociones.stream()
                .filter(p -> p.getTitulo().equalsIgnoreCase(properties.getPromocionDestacada().trim()))
                .findFirst();

        promoOpt.ifPresent(promocion -> resultado.put("detalle", promocion));
        return resultado;
    }

    public CalculoDescuentoResponse calcularPrecioConDescuento(BigDecimal precioOriginal) {
        if (precioOriginal == null || precioOriginal.compareTo(BigDecimal.ZERO) <= 0) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "El precio debe ser un valor numérico mayor a cero."
            );
        }

        BigDecimal precioNormalizado = precioOriginal.setScale(2, RoundingMode.HALF_UP);

        if (!properties.isHabilitadas()) {
            return new CalculoDescuentoResponse(
                    precioNormalizado,
                    0,
                    BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP),
                    precioNormalizado,
                    false,
                    "Las promociones se encuentran deshabilitadas por política comercial."
            );
        }

        int porcentaje = properties.getDescuentoPorcentaje();
        if (porcentaje < 0 || porcentaje > 100) {
            throw new ResponseStatusException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    "El porcentaje de descuento configurado (" + porcentaje + "%) es inválido."
            );
        }

        BigDecimal factor = BigDecimal.valueOf(porcentaje).divide(BigDecimal.valueOf(100), 4, RoundingMode.HALF_UP);
        BigDecimal montoDescuento = precioNormalizado.multiply(factor).setScale(2, RoundingMode.HALF_UP);
        BigDecimal precioFinal = precioNormalizado.subtract(montoDescuento).setScale(2, RoundingMode.HALF_UP);

        return new CalculoDescuentoResponse(
                precioNormalizado,
                porcentaje,
                montoDescuento,
                precioFinal,
                true,
                properties.getMensaje()
        );
    }

    public Map<String, Object> obtenerConfiguracion() {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("habilitadas", properties.isHabilitadas());
        config.put("descuentoPorcentaje", properties.getDescuentoPorcentaje());
        config.put("promocionDestacada", properties.getPromocionDestacada());
        config.put("mensaje", properties.getMensaje());
        config.put("origen", "Spring Cloud Config Server -> Git: promocion-service.yml");
        return config;
    }
}
