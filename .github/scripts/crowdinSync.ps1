#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

# Git configuration for automated commits
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

$rawAddonId = $env:ADDON_ID
if ([string]::IsNullOrWhiteSpace($rawAddonId)) {
    Write-Error "Failed to get addon ID."
    exit 1
}
$addonId = $rawAddonId.Trim()

# --- STEP 1: PREPARATION AND SOURCE UPDATE ---

$xliffFile = "./$addonId.xliff"
$mdFile = "./readme.md"

if (Test-Path $mdFile) {
    if (Test-Path $xliffFile) {
        $tempXliff = [System.IO.Path]::GetTempFileName()
        try {
            Copy-Item "$addonId.xliff" $tempXliff -Force
            Write-Host "DEBUG: Updating XLIFF source based on readme.md..."
            ./l10nUtil.exe md2xliff $mdFile $xliffFile -o $tempXliff
        }
        finally {
            if (Test-Path $tempXliff) {
                Remove-Item $tempXliff -Force
            }
        }
    }
    else {
        Write-Host "DEBUG: XLIFF template not found. Creating new one from readme.md..."
        ./l10nUtil.exe md2xliff $mdFile $xliffFile
    }
}

# Update POT file (addon interface)
uv run scons pot
$potFile = "$addonId.pot"

# --- STEP 2: UPLOAD SOURCES TO CROWDIN ---

if (Test-Path $potFile) {
    Write-Host "DEBUG: Uploading updated POT source to Crowdin..."
    ./l10nUtil.exe uploadSourceFile "$potFile" -c $env:L10N_UTIL_CONFIG
}

if (Test-Path $xliffFile) {
    Write-Host "DEBUG: Uploading updated XLIFF source to Crowdin..."
    ./l10nUtil.exe uploadSourceFile "$xliffFile" -c $env:L10N_UTIL_CONFIG

    git add "$xliffFile"
    git diff --staged --quiet

    if ($LASTEXITCODE -ne 0) {
        git commit -m "Update $xliffFile for $addonId"
    }
}

# --- STEP 3: EXPORT AND PROCESS TRANSLATIONS ---

Write-Host "DEBUG: Exporting translations from Crowdin..."
./l10nUtil.exe exportTranslations -o _addonL10n -c $env:L10N_UTIL_CONFIG

# Ensure base directories exist
New-Item -ItemType Directory -Force -Path addon/locale | Out-Null
New-Item -ItemType Directory -Force -Path addon/doc | Out-Null

# Load language mappings for Crowdin API calls
$languageMappings = Get-Content -Raw ".github/scripts/languageMappings.json" | ConvertFrom-Json

foreach ($dir in Get-ChildItem -Path "_addonL10n/$addonId" -Directory) {

    $langCode = $dir.Name

    if ($langCode -eq "en") {
        continue
    }

    # --- Identify codes

    $crowdinLang = $null

    if ($languageMappings.PSObject.Properties.Name -contains $langCode) {
        $crowdinLang = $languageMappings."$langCode"
    }

    if (-not $crowdinLang) {
        $crowdinLang = $langCode.Replace('_', '-')
    }

    Write-Host "--- Processing Language: $langCode (Crowdin: $crowdinLang) ---" -ForegroundColor Cyan

    # Paths

    $remoteXliff = Join-Path $dir.FullName "$addonId.xliff"
    $remotePo = Join-Path $dir.FullName "$addonId.po"

    $localMdDir = "addon/doc/$langCode"
    $localMd = "$localMdDir/readme.md"

    $localPoPath = "addon/locale/$langCode/LC_MESSAGES/nvda.po"

    # --- 3.1 PO FILE PROCESSING ---
    $poImported = $false
    $scorePo = 0.0
    $threshold = $env:MIN_PERCENTAGE_TRANSLATED

    if (Test-Path $remotePo) {

        Write-Host "DEBUG: Evaluating Remote PO score..."

        $res = uv run python .github/scripts/checkTranslation.py "$addonId.po" $crowdinLang

        $scorePo = [double](
            ($res | Select-String "poScore=").ToString().Split("=")[1]
        )

        Write-Host "DEBUG: PO Score -> $scorePo"

        if ($scorePo -ge $threshold) {

            Write-Host "SUCCESS: Remote PO is above threshold. Importing to $localPoPath"

            New-Item -ItemType Directory -Force -Path (Split-Path $localPoPath) | Out-Null

            Move-Item $remotePo $localPoPath -Force

            $poImported = $true
        }
        else {

            Write-Host "WARNING: Remote PO score is below threshold ($threshold)."
        }
    }

    if (-not $poImported -and (Test-Path $localPoPath)) {

        Write-Host "ACTION: Uploading local legacy PO to Crowdin ($crowdinLang) as fallback."

        ./l10nUtil.exe uploadTranslationFile $crowdinLang "$addonId.po" $localPoPath -c $env:L10N_UTIL_CONFIG
    }

    # --- 3.2 DOCUMENTATION PROCESSING (XLIFF ONLY) ---

    $scoreXliff = 0.0

    if (Test-Path $remoteXliff) {

        Write-Host "DEBUG: Evaluating Remote XLIFF score..."

        $res = uv run python .github/scripts/checkTranslation.py "$addonId.xliff" $crowdinLang

        $scoreXliff = [double](
            ($res | Select-String "xliffScore=").ToString().Split("=")[1]
        )
    }
    else {
        Write-Host "DEBUG: No remote XLIFF file found for this language."
    }

    Write-Host "DEBUG: XLIFF Score -> $scoreXliff"

    $threshold = $env:MIN_PERCENTAGE_TRANSLATED
    $docImported = $false

    if ($scoreXliff -ge $threshold) {

        if (!(Test-Path $localMdDir)) {
            New-Item -ItemType Directory -Force -Path $localMdDir | Out-Null
        }

        Write-Host "SUCCESS: Importing documentation from XLIFF ($langCode)..."

        ./l10nUtil.exe xliff2md $remoteXliff $localMd

        $docImported = $true
    }
    else {

        Write-Host "WARNING: Remote XLIFF score is below threshold ($threshold)."
    }

    # No Markdown fallback upload anymore.
    # XLIFF is now the single translation source in Crowdin.
}

# --- STEP 4: COMMIT UPDATED TRANSLATIONS ---

git add addon/locale addon/doc

git diff --staged --quiet

if ($LASTEXITCODE -ne 0) {

    git commit -m "Update translations for $addonId from Crowdin (Automatic Sync)"

    Write-Host "SUCCESS: Translations committed."
}
else {

    Write-Host "DEBUG: No changes in translations to commit."
}

# Push all generated commits after successful Crowdin synchronization

$pushOutput = git push 2>&1

$repository = $env:GITHUB_REPOSITORY

Write-Host $pushOutput

if ($LASTEXITCODE -ne 0) {

    Write-Host "ERROR: Failed to push commits to $repository."
}
elseif ($pushOutput -match "Everything up-to-date") {

    Write-Host "INFO: No new commits needed to be pushed."
}
else {

    Write-Host "SUCCESS: New commits successfully pushed to $repository."
}
