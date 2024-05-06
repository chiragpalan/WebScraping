Sub ArrangeTextBoxesCircular()
    Dim slide As slide
    Dim shp As Shape
    Dim radius As Double
    Dim angle As Double
    Dim centerX As Double
    Dim centerY As Double
    Dim incrementAngle As Double
    
    ' Set the radius and center of the circle
    radius = 200
    centerX = 400 ' Adjust as needed
    centerY = 300 ' Adjust as needed
    
    ' Set the initial angle and angle increment
    angle = 0
    incrementAngle = 2 * WorksheetFunction.Pi / ActivePresentation.Slides(1).Shapes.Count
    
    For Each slide In ActivePresentation.Slides
        For Each shp In slide.Shapes
            If shp.Type = msoTextBox Then
                ' Calculate the position of the text box
                shp.Left = centerX + radius * Cos(angle)
                shp.Top = centerY + radius * Sin(angle)
                
                ' Increment the angle for the next text box
                angle = angle + incrementAngle
            End If
        Next shp
    Next slide
End Sub

