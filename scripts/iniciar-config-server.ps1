# ==============================================================================
# Sazón Express - Iniciar Config Server (Puerto 8888)
# ==============================================================================

param(
    [switch]$NoWait
)

$root = Resolve-Path "$PSScriptRoot\.."
$configServerDir = "$root\config-server"
$configRepoDir = "$root\config-repo"
$jarPath = "$configServerDir\target\config-server-0.0.1-SNAPSHOT.jar"
$evidenciasDir = "$root\docs\evidencias"
New-Item -ItemType Directory -Force -Path $evidenciasDir | Out-Null

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [Sazón Express] Iniciando Spring Cloud Config Server   " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# Comprobar si ya está corriendo en el puerto 8888
$conn = Get-NetTCPConnection -LocalPort 8888 -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
if ($conn) {
    Write-Host "Config Server YA está ejecutándose en el puerto 8888 (PID: $($conn[0].OwningProcess))." -ForegroundColor Yellow
    exit 0
}

# Si no existe el JAR, compilarlo
if (-not (Test-Path $jarPath)) {
    Write-Host "JAR no encontrado. Compilando config-server..." -ForegroundColor Yellow
    Push-Location $configServerDir
    mvn clean package -DskipTests
    Pop-Location
}

# Normalizar ruta Git compatible con Spring Cloud Config / JGit en Windows
if (-not (Test-Path "$configRepoDir\.git")) {
    Write-Host "Repositorio local config-repo no detectado. Clonando desde GitHub..." -ForegroundColor Yellow
    git clone https://github.com/Jeanfranco06/sazon-express-config.git "$configRepoDir"
}
$gitUri = "file:///" + ($configRepoDir -replace '\\', '/')
Write-Host "Repositorio Git objetivo: $gitUri" -ForegroundColor Gray

$logFile = "$evidenciasDir\config-server.log"
$errFile = "$evidenciasDir\config-server-error.log"

$argList = @(
    "-Dspring.cloud.config.server.git.uri=$gitUri",
    "-jar",
    "`"$jarPath`""
)

$proc = Start-Process -FilePath "java" `
    -ArgumentList $argList `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError $errFile `
    -WindowStyle Hidden `
    -PassThru

Write-Host "Proceso Config Server lanzado con PID: $($proc.Id)" -ForegroundColor Green
Write-Host "Logs disponibles en: $logFile" -ForegroundColor Gray

if ($NoWait) {
    exit 0
}

# Esperar a que Config Server responda
Write-Host "Esperando a que Config Server esté listo en http://localhost:8888..." -NoNewline
$intentos = 0
$maxIntentos = 35
$listo = $false

while ($intentos -lt $maxIntentos) {
    Start-Sleep -Seconds 1
    $intentos++
    try {
        $resp = Invoke-RestMethod -Uri "http://localhost:8888/menu-service/default" -Method Get -TimeoutSec 2 -ErrorAction Stop
        if ($resp -and $resp.propertySources) {
            $listo = $true
            break
        }
    } catch {
        Write-Host "." -NoNewline
    }
}

Write-Host ""
if ($listo) {
    Write-Host "`n Config Server está LISTO y respondiendo configuraciones desde Git!" -ForegroundColor Green
    Write-Host " URL de prueba: http://localhost:8888/menu-service/default" -ForegroundColor Cyan
} else {
    Write-Host "`n ADVERTENCIA: Config Server tardó en responder. Revise el archivo de log: $logFile" -ForegroundColor Yellow
}
