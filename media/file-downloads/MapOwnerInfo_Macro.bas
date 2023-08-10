Sub AddOwnerInfo()
    Dim ws As Worksheet
    ' Set the current worksheet to the one where the data is located
    Set ws = ThisWorkbook.ActiveSheet
    
    ' Define owner data
    Dim owner_name As Variant
    Dim owner_id As Variant
    Dim owner_email As Variant
    
    owner_name = Array("Joey Talocka", "Jesse Crawford-Lang", "Michael Johnson")
    owner_id = Array("JTalocka", "jessecrawfordlang", "MichaelJohnson2")
    owner_email = Array("talocka@hydeparkcapital.com", "crawfordlang@hydeparkcapital.com", "johnson@hydeparkcapital.com")
    
    ' Add necessary columns at the beginning of the worksheet
    ws.Columns("A:C").Insert Shift:=xlToRight
    ws.Range("A1") = "Owner Name"
    ws.Range("B1") = "Owner ID"
    ws.Range("C1") = "Owner Email"
    
    ' Add owner data to the worksheet
    Dim totalRows As Long
    totalRows = ws.Cells(ws.Rows.Count, "D").End(xlUp).Row ' Assuming data starts from column D
    
    Dim ownerIndex As Long
    ownerIndex = 0
    
    Dim i As Long
    For i = 2 To totalRows
        ws.Cells(i, "A").Value = owner_name(ownerIndex)
        ws.Cells(i, "B").Value = owner_id(ownerIndex)
        ws.Cells(i, "C").Value = owner_email(ownerIndex)
        
        ownerIndex = (ownerIndex + 1) Mod 3
    Next i

    MsgBox "Owner Mapping Completed"
End Sub
 
