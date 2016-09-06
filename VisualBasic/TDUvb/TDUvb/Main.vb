Public Class Main
    Private Sub ComboBox1_SelectedIndexChanged(sender As Object, e As EventArgs) Handles ComboBox1.SelectedIndexChanged

    End Sub
    Private Sub doMath_Click(sender As Object, e As EventArgs) Handles doMath.Click

        ' math testing, At = 1, Ae = 2.005, k = 1.4
        ' From page 635, NASA 1135 http://www.nasa.gov/sites/default/files/734673main_Equations-Tables-Charts-CompressibleFlow-Report-1135.pdf
        Dim tolerance = 0.0001


        Dim g0 = 9.81        ' [m/s^2] Standard gravity
        Dim R0 = 0.008314    ' [J/K*kmol] Universal gas constant
        ' get variables
        Dim mMol, k, Pc, Tc, alpha, Rt, Re As Double ' inputs
        Dim L, At, Pt, Tt, mdot, Ae, M, Pe, Te, ve, expansionRatio, F, Isp, CF, vc As Double ' outputs

        'DEBUG VALUES
        At = 1.0 'm2
        Ae = 2.005 'm2
        k = 1.4
        mMol = 28.02 'kJ/kmol
        Pc = 25 'bar
        Tc = 273 'K
        'END DEBUG VALUES

        Dim R = R0 / mMol
        ' At = (Rt / 1000) ^ 2 * Math.PI
        ' Ae = (Re / 1000) ^ 2 * Math.PI
        L = (Re - Rt) / Math.Sin(alpha / (180 / Math.PI))
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

        'math checkouts
        Dim testMach As Boolean = M - 2.2 < tolerance
        Dim testPres As Boolean = (Pe / Pt) - (0.9352 ^ -1) < tolerance
        Dim testTemp As Boolean = (Te / Tc) - 0.5081 < tolerance
        Dim testSpeed As Boolean = (ve / astar) - 1.71791 < tolerance
        Dim verdict As Boolean = testMach And testPres And testTemp And testSpeed 'true = pass, false = fail
        Dim verdictstring = vbCrLf & "Failed!"
        If verdict Then
            verdictstring = vbCrLf & "Success!"
        End If

        Dim testReport As String =
            "Test results for Ae/At = 2.005, k = 1.4:" & vbCrLf &
            "Mach: " & Convert.ToString(Format(M, "#.##")) & " " & Convert.ToString(testMach) & vbCrLf &
            "Pres: " & Convert.ToString(Format(Pe / Pt, "#.####")) & " " & Convert.ToString(testPres) & vbCrLf &
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
        Dim diff = 1  ' initalize iteration difference
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
End Class
