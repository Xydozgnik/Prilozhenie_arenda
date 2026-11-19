${env:ProgramFiles(x86)} = 'C:\Program Files (x86)'
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$env:JAVA_HOME = [Environment]::GetEnvironmentVariable('JAVA_HOME','User')
if (-not $env:JAVA_HOME) { $env:JAVA_HOME = 'D:\Android\jbr' }
Set-Location D:\Projects\porog_flutter\android
.\gradlew.bat --stop 2>&1 | Select-Object -Last 1
Set-Location D:\Projects\porog_flutter
flutter clean 2>&1 | Select-Object -Last 1
flutter pub get 2>&1 | Select-Object -Last 1
flutter build apk --debug 2>&1 | Out-File -Encoding utf8 "$env:TEMP\apk.txt"
Get-Content "$env:TEMP\apk.txt" | Select-Object -Last 4
