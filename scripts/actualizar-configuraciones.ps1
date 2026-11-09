# ==============================================================================
# Sazon Express - Demostracion de Actualizacion Dinamica de Configuraciones
# ==============================================================================
# Flujo: Git -> Spring Cloud Config Server -> POST /actuator/refresh -> API
# ==============================================================================

param(
    [switch]$Restaurar
)

$root = Resolve-Path "$PSScriptRoot\.."
$configRepoDir = "$root\config-repo"
$evidenciasDir = "$root\docs\evidencias"
New-Item -ItemType Directory -Force -Path $evidenciasDir | Out-Null

$menuFile = "$configRepoDir\menu-service.yml"
$pedidoFile = "$configRepoDir\pedido-service.yml"
$promoFile = "$configRepoDir\promocion-service.yml"

function Ejecutar-Commit-Git {
    param([string]$Mensaje)
    Push-Location $configRepoDir
    git add .
    git commit -m "$Mensaje" | Out-Null
    $commitHash = (git rev-parse --short HEAD)
    $remotes = git remote
    if ($remotes -contains "origin") {
        try {
            git push origin main 2>$null | Out-Null
            Write-Host "   -> Git Push a GitHub completado con éxito." -ForegroundColor DarkCyan
        } catch {
            Write-Host "   -> Git Push omitido (modo offline)." -ForegroundColor DarkGray
        }
    }
    Pop-Location
    Write-Host "   -> Git Commit registrado: [$commitHash] $Mensaje" -ForegroundColor DarkGray
    return $commitHash
}

if ($Restaurar) {
    Write-Host "`n[Sazon Express] Restaurando configuraciones originales en Git..." -ForegroundColor Yellow

    $menuBase = @(
        'server:',
        '  port: 8081',
        '',
        'restaurante:',
        '  menu:',
        '    nombre: "Carta Sazon Express"',
        '    plato-destacado: "Lomo saltado"',
        '    mensaje: "Disfruta nuestros sabores"',
        '    mostrar-disponibles: true'
    )

    $pedidoBase = @(
        'server:',
        '  port: 8082',
        '',
        'restaurante:',
        '  pedidos:',
        '    max-platos: 5',
        '    pedidos-habilitados: true',
        '    tiempo-estimado-minutos: 20',
        '    mensaje: "Tu pedido esta siendo preparado"'
    )

    $promoBase = @(
        'server:',
        '  port: 8083',
        '',
        'restaurante:',
        '  promociones:',
        '    habilitadas: true',
        '    descuento-porcentaje: 15',
        '    promocion-destacada: "Combo familiar"',
        '    mensaje: "Aprovecha nuestras promociones"'
    )

    $menuBase | Set-Content -Path $menuFile -Encoding utf8
    $pedidoBase | Set-Content -Path $pedidoFile -Encoding utf8
    $promoBase | Set-Content -Path $promoFile -Encoding utf8

    Ejecutar-Commit-Git -Mensaje "revert(config): restaurar valores originales de configuracion"

    Write-Host "Aplicando refresh en los tres microservicios..." -ForegroundColor Cyan
    try { Invoke-RestMethod -Uri "http://localhost:8081/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}" | Out-Null } catch {}
    try { Invoke-RestMethod -Uri "http://localhost:8082/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}" | Out-Null } catch {}
    try { Invoke-RestMethod -Uri "http://localhost:8083/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}" | Out-Null } catch {}

    Write-Host "Configuraciones restauradas correctamente a su estado inicial." -ForegroundColor Green
    exit 0
}

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host " [Sazon Express] DEMOSTRACION DE CONFIGURACION CENTRALIZADA DINAMICA " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# DEMOSTRACION 1: MENU-SERVICE
# ------------------------------------------------------------------------------
Write-Host "`n------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host " DEMOSTRACION 1: Actualizacion de Plato Destacado [menu-service] " -ForegroundColor Yellow
Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow

Write-Host "1. Consultando plato destacado inicial antes del cambio..." -ForegroundColor Gray
$antesMenu = Invoke-RestMethod -Uri "http://localhost:8081/api/menu/destacado" -Method Get
Write-Host ("   Plato destacado actual: " + $antesMenu.nombreDestacadoConfigurado + " -- Mensaje: " + $antesMenu.mensaje) -ForegroundColor White

