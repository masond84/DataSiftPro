Sub AutoMapHeaders()
    Dim accounts_headers As Object
    Dim prospects_headers As Object
    Dim mapping As Object
    Dim ws As Worksheet
    Dim dataRange As Range
    Dim headers As Variant
    Dim header As Variant
    Dim i As Long
    
    ' Create dictionary for header mappings
    Set accounts_headers = CreateObject("Scripting.Dictionary")
    accounts_headers.Add "Company Name", "Name"
    accounts_headers.Add "Informal Name", "Natural Name"
    accounts_headers.Add "Founding Year", "Founded At"
    accounts_headers.Add "City", "City"
    accounts_headers.Add "State", "State"
    accounts_headers.Add "Postal Code", "Postal Code"
    accounts_headers.Add "Country", "Locality"
    accounts_headers.Add "Phone Number", "Phone Number"
    accounts_headers.Add "Website", "Website"
    accounts_headers.Add "Description", "Description"
    accounts_headers.Add "Specialties", "Custom Field 1"
    accounts_headers.Add "LinkedIn Account", "LinkedIn URL"
    accounts_headers.Add "Employee Count", "Employees"
    accounts_headers.Add "Employee Range", "Employee Range"
    accounts_headers.Add "Products and Services", "Products and Services"
    accounts_headers.Add "End Markets", "End Markets"
    accounts_headers.Add "3 Months Growth Rate %", "3 Months Growth Rate %"
    accounts_headers.Add "6 Months Growth Rate %", "6 Months Growth Rate %"
    accounts_headers.Add "9 Months Growth Rate %", "9 Months Growth Rate %"
    accounts_headers.Add "12 Months Growth Rate %", "12 Months Growth Rate %"
    accounts_headers.Add "Growth Intent", "Growth Intent"
    accounts_headers.Add "Job Count", "Job Count"
    accounts_headers.Add "Ownership", "Ownership"
    accounts_headers.Add "Total Raised", "Total Raised"
    accounts_headers.Add "Latest Raised", "Latest Raised"
    accounts_headers.Add "Date of Most recent Investment", "Date of Most recent Investment"
    accounts_headers.Add "Investors", "Investors"
    accounts_headers.Add "Parent Company", "Parent Company"
    accounts_headers.Add "Executive Title", "Prospect Titles"
    accounts_headers.Add "Executive First Name", "Executive First Name"
    accounts_headers.Add "Executive Last Name", "Executive Last Name"
    accounts_headers.Add "Executive Email", "Executive Email"
    accounts_headers.Add "Executive LinkedIn", "Executive LinkedIn"
    accounts_headers.Add "Last Financial Year", "Last Financial Year"
    accounts_headers.Add "Verified Revenue", "Verified Revenue"
    accounts_headers.Add "Latest Estimated Revenue ($)", "Latest Estimated Revenue ($)"
    accounts_headers.Add "Financial Growth %", "Financial Growth %"
    accounts_headers.Add "Financial Growth Period (yr)", "Financial Growth Period (yr)"
    accounts_headers.Add "Sources Count", "Number of Prospects"
    accounts_headers.Add "CRM Id", "Id"
    accounts_headers.Add "My Tags", "Tags"
    accounts_headers.Add "Firm Tags", "Firm Tags"
    accounts_headers.Add "Industries", "Industry"
    ' Add other key-value pairs for the "Accounts" header mapping
    
    Set prospects_headers = CreateObject("Scripting.Dictionary")
    prospects_headers.Add "Company Name", "Company"
    prospects_headers.Add "Informal Name", "Company Natural"
    prospects_headers.Add "Founding Year", "Company Founded At"
    prospects_headers.Add "City", "City"
    prospects_headers.Add "State", "State"
    prospects_headers.Add "Postal Code", "Zip"
    prospects_headers.Add "Country", "Country"
    prospects_headers.Add "Phone Number", "Mobile Phone"
    prospects_headers.Add "Website", "Website"
    prospects_headers.Add "Description", "Custom 6"
    prospects_headers.Add "Specialties", "Specialties"
    prospects_headers.Add "LinkedIn Account", "Company LinkedIn"
    prospects_headers.Add "Employee Count", "Custom 2"
    prospects_headers.Add "Employee Range", "Company LinkedIn Employees"
    prospects_headers.Add "Products and Services", "Products and Services"
    prospects_headers.Add "End Markets", "End Markets"
    prospects_headers.Add  "3 Months Growth Rate %", "3 Months Growth Rate %"
    prospects_headers.Add "6 Months Growth Rate %", "6 Months Growth Rate %"
    prospects_headers.Add "9 Months Growth Rate %", "9 Months Growth Rate %"
    prospects_headers.Add "12 Months Growth Rate %", "12 Months Growth Rate %"
    prospects_headers.Add "Growth Intent", "Growth Intent"
    prospects_headers.Add "Job Count", "Job Count"
    prospects_headers.Add "Ownership", "Ownership"
    prospects_headers.Add "Total Raised", "Total Raised"
    prospects_headers.Add "Latest Raised", "Latest Raised"
    prospects_headers.Add "Date of Most recent Investment", "Date of Most recent Investment"
    prospects_headers.Add "Investors", "Investors"
    prospects_headers.Add "Parent Company", "Parent Company"
    prospects_headers.Add "Executive Title", "Title"
    prospects_headers.Add "Executive First Name", "First Name"
    prospects_headers.Add "Executive Last Name", "Last Name"
    prospects_headers.Add "Executive Email", "Email"
    prospects_headers.Add "Executive LinkedIn", "LinkedIn"
    prospects_headers.Add "Last Financial Year", "Last Financial Year"
    prospects_headers.Add "Verified Revenue", "Verified Revenue"
    prospects_headers.Add "Latest Estimated Revenue ($)", "Latest Estimated Revenue ($)"
    prospects_headers.Add "Financial Growth %", "Financial Growth %"
    prospects_headers.Add "Financial Growth Period (yr)", "Financial Growth Period (yr)"
    prospects_headers.Add "Sources Count", "Number of Prospects"
    prospects_headers.Add "CRM Id", "CRM Id"
    prospects_headers.Add "My Tags", "My Tags"
    prospects_headers.Add "Firm Tags", "Tags"
    prospects_headers.Add "Industries", "Custom 7"
    
    ' Prompt user to choose between accounts_headers and prospects_headers
    choice = UCase(InputBox("Choose header mapping: A) Accounts or B) Prospects", "Choose Mapping"))

    If choice = "A" Then
        Set mapping = accounts_headers
    ElseIf choice = "B" Then
        Set mapping = prospects_headers
    Else
        MsgBox "Invalid choice. Please choose A or B.", vbExclamation
        Exit Sub
    End If
    
    ' Set the current worksheet to the one where the data is located
    Set ws = ThisWorkbook.ActiveSheet
    
    ' Get the range of data
    Set dataRange = ws.UsedRange
    
    ' Get the header row
    headers = dataRange.Rows(1).Value
    
    ' Map the headers
    For i = LBound(headers, 2) To UBound(headers, 2)
        header = headers(1, i)
        If mapping.Exists(header) Then
            headers(1, i) = mapping(header)
        End If
    Next i
    
    ' Update the header row
    dataRange.Rows(1).Value = headers
    
    MsgBox "Header Mapping Completed"
End Sub

