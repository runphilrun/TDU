Public Class Main
    Private Sub ComboBox1_SelectedIndexChanged(sender As Object, e As EventArgs) Handles ComboBox1.SelectedIndexChanged
        Dim prop As String = ComboBox1.Text
        Select Case prop
            Case "Air"
                doMath.Enabled = True
                LabelmMol.Text = 28.966
                Labelk.Text = 1.4018
            Case "Nitogen (N2)"
                doMath.Enabled = True
                LabelmMol.Text = 28.0134
                Labelk.Text = 1.4013
            Case "Helium"
                doMath.Enabled = True
                LabelmMol.Text = 4.002602
                Labelk.Text = 1.6665
            Case "Argon"
                doMath.Enabled = True
                LabelmMol.Text = 39.948
                Labelk.Text = 1.6696
            Case "Xenon"
                doMath.Enabled = True
                LabelmMol.Text = 131.3
                Labelk.Text = 1.6773
            Case "Ammonia"
                doMath.Enabled = True
                LabelmMol.Text = 17.02
                Labelk.Text = 1.316
            Case "Hydrazine"
                doMath.Enabled = True
                LabelmMol.Text = 32.0452
                Labelk.Text = 1.191
        End Select
    End Sub
    Private Sub doMath_Click(sender As Object, e As EventArgs) Handles doMath.Click

        ' set constants
        Dim g0 = 9.81        ' [m/s^2] Standard gravity
        Dim universalGasConstant = 0.008314    ' [J/K*kmol] Universal gas constant

        ' get inputs
        Dim molarMass, specificHeatRatio, chamberPressure, chamberTemp, halfAngle, throatRadius, exitRadius As Double ' inputs
        molarMass = Convert.ToDouble(LabelmMol.Text)
        specificHeatRatio = Convert.ToDouble(Labelk.Text)
        halfAngle = Convert.ToDouble(UpDownAlpha.Value) * Math.PI / 180 'convert to radians
        throatRadius = Convert.ToDouble(UpDownRt.Value)
        exitRadius = Convert.ToDouble(UpDownRe.Value)
        chamberPressure = Convert.ToDouble(UpDownPc.Value)
        chamberTemp = Convert.ToDouble(UpDownTc.Value)
        If (exitRadius - throatRadius) < 0 Then
            Throw New ApplicationException("Exit radius must be greater than throat radius")
        End If
        Dim Length, throatArea, throatPressure, throatTemp, massFlowRate, exitArea, exitMach, exitPressure, exitTemp, exitVelocity, expansionRatio, thrust, Isp, CF, vc As Double ' outputs

        ''DEBUG VALUES
        'At = 1.0 'm2
        'Ae = 2.005 'm2
        'k = 1.4
        'mMol = 28.02 'kJ/kmol
        'Pc = 1 'bar
        'Tc = 273 'K
        ''END DEBUG VALUES

        Dim specificGasConstant = universalGasConstant / molarMass
        throatArea = (throatRadius / 1000) ^ 2 * Math.PI
        exitArea = (exitRadius / 1000) ^ 2 * Math.PI
        Length = (exitRadius - throatRadius) / Math.Sin(halfAngle)
        expansionRatio = exitArea / throatArea

        Dim critP = (2 / (specificHeatRatio + 1)) ^ (specificHeatRatio / (specificHeatRatio - 1))
        throatPressure = chamberPressure * critP
        throatTemp = chamberTemp * (2 / (specificHeatRatio + 1))
        massFlowRate = (throatPressure / (specificGasConstant * throatTemp)) * Math.Sqrt(specificHeatRatio * specificGasConstant * throatTemp) * throatArea
        Dim aStar = Math.Sqrt(2 * specificHeatRatio * specificGasConstant * throatTemp) 'speed of sound at throat

        exitMach = solveMach(throatArea, exitArea, specificHeatRatio)
        exitVelocity = Math.Sqrt(((2 * specificHeatRatio * specificGasConstant * chamberTemp) / (specificHeatRatio - 1)) * (1 - (1 / (1 + ((specificHeatRatio - 1) / 2) * exitMach ^ 2))))
        Dim tempRatio = 1 + ((specificHeatRatio - 1) / 2) * exitMach ^ 2
        Dim presRatio = tempRatio ^ ((specificHeatRatio - 1) / specificHeatRatio)
        exitPressure = chamberPressure / presRatio
        exitTemp = chamberTemp / tempRatio

        vc = throatPressure * throatArea / massFlowRate
        CF = (exitVelocity / vc) + (exitArea / throatArea) * (exitPressure / chamberPressure)

        thrust = massFlowRate * exitVelocity + exitPressure * exitArea
        Isp = thrust / (g0 * massFlowRate)

        ' set outputs
        LabelL.Text = Length
        Labele.Text = expansionRatio
        LabelPt.Text = throatPressure
        LabelTt.Text = throatTemp
        Labelmdot.Text = massFlowRate
        LabelPe.Text = exitPressure
        LabelTe.Text = exitTemp
        LabelM.Text = exitMach
        Labelve.Text = exitVelocity
        LabelF.Text = thrust
        LabelIsp.Text = Isp

        'math checkouts
        ' From page 635, NASA 1135 http://www.nasa.gov/sites/default/files/734673main_Equations-Tables-Charts-CompressibleFlow-Report-1135.pdf
        Dim tolerance = 0.01
        Dim testMach As Boolean = Math.Abs(exitMach - 2.2) < tolerance
        Dim testPres As Boolean = Math.Abs((exitPressure / chamberPressure) - (0.09352)) < tolerance
        Dim testTemp As Boolean = Math.Abs((exitTemp / chamberTemp) - 0.5081) < tolerance
        Dim testSpeed As Boolean = Math.Abs((exitVelocity / aStar) - 1.71791) < tolerance
        Dim verdict As Boolean = testMach And testPres And testTemp And testSpeed 'true = pass, false = fail
        Dim verdictstring = vbCrLf & "Failed!"
        If verdict Then
            verdictstring = vbCrLf & "Success!"
        End If

        Dim testReport As String =
            "Test results for Ae/At = 2.005, k = 1.4:" & vbCrLf &
            "Mach: " & Convert.ToString(Format(exitMach, "#.####")) & " " & Convert.ToString(testMach) & vbCrLf &
            "Pres: " & Convert.ToString(Format((exitPressure / chamberPressure), "#.####")) & " " & Convert.ToString(testPres) & vbCrLf &
            "Temp: " & Convert.ToString(Format(exitTemp / chamberTemp, "#.####")) & " " & Convert.ToString(testTemp) & vbCrLf &
            "Speed: " & Convert.ToString(Format(exitVelocity / aStar, "#.####")) & " " & Convert.ToString(testSpeed) & vbCrLf &
            verdictstring
        MsgBox(testReport)

    End Sub

    Function solveMach(At As Double, Ae As Double, k As Double)
        ' solve Mach number from area ratio by iteration. assume supersonic
        ' https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
        Dim P = 2 / (k + 1)
        Dim Q = 1 - P
        Dim R1 = (Ae / At) ^ ((2 * Q) / P)
        Dim a = Q ^ (1 / P)
        Dim R2 = (R1 - 1) / (2 * a)
        Dim X = 1 / ((1 + R2) + Math.Sqrt(R2 * (R2 + 2)))  ' initial guess
        Dim diff = 1.0  ' initalize iteration difference
        Dim F, dF, Xnew, M
        While Math.Abs(diff) > 0.0001
            F = (P * X + Q) ^ (1 / P) - R1 * X
            dF = (P * X + Q) ^ ((1 / P) - 1) - R1
            Xnew = X - F / dF
            diff = Xnew - X
            X = Xnew
            M = 1 / Math.Sqrt(X)
        End While
        Return M
    End Function

    Private Sub UpDownAlpha_ValueChanged(sender As Object, e As EventArgs) Handles UpDownAlpha.ValueChanged
        Dim alpha = Convert.ToDouble(UpDownAlpha.Value) * Math.PI / 180 'convert to radians
        Dim Rt = Convert.ToDouble(UpDownRt.Value)
        Dim Re = Convert.ToDouble(UpDownRe.Value)

        Dim At = (Rt / 1000) ^ 2 * Math.PI
        Dim Ae = (Re / 1000) ^ 2 * Math.PI
        Dim L = (Re - Rt) / Math.Sin(alpha)
        Dim expansionratio = Ae / At

        LabelL.Text = L
        Labele.Text = expansionratio
    End Sub

    Private Sub UpDownRt_ValueChanged(sender As Object, e As EventArgs) Handles UpDownRt.ValueChanged
        Dim alpha = Convert.ToDouble(UpDownAlpha.Value) * Math.PI / 180 'convert to radians
        Dim Rt = Convert.ToDouble(UpDownRt.Value)
        Dim Re = Convert.ToDouble(UpDownRe.Value)

        Dim At = (Rt / 1000) ^ 2 * Math.PI
        Dim Ae = (Re / 1000) ^ 2 * Math.PI
        Dim L = (Re - Rt) / Math.Sin(alpha)
        Dim expansionratio = Ae / At

        LabelL.Text = L
        Labele.Text = expansionratio
    End Sub

    Private Sub UpDownRe_ValueChanged(sender As Object, e As EventArgs) Handles UpDownRe.ValueChanged
        Dim alpha = Convert.ToDouble(UpDownAlpha.Value) * Math.PI / 180 'convert to radians
        Dim Rt = Convert.ToDouble(UpDownRt.Value)
        Dim Re = Convert.ToDouble(UpDownRe.Value)

        Dim At = (Rt / 1000) ^ 2 * Math.PI
        Dim Ae = (Re / 1000) ^ 2 * Math.PI
        Dim L = (Re - Rt) / Math.Sin(alpha)
        Dim expansionratio = Ae / At

        LabelL.Text = L
        Labele.Text = expansionratio
    End Sub

End Class
