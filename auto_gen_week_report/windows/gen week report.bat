@echo off
goto :PS_START

:PS_START
powershell -Command "cd C:\Users\nidan\weekreport\;py .\gen_email_draft_of_week_report.python"
exit