Attribute VB_Name = "Module2"
Sub CleanEmails()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim email As String
    Dim cleanedEmail As String
    Dim emailCol As Long

    On Error Resume Next ' Turn on error handling to suppress error if header not found

    Set ws = ActiveSheet ' Use the currently active sheet

    ' Find the column number for "Email" header
    emailCol = Application.WorksheetFunction.Match("Email", ws.Rows(1), 0)

    On Error GoTo 0 ' Turn off error handling

    If emailCol = 0 Then
        MsgBox "Header 'Email' not found. Please ensure the header exists.", vbExclamation
        Exit Sub
    End If

    ' Find the last used row in the "Email" column
    lastRow = ws.Cells(ws.Rows.Count, emailCol).End(xlUp).Row

    ' Loop through each cell in the "Email" column starting from the row after the header
    For i = 2 To lastRow ' Assuming the header is in row 1, start from row 2
        email = Trim(ws.Cells(i, emailCol).Value) ' Remove leading/trailing spaces

        ' Find the position of the "@" symbol in the email address
        Dim atPosition As Integer
        atPosition = InStr(email, "@")

        ' If the "@" symbol is found, keep only the part after it and add an asterisk before
        If atPosition > 0 Then
            cleanedEmail = "*" & Mid(email, atPosition)
        Else
            cleanedEmail = email ' Keep the original value if no "@" symbol found
        End If

        ' Update the cell with the cleaned email
        ws.Cells(i, emailCol).Value = cleanedEmail
    Next i
End Sub
