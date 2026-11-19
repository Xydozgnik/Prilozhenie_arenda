${env:ProgramFiles(x86)} = 'C:\Program Files (x86)'
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
Set-Location D:\Projects\porog_flutter
flutter analyze 2>&1 | Select-Object -Last 3
flutter test 2>&1 | Select-Object -Last 3
