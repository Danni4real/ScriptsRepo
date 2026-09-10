@echo off
goto :PS_START

:PS_START
powershell -Command "$ip='192.168.227.136'; if(Test-Connection $ip -Count 2 -Quiet){ Write-Host 'shutdown Ubuntu...'; sshpass.exe -p 1 ssh -t -o StrictHostKeyChecking=no dan@$ip 'echo 1 | sudo -S poweroff'; Start-Sleep 1800; } else { Start-Sleep 2; }; Write-Host 'shutdown Windows...'; shutdown /s /t 2"
exit