# ==============================================================================
# Sazón Express - Script de Verificación de Entorno
# ==============================================================================
# Propósito: Comprobar requisitos previos antes de la ejecución:
# Java 17+, Maven/mvnw, Git, estado del config-repo y puertos libres (8888, 8081, 8082, 8083).
# ==============================================================================

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [Sazón Express] Verificación de Entorno de Ejecución   " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

$root = Resolve-Path "$PSScriptRoot\.."
$errores = 0

# 1. Comprobar Java
Write-Host "[1/5] Verificando JDK..." -NoNewline
try {
    $javaVersionOutput = java -version 2>&1 | Out-String
    if ($javaVersionOutput -match 'version "(\d+)') {
        $majorVersion = [int]$matches[1]
        if ($majorVersion -ge 17) {
            Write-Host " OK (Java $majorVersion detectado)" -ForegroundColor Green
        } else {
            Write-Host " ADVERTENCIA: Se requiere Java 17 o superior. Versión detectada: $majorVersion" -ForegroundColor Yellow
            $errores++
        }
    } else {
        Write-Host " OK" -ForegroundColor Green
    }
} catch {
    Write-Host " ERROR: Java no está en el PATH." -ForegroundColor Red
    $errores++
}

# 2. Comprobar Maven
Write-Host "[2/5] Verificando Maven..." -NoNewline
try {
    $mvnVer = mvn -v 2>&1 | Select-Object -First 1
    Write-Host " OK ($mvnVer)" -ForegroundColor Green
} catch {
    if (Test-Path "$root\mvnw.cmd") {
        Write-Host " OK (Maven Wrapper detectado)" -ForegroundColor Green
    } else {
        Write-Host " ERROR: Maven no encontrado en el sistema ni mvnw local." -ForegroundColor Red
        $errores++
    }
}

# 3. Comprobar Git
Write-Host "[3/5] Verificando Git..." -NoNewline
try {
    $gitVer = git --version 2>&1
    Write-Host " OK ($gitVer)" -ForegroundColor Green
} catch {
    Write-Host " ERROR: Git no está disponible en el PATH." -ForegroundColor Red
    $errores++
}

# 4. Comprobar Repositorio Git de Configuraciones
Write-Host "[4/5] Verificando repositorio Git de configuraciones (config-repo)..." -NoNewline
$configRepoPath = "$root\config-repo"
$gitDir = "$configRepoPath\.git"

if (-not (Test-Path $gitDir)) {
    Write-Host " ADVERTENCIA: No se detectó config-repo local. Clonando automáticamente desde GitHub..." -ForegroundColor Yellow
    try {
        git clone https://github.com/Jeanfranco06/sazon-express-config.git "$configRepoPath" | Out-Null
    } catch {}
}

if (Test-Path $gitDir) {
    try {
        Push-Location $configRepoPath
        $commitCount = git rev-list --count HEAD 2>&1
        $currentBranch = git rev-parse --abbrev-ref HEAD 2>&1
        Pop-Location
        Write-Host " OK (Rama: $currentBranch, Commits: $commitCount)" -ForegroundColor Green
    } catch {
        Pop-Location
        Write-Host " ERROR: Falló inspección de git en config-repo" -ForegroundColor Red
        $errores++
    }
} else {
    Write-Host " ERROR: No existe .git en $configRepoPath" -ForegroundColor Red
    $errores++
}

# 5. Comprobar Disponibilidad de Puertos
Write-Host "[5/5] Verificando disponibilidad de puertos requeridos..."
$puertos = @(
    @{ Puerto = 8888; Servicio = "Config Server" },
    @{ Puerto = 8081; Servicio = "Menu Service" },
    @{ Puerto = 8082; Servicio = "Pedido Service" },
    @{ Puerto = 8083; Servicio = "Promocion Service" }
)

foreach ($p in $puertos) {
    $puerto = $p.Puerto
    $nom = $p.Servicio
    $ocupado = Get-NetTCPConnection -LocalPort $puerto -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($ocupado) {
        $pidOcupado = $ocupado[0].OwningProcess
        Write-Host "  -> Puerto $puerto ($nom): OCUPADO por PID $pidOcupado (Ejecute detener-servicios.ps1 si es necesario)" -ForegroundColor Yellow
    } else {
        Write-Host "  -> Puerto $puerto ($nom): DISPONIBLE" -ForegroundColor Green
    }
}

Write-Host "`n========================================================" -ForegroundColor Cyan
if ($errores -eq 0) {
    Write-Host " Resultado: Entorno LISTO para ejecutar Sazón Express." -ForegroundColor Green
} else {
    Write-Host " Resultado: Se detectaron $errores observaciones en el entorno." -ForegroundColor Yellow
}
Write-Host "========================================================`n" -ForegroundColor Cyan