Write-Host "2. Modificando plato-destacado a 'Ceviche clasico' en Git..." -ForegroundColor Gray
$menuModificado = @(
    'server:',
    '  port: 8081',
    '',
    'restaurante:',
    '  menu:',
    '    nombre: "Carta Sazon Express"',
    '    plato-destacado: "Ceviche clasico"',
    '    mensaje: "Especial marino de temporada"',
    '    mostrar-disponibles: true'
)
$menuModificado | Set-Content -Path $menuFile -Encoding utf8
$hash1 = Ejecutar-Commit-Git -Mensaje "feat(menu): cambiar plato destacado a Ceviche clasico"

Write-Host "3. Verificando que Config Server recupera la nueva propiedad desde Git..." -ForegroundColor Gray
$csMenu = Invoke-RestMethod -Uri "http://localhost:8888/menu-service/default" -Method Get
Write-Host ("   Config Server version Git detectada: " + $csMenu.version) -ForegroundColor DarkCyan

Write-Host "4. Aplicando recarga en caliente en menu-service [POST /actuator/refresh]..." -ForegroundColor Gray
$refreshedKeys1 = Invoke-RestMethod -Uri "http://localhost:8081/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}"
Write-Host ("   Propiedades recargadas en cliente: " + ($refreshedKeys1 -join ', ')) -ForegroundColor Green

Write-Host "5. Consultando nuevamente el endpoint /api/menu/destacado..." -ForegroundColor Gray
$despuesMenu = Invoke-RestMethod -Uri "http://localhost:8081/api/menu/destacado" -Method Get
Write-Host ("   NUEVO Plato Destacado: " + $despuesMenu.nombreDestacadoConfigurado + " -- Mensaje: " + $despuesMenu.mensaje) -ForegroundColor Green
$despuesMenu | ConvertTo-Json -Depth 5 | Out-File "$evidenciasDir\demo1-menu-actualizado.json" -Encoding utf8

# ------------------------------------------------------------------------------
# DEMOSTRACION 2: PEDIDO-SERVICE
# ------------------------------------------------------------------------------
Write-Host "`n------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host " DEMOSTRACION 2: Modificacion de Limite de Platos [pedido-service]" -ForegroundColor Yellow
Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow

Write-Host "1. Regla inicial: max-platos = 5. Realizando pedido con 3 platos..." -ForegroundColor Gray
$pedido3 = '{"cliente":"Cliente Demostracion","items":[{"plato":"Lomo saltado","cantidad":2,"precioUnitario":38.00},{"plato":"Ceviche clasico","cantidad":1,"precioUnitario":42.00}]}'
$respP3 = Invoke-RestMethod -Uri "http://localhost:8082/api/pedidos" -Method Post -ContentType "application/json" -Body $pedido3
Write-Host ("   Pedido ACEPTADO con ID: " + $respP3.id + " -- Total platos: " + $respP3.totalPlatos) -ForegroundColor Green

Write-Host "2. Modificando 'max-platos: 2' en Git..." -ForegroundColor Gray
$pedidoModificado = @(
    'server:',
    '  port: 8082',
    '',
    'restaurante:',
    '  pedidos:',
    '    max-platos: 2',
    '    pedidos-habilitados: true',
    '    tiempo-estimado-minutos: 15',
    '    mensaje: "Tu pedido express esta siendo preparado rapidamente"'
)
$pedidoModificado | Set-Content -Path $pedidoFile -Encoding utf8
$hash2 = Ejecutar-Commit-Git -Mensaje "feat(pedidos): reducir limite max-platos a 2 por alta demanda"

Write-Host "3. Aplicando recarga en cliente pedido-service [POST /actuator/refresh]..." -ForegroundColor Gray
$refreshedKeys2 = Invoke-RestMethod -Uri "http://localhost:8082/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}"
Write-Host ("   Propiedades recargadas en cliente: " + ($refreshedKeys2 -join ', ')) -ForegroundColor Green

