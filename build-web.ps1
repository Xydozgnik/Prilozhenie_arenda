${env:ProgramFiles(x86)} = 'C:\Program Files (x86)'
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
Set-Location D:\Projects\porog_flutter
flutter build web --base-href '/porog-app/'
exit $LASTEXITCODE
