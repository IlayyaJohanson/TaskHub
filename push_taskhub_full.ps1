param (
    [string]$RepoName = "TaskHub",
    [string]$Private = "false" # "true" или "false"
)

Write-Host "=== 🚀 Авто-деплой TaskHub на GitHub ===" -ForegroundColor Cyan

# --- Проверка Git ---
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git не установлен. Скачай: https://git-scm.com/" -ForegroundColor Red
    exit
}

# --- Проверка GitHub CLI ---
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "❌ GitHub CLI (gh) не установлен. Скачай: https://cli.github.com/" -ForegroundColor Red
    exit
}

# --- Проверка SSH-ключа ---
$sshPath = "$env:USERPROFILE\.ssh\id_ed25519"
if (-not (Test-Path "$sshPath")) {
    Write-Host "🔑 SSH-ключ не найден. Генерирую..."
    ssh-keygen -t ed25519 -C "$env:USERNAME@github" -f $sshPath -N ""
    Write-Host "✅ Ключ создан: $sshPath"
}

# --- Копируем публичный ключ в буфер ---
Get-Content "$sshPath.pub" | Set-Clipboard
Write-Host "📋 Публичный ключ скопирован в буфер. Добавь его на GitHub:"
Write-Host "   https://github.com/settings/keys"
Write-Host "Нажми Enter, когда добавишь ключ..."
Pause

# --- Авторизация GH ---
$ghAuth = gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔐 Авторизация GH..."
    gh auth login
}

# --- Проверка наличия PROJECT_CONTEXT.md ---
if (-not (Test-Path "PROJECT_CONTEXT.md")) {
    Write-Host "⚠️ Файл PROJECT_CONTEXT.md не найден! Создаю пустой шаблон..." -ForegroundColor Yellow
    @"
# PROJECT CONTEXT

(здесь будет описание проекта)
"@ | Out-File -Encoding UTF8 PROJECT_CONTEXT.md
} else {
    Write-Host "📄 Найден PROJECT_CONTEXT.md — он будет добавлен в репозиторий" -ForegroundColor Green
}

# --- Git init ---
if (-not (Test-Path ".git")) {
    git init
    git checkout -b main
}

# --- Добавление всех файлов, включая PROJECT_CONTEXT.md ---
git add .
git commit -m "chore: initial commit with project structure and context" --allow-empty

# --- Создание репо на GitHub ---
if ($Private -eq "true") {
    gh repo create $RepoName --private --source=. --remote=origin --push
} else {
    gh repo create $RepoName --public --source=. --remote=origin --push
}

Write-Host "✅ Репозиторий $RepoName создан и запушен на GitHub с PROJECT_CONTEXT.md!" -ForegroundColor Green
