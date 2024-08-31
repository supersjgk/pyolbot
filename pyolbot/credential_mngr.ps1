Import-Module CredentialManager

$targetName = "OverleafBot"
$username = Read-Host "Enter your Overleaf email (e.g., your_email@example.com)"
$password = Read-Host "Enter your Overleaf password" -AsSecureString

$plainPassword = [System.Net.NetworkCredential]::new("", $password).Password

# Add the credential to Windows Credential Manager
New-StoredCredential -Target $targetName -UserName $username -Password $plainPassword -Persist LocalMachine

# Confirm the credential was added
Write-Host "Generic credentials added to Windows Credential Manager..."
