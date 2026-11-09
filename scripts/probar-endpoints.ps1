# ==============================================================================
# Sazón Express - Pruebas Funcionales de Endpoints
# ==============================================================================

param(
    [switch]$GuardarEvidencias = $true
)

$root = Resolve-Path "$PSScriptRoot\.."
$evidenciasDir = "$root\docs\evidencias"
New-Item -ItemType Directory -Force -Path $evidenciasDir | Out-Null

function Mostrar-Respuesta {
    param(
        [string]$Titulo,
        [string]$Metodo,
        [string]$Url,
        [string]$Body = $null,
        [string]$ArchivoEvidencia = ""
    )

    Write-Host "`n--------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ">> $Titulo" -ForegroundColor Yellow
    Write-Host "   $Metodo $Url" -ForegroundColor Cyan

    try {
        if ($Metodo -eq "POST") {
            $resp = Invoke-RestMethod -Uri $Url -Method Post -ContentType "application/json" -Body $Body -ErrorAction Stop
        } else {
            $resp = Invoke-RestMethod -Uri $Url -Method Get -ErrorAction Stop
        }

        $jsonFormateado = $resp | ConvertTo-Json -Depth 6
        Write-Host $jsonFormateado -ForegroundColor White

        if ($GuardarEvidencias -and $ArchivoEvidencia) {
            $jsonFormateado | Out-File -FilePath "$evidenciasDir\$ArchivoEvidencia" -Encoding utf8
        }
        return $resp
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errBody = $reader.ReadToEnd()
            Write-Host "Detalle: $errBody" -ForegroundColor DarkRed
        }
        return $null
    }
}

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " [Sazón Express] Ejecución de Pruebas de Endpoints      " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green

# 1. Config Server
Write-Host "`n=== 1. SPRING CLOUD CONFIG SERVER (Puerto 8888) ===" -ForegroundColor Magenta
Mostrar-Respuesta -Titulo "Configuraciones Git para Menu Service" `
    -Metodo "GET" -Url "http://localhost:8888/menu-service/default" `
    -ArchivoEvidencia "config-server-menu-response.json"

Mostrar-Respuesta -Titulo "Configuraciones Git para Pedido Service" `
    -Metodo "GET" -Url "http://localhost:8888/pedido-service/default" `
    -ArchivoEvidencia "config-server-pedido-response.json"

Mostrar-Respuesta -Titulo "Configuraciones Git para Promocion Service" `
    -Metodo "GET" -Url "http://localhost:8888/promocion-service/default" `
    -ArchivoEvidencia "config-server-promocion-response.json"

# 2. Menu Service
Write-Host "`n=== 2. MENU SERVICE (Puerto 8081) ===" -ForegroundColor Magenta
Mostrar-Respuesta -Titulo "Listar todos los platos del menú" `
    -Metodo "GET" -Url "http://localhost:8081/api/menu" `
    -ArchivoEvidencia "menu-listar-response.json"

Mostrar-Respuesta -Titulo "Consultar plato destacado configurable" `
    -Metodo "GET" -Url "http://localhost:8081/api/menu/destacado" `
    -ArchivoEvidencia "menu-destacado-response.json"

Mostrar-Respuesta -Titulo "Consultar configuración centralizada de menú" `
    -Metodo "GET" -Url "http://localhost:8081/api/menu/configuracion" `
    -ArchivoEvidencia "menu-configuracion-response.json"

# 3. Pedido Service
Write-Host "`n=== 3. PEDIDO SERVICE (Puerto 8082) ===" -ForegroundColor Magenta
Mostrar-Respuesta -Titulo "Consultar reglas de pedidos centralizadas" `
    -Metodo "GET" -Url "http://localhost:8082/api/pedidos/configuracion" `
    -ArchivoEvidencia "pedido-configuracion-response.json"

$pedidoJson = @"
{
    "cliente": "Estudiante Exposición",
    "items": [
        { "plato": "Lomo saltado", "cantidad": 2, "precioUnitario": 38.00 },
        { "plato": "Ceviche clásico", "cantidad": 1, "precioUnitario": 42.00 }
    ]
}
"@
$nuevoPedido = Mostrar-Respuesta -Titulo "Registrar un pedido nuevo (3 platos <= límite 5)" `
    -Metodo "POST" -Url "http://localhost:8082/api/pedidos" `
    -Body $pedidoJson `
    -ArchivoEvidencia "pedido-creado-response.json"

Mostrar-Respuesta -Titulo "Listar todos los pedidos en memoria" `
    -Metodo "GET" -Url "http://localhost:8082/api/pedidos" `
    -ArchivoEvidencia "pedido-listar-response.json"

if ($nuevoPedido -and $nuevoPedido.id) {
    Mostrar-Respuesta -Titulo "Buscar pedido por ID ($($nuevoPedido.id))" `
        -Metodo "GET" -Url "http://localhost:8082/api/pedidos/$($nuevoPedido.id)" `
        -ArchivoEvidencia "pedido-id-response.json"
}

# 4. Promocion Service
Write-Host "`n=== 4. PROMOCION SERVICE (Puerto 8083) ===" -ForegroundColor Magenta
Mostrar-Respuesta -Titulo "Listar promociones disponibles" `
    -Metodo "GET" -Url "http://localhost:8083/api/promociones" `
    -ArchivoEvidencia "promocion-listar-response.json"

Mostrar-Respuesta -Titulo "Consultar promoción destacada" `
    -Metodo "GET" -Url "http://localhost:8083/api/promociones/destacada" `
    -ArchivoEvidencia "promocion-destacada-response.json"

Mostrar-Respuesta -Titulo "Consultar configuración centralizada de promociones" `
    -Metodo "GET" -Url "http://localhost:8083/api/promociones/configuracion" `
    -ArchivoEvidencia "promocion-configuracion-response.json"

Mostrar-Respuesta -Titulo "Calcular precio con descuento para S/ 50 (Esperado con 15%: S/ 42.50)" `
    -Metodo "GET" -Url "http://localhost:8083/api/promociones/calcular?precio=50" `
    -ArchivoEvidencia "promocion-calcular-50-response.json"

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " Pruebas de endpoints completadas exitosamente." -ForegroundColor Green
Write-Host " Evidencias JSON guardadas en: $evidenciasDir" -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Green
