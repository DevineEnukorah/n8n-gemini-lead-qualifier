param(
    [string]$Path = ".\workflow.json"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Path)) {
    throw "Workflow file not found: $Path"
}

$backup = "$Path.bak"
Copy-Item $Path $backup -Force

$workflow = Get-Content $Path -Raw | ConvertFrom-Json

$parser = $workflow.nodes | Where-Object { $_.name -eq "Structured Output Parser" }
if (-not $parser) {
    throw "Structured Output Parser node not found."
}

$autoFixProperty = $parser.parameters.PSObject.Properties["autoFix"]
if ($autoFixProperty) {
    $parser.parameters.autoFix = $false
}
else {
    $parser.parameters | Add-Member -NotePropertyName "autoFix" -NotePropertyValue $false
}

$gemini = $workflow.nodes | Where-Object { $_.name -eq "Google Gemini Chat Model" }
if (-not $gemini) {
    throw "Google Gemini Chat Model node not found."
}

$gemini.PSObject.Properties.Remove("credentials")

$workflow.PSObject.Properties.Remove("id")

if ($workflow.meta) {
    $workflow.meta.PSObject.Properties.Remove("instanceId")

    if ($workflow.meta.PSObject.Properties["templateCredsSetupCompleted"]) {
        $workflow.meta.templateCredsSetupCompleted = $false
    }
    else {
        $workflow.meta | Add-Member -NotePropertyName "templateCredsSetupCompleted" -NotePropertyValue $false
    }
}

$workflow |
    ConvertTo-Json -Depth 100 |
    Set-Content $Path -Encoding utf8

Write-Host "Sanitized: $Path" -ForegroundColor Green
Write-Host "Backup:    $backup" -ForegroundColor Yellow
Write-Host "Changes:" -ForegroundColor Cyan
Write-Host " - Structured Output Parser autoFix explicitly set to false"
Write-Host " - Gemini credential reference removed"
Write-Host " - Deployment-specific workflow id and instanceId removed"
