Option Explicit
Const wdFormatWebArchive = 9

Dim objWord, objDoc, objFSO
Dim srcFile, outFile

If WScript.Arguments.Count < 2 Then
    WScript.Echo "用法: cscript Word2Mht.vbs 源.doc/docx 输出.mht"
    WScript.Quit 1
End If

srcFile = WScript.Arguments(0)
outFile = WScript.Arguments(1)

Set objFSO = CreateObject("Scripting.FileSystemObject")
If Not objFSO.FileExists(srcFile) Then
    WScript.Echo "错误：源文件不存在 " & srcFile
    WScript.Quit 2
End If

Set objWord = CreateObject("Word.Application")
objWord.Visible = False
objWord.DisplayAlerts = 0

Set objDoc = objWord.Documents.Open(srcFile)
objDoc.SaveAs outFile, wdFormatWebArchive
objDoc.Close
objWord.Quit

Set objDoc = Nothing
Set objWord = Nothing
Set objFSO = Nothing
WScript.Echo "转换成功：" & outFile
