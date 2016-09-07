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
        Dim R0 = 0.008314    ' [J/K*kmol] Universal gas constant

        ' get inputs
        Dim mMol, k, Pc, Tc, alpha, Rt, Re As Double ' inputs
        mMol = Convert.ToDouble(LabelmMol.Text)
        k = Convert.ToDouble(Labelk.Text)
        alpha = Convert.ToDouble(UpDownAlpha.Value) * Math.PI / 180 'convert to radians
        Rt = Convert.ToDouble(UpDownRt.Value)
        Re = Convert.ToDouble(UpDownRe.Value)
        Pc = Convert.ToDouble(UpDownPc.Value)
        Tc = Convert.ToDouble(updownTc.value)

        Dim L, At, Pt, Tt, mdot, Ae, M, Pe, Te, ve, expansionRatio, F, Isp, CF, vc As Double ' outputs

        ''DEBUG VALUES
        'At = 1.0 'm2
        'Ae = 2.005 'm2
        'k = 1.4
        'mMol = 28.02 'kJ/kmol
        'Pc = 25 'bar
        'Tc = 273 'K
        ''END DEBUG VALUES

        Dim R = R0 / mMol
        At = (Rt / 1000) ^ 2 * Math.PI
        Ae = (Re / 1000) ^ 2 * Math.PI
        L = (Re - Rt) / Math.Sin(alpha)
        expansionRatio = Ae / At

        Dim critP = (2 / (k + 1)) ^ (k / (k - 1))
        Pt = Pc * critP
        Tt = Tc * (2 / (k + 1))
        mdot = (Pt / (R * Tt)) * Math.Sqrt(k * R * Tt) * At
        Dim astar = Math.Sqrt(2 * k * R * Tt) 'speed of sound at throat

        M = solveMach(At, Ae, k)
        ve = Math.Sqrt(((2 * k * R * Tc) / (k - 1)) * (1 - (1 / (1 + ((k - 1) / 2) * M ^ 2))))
        Pe = Pc / ((1 + ((k - 1) / 2) * M ^ 2) ^ (k / (k - 1)))
        Te = Tc / (1 + ((k - 1) / 2) * M ^ 2)

        vc = Pt * At / mdot
        CF = (ve / vc) + (Ae / At) * (Pe / Pc)

        F = At * Pc * CF
        Isp = F / (g0 * mdot)

        ' set outputs
        LabelL.Text = L
        Labele.Text = expansionRatio
        LabelPt.Text = Pt
        LabelTt.Text = Tt
        Labelmdot.Text = mdot
        LabelPe.Text = Pe
        LabelTe.Text = Te
        LabelM.Text = M
        Labelve.Text = ve
        LabelF.Text = F
        LabelIsp.Text = Isp

        'math checkouts
        ' From page 635, NASA 1135 http://www.nasa.gov/sites/default/files/734673main_Equations-Tables-Charts-CompressibleFlow-Report-1135.pdf

        Dim testMach As Boolean = Math.Abs(M - 2.2) < 0.001
        Dim testPres As Boolean = Math.Abs((Pe / Pt) - (0.09352)) < 0.00001
        Dim testTemp As Boolean = Math.Abs((Te / Tt) - 0.5081) < 0.0001
        Dim testSpeed As Boolean = Math.Abs((ve / astar) - 1.71791) < 0.00001
        Dim verdict As Boolean = testMach And testPres And testTemp And testSpeed 'true = pass, false = fail
        Dim verdictstring = vbCrLf & "Failed!"
        If verdict Then
            verdictstring = vbCrLf & "Success!"
        End If

        Dim testReport As String =
            "Test results for Ae/At = 2.005, k = 1.4:" & vbCrLf &
            "Mach: " & Convert.ToString(Format(M, "#.##")) & " " & Convert.ToString(testMach) & vbCrLf &
            "Pres: " & Convert.ToString(Format(Pe / Pt, "#.#####")) & " " & Convert.ToString(testPres) & vbCrLf &
            "Temp: " & Convert.ToString(Format(Te / Tt, "#.####")) & " " & Convert.ToString(testTemp) & vbCrLf &
            "Speed: " & Convert.ToString(Format(ve / astar, "#.#####")) & " " & Convert.ToString(testSpeed) & vbCrLf &
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
        While Math.Abs(diff) > 0.01
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
