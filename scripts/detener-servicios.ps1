# ==============================================================================
# Sazón Express - Detener Todos los Servicios del Sistema
# ==============================================================================

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [Sazón Express] Deteniendo Servicios en Ejecución      " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

$puertos = @(
    @{ Puerto = 8888; Nombre = "Config Server" },
    @{ Puerto = 8081; Nombre = "Menu Service" },
    @{ Puerto = 8082; Nombre = "Pedido Service" },
    @{ Puerto = 8083; Nombre = "Promocion Service" }
)

$detenidos = 0

foreach ($p in $puertos) {
    $puerto = $p.Puerto
    $nom = $p.Nombre

    $conns = Get-NetTCPConnection -LocalPort $puerto -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($conns) {
        $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($pidProc in $pids) {
            try {
                $proc = Get-Process -Id $pidProc -ErrorAction SilentlyContinue
                if ($proc) {
                    Write-Host "Deteniendo $nom (PID: $pidProc, Proceso: $($proc.ProcessName))..." -ForegroundColor Yellow
                    Stop-Process -Id $pidProc -Force -ErrorAction SilentlyContinue
                    $detenidos++
                }
            } catch {
                Write-Host "No se pudo detener PID $pidProc : $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "Puerto $puerto ($nom): No hay procesos activos." -ForegroundColor Gray
    }
}

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " Proceso finalizado. Total de procesos detenidos: $detenidos." -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Cyan