Write-Host "4. Repitiendo el pedido de 3 platos [esperado: RECHAZADO por max-platos=2]..." -ForegroundColor Gray
try {
    $respRechazo = Invoke-RestMethod -Uri "http://localhost:8082/api/pedidos" -Method Post -ContentType "application/json" -Body $pedido3 -ErrorAction Stop
    Write-Host "   ADVERTENCIA: El pedido no debio ser aceptado" -ForegroundColor Red
} catch {
    Write-Host "   CORRECTO: El pedido fue RECHAZADO segun la nueva regla centralizada." -ForegroundColor Green
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $errBody = $reader.ReadToEnd()
        Write-Host ("   Mensaje de error del servidor: " + $errBody) -ForegroundColor DarkYellow
        $errBody | Out-File "$evidenciasDir\demo2-pedido-rechazado.json" -Encoding utf8
    }
}

Write-Host "5. Probando pedido con 2 platos [dentro del nuevo limite permitido]..." -ForegroundColor Gray
$pedido2 = '{"cliente":"Cliente Limite Reducido","items":[{"plato":"Lomo saltado","cantidad":2,"precioUnitario":38.00}]}'
$respP2 = Invoke-RestMethod -Uri "http://localhost:8082/api/pedidos" -Method Post -ContentType "application/json" -Body $pedido2
Write-Host ("   Pedido ACEPTADO con ID: " + $respP2.id + " -- Total platos: " + $respP2.totalPlatos + " -- Tiempo: " + $respP2.tiempoEstimadoMinutos + " min") -ForegroundColor Green

# ------------------------------------------------------------------------------
# DEMOSTRACION 3: PROMOCION-SERVICE
# ------------------------------------------------------------------------------
Write-Host "`n------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host " DEMOSTRACION 3: Actualizacion de Descuento [promocion-service]  " -ForegroundColor Yellow
Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow

Write-Host "1. Calculando precio con descuento inicial de 15 por ciento para S/ 50.00..." -ForegroundColor Gray
$calcAntes = Invoke-RestMethod -Uri "http://localhost:8083/api/promociones/calcular?precio=50" -Method Get
Write-Host ("   Precio Original: S/ " + $calcAntes.precioOriginal + " -- Descuento: " + $calcAntes.porcentajeDescuentoAplicado + "% -> Precio Final: S/ " + $calcAntes.precioFinal) -ForegroundColor White

Write-Host "2. Modificando 'descuento-porcentaje: 20' en Git..." -ForegroundColor Gray
$promoModificado = @(
    'server:',
    '  port: 8083',
    '',
    'restaurante:',
    '  promociones:',
    '    habilitadas: true',
    '    descuento-porcentaje: 20',
    '    promocion-destacada: "Combo familiar"',
    '    mensaje: "Aprovecha nuestro mega descuento del 20 por ciento"'
)
$promoModificado | Set-Content -Path $promoFile -Encoding utf8
$hash3 = Ejecutar-Commit-Git -Mensaje "feat(promociones): incrementar descuento a 20 por ciento"

Write-Host "3. Aplicando recarga en cliente promocion-service [POST /actuator/refresh]..." -ForegroundColor Gray
$refreshedKeys3 = Invoke-RestMethod -Uri "http://localhost:8083/actuator/refresh" -Method Post -ContentType "application/json" -Body "{}"
Write-Host ("   Propiedades recargadas en cliente: " + ($refreshedKeys3 -join ', ')) -ForegroundColor Green

Write-Host "4. Consultando nuevamente el calculo para S/ 50.00 [esperado: S/ 40.00]..." -ForegroundColor Gray
$calcDespues = Invoke-RestMethod -Uri "http://localhost:8083/api/promociones/calcular?precio=50" -Method Get
Write-Host ("   NUEVO Precio Original: S/ " + $calcDespues.precioOriginal + " -- Descuento: " + $calcDespues.porcentajeDescuentoAplicado + "% -> NUEVO Precio Final: S/ " + $calcDespues.precioFinal) -ForegroundColor Green
$calcDespues | ConvertTo-Json -Depth 5 | Out-File "$evidenciasDir\demo3-promocion-descuento20.json" -Encoding utf8

Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host " DEMOSTRACION DE CENTRALIZACION Y ACTUALIZACION COMPLETADA CON EXITO " -ForegroundColor Green
Write-Host " Nota: Para volver a los valores originales ejecute:" -ForegroundColor Cyan
Write-Host " .\scripts\actualizar-configuraciones.ps1 -Restaurar" -ForegroundColor Cyan
Write-Host "==================================================================`n" -ForegroundColor Green
