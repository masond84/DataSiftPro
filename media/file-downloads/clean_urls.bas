Attribute VB_Name = "Module1"
Sub CleanWebsiteURLs()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim url As String
    Dim cleanedURL As String
    Dim websiteCol As Long
    
    On Error Resume Next ' Turn on error handling to suppress error if header not found
    
    Set ws = ActiveSheet ' Use the currently active sheet
    
    ' Find the column number for "Website" header
    websiteCol = Application.WorksheetFunction.Match("Website", ws.Rows(1), 0)
    
    On Error GoTo 0 ' Turn off error handling
    
    If websiteCol = 0 Then
        MsgBox "Header 'Website' not found. Please ensure the header exists.", vbExclamation
        Exit Sub
    End If
    
    ' Find the last used row in the "Website" column
    lastRow = ws.Cells(ws.Rows.Count, websiteCol).End(xlUp).Row
    
    ' Loop through each cell in the "Website" column starting from the row after the header
    For i = 2 To lastRow ' Assuming the header is in row 1, start from row 2
        url = Trim(ws.Cells(i, websiteCol).Value) ' Remove leading/trailing spaces
        cleanedURL = url
        
        ' Remove "https://", "http://", and "www." from the URL
        cleanedURL = Replace(cleanedURL, "https://", "")
        cleanedURL = Replace(cleanedURL, "http://", "")
        cleanedURL = Replace(cleanedURL, "www.", "")
        
        ' Remove trailing "/" if it exists
        If Right(cleanedURL, 1) = "/" Then
            cleanedURL = Left(cleanedURL, Len(cleanedURL) - 1)
        End If
        
        ' Update the cell with the cleaned URL
        ws.Cells(i, websiteCol).Value = cleanedURL
    Next i
End Sub

