# ==============================================================================
# Sazón Express - Iniciar los Tres Microservicios
# ==============================================================================
# Inicia:
# - menu-service (Puerto 8081)
# - pedido-service (Puerto 8082)
# - promocion-service (Puerto 8083)
# ==============================================================================

$root = Resolve-Path "$PSScriptRoot\.."
$evidenciasDir = "$root\docs\evidencias"
New-Item -ItemType Directory -Force -Path $evidenciasDir | Out-Null

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [Sazón Express] Iniciando Microservicios de Negocio    " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# 1. Comprobar que Config Server esté activo
Write-Host "Verificando disponibilidad de Config Server en :8888..." -NoNewline
try {
    $csResp = Invoke-RestMethod -Uri "http://localhost:8888/menu-service/default" -Method Get -TimeoutSec 3 -ErrorAction Stop
    Write-Host " ONLINE" -ForegroundColor Green
} catch {
    Write-Host " OFFLINE" -ForegroundColor Yellow
    Write-Host "Iniciando Config Server automáticamente..." -ForegroundColor Cyan
    & "$PSScriptRoot\iniciar-config-server.ps1"
}

$servicios = @(
    @{ Nombre = "menu-service";      Puerto = 8081; Jar = "$root\menu-service\target\menu-service-0.0.1-SNAPSHOT.jar";           Url = "http://localhost:8081/actuator/health" },
    @{ Nombre = "pedido-service";    Puerto = 8082; Jar = "$root\pedido-service\target\pedido-service-0.0.1-SNAPSHOT.jar";       Url = "http://localhost:8082/actuator/health" },
    @{ Nombre = "promocion-service"; Puerto = 8083; Jar = "$root\promocion-service\target\promocion-service-0.0.1-SNAPSHOT.jar"; Url = "http://localhost:8083/actuator/health" }
)

foreach ($s in $servicios) {
    $nom = $s.Nombre
    $puerto = $s.Puerto
    $jar = $s.Jar
    $url = $s.Url

    Write-Host "`n--- Iniciando $nom en puerto $puerto ---" -ForegroundColor Cyan

    # Verificar si ya está corriendo
    $ocupado = Get-NetTCPConnection -LocalPort $puerto -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($ocupado) {
        Write-Host "$nom ya se encuentra en ejecución en puerto $puerto (PID: $($ocupado[0].OwningProcess))." -ForegroundColor Yellow
        continue
    }

    if (-not (Test-Path $jar)) {
        Write-Host "Compilando $nom..." -ForegroundColor Yellow
        Push-Location "$root\$nom"
        mvn clean package -DskipTests
        Pop-Location
    }

    $logFile = "$evidenciasDir\$nom.log"
    $errFile = "$evidenciasDir\$nom-error.log"

    $proc = Start-Process -FilePath "java" `
        -ArgumentList @("-jar", "`"$jar`"") `
        -RedirectStandardOutput $logFile `
        -RedirectStandardError $errFile `
        -WindowStyle Hidden `
        -PassThru

    Write-Host "Lanzado proceso PID: $($proc.Id). Esperando inicialización..." -NoNewline
    $intentos = 0
    $maxIntentos = 30
    $ok = $false

    while ($intentos -lt $maxIntentos) {
        Start-Sleep -Seconds 1
        $intentos++
        try {
            $resp = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 2 -ErrorAction Stop
            if ($resp -and ($resp.status -eq "UP" -or $resp.status -eq "OK")) {
                $ok = $true
                break
            }
        } catch {
            Write-Host "." -NoNewline
        }
    }

    Write-Host ""
    if ($ok) {
        Write-Host "$nom activo y saludable en puerto $puerto" -ForegroundColor Green
    } else {
        Write-Host "Advertencia: $nom demoró en responder. Verifique log: $logFile" -ForegroundColor Yellow
    }
}

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " Todos los microservicios han sido procesados." -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Cyan
