; 按住 Shift 时加速滚动
+WheelUp::Send("{WheelUp 10}")      ; 向上滚动10倍速度
+WheelDown::Send("{WheelDown 10}")  ; 向下滚动10倍速度

; 按住 Alt 时水平滚动
!WheelUp::Send("{WheelLeft 2}")     ; 向左滚动
!WheelDown::Send("{WheelRight 2}")  ; 向右滚动

!1::  ; Alt+1 —— 白色照片打印
{
    CoordMode("Mouse", "Client")  ; 全局设置一次即可

    printWin    := "打印图片 ahk_class NativeHWNDHost ahk_exe explorer.exe"
    settingsWin := "打印设置 ahk_class #32770 ahk_exe explorer.exe"
    propertyWin := "大打印机 属性 ahk_class #32770 ahk_exe explorer.exe"

    ; ── 第一步：激活「打印图片」并点击「选项」按钮 ──────────────────
    if !ActivateAndClick(printWin, 888, 618)
        return

    ; ── 第二步：激活「打印设置」并点击对应按钮 ──────────────────────
    if !ActivateAndClick(settingsWin, 51, 212)
        return

    ; ── 第三步：激活「打印机属性」并依次点击两个按钮 ────────────────
    if !ActivateAndClick(propertyWin, 270, 188)
        return
    Sleep(50)
    Click(638, 692)
}

!2::  ; Alt+2 —— 黑色照片打印
{
    CoordMode("Mouse", "Client")  ; 全局设置一次即可

    printWin    := "打印图片 ahk_class NativeHWNDHost ahk_exe explorer.exe"
    settingsWin := "打印设置 ahk_class #32770 ahk_exe explorer.exe"
    propertyWin := "大打印机 属性 ahk_class #32770 ahk_exe explorer.exe"

    ; ── 第一步：激活「打印图片」并点击「选项」按钮 ──────────────────
    if !ActivateAndClick(printWin, 888, 618)
        return

    ; ── 第二步：激活「打印设置」并点击对应按钮 ──────────────────────
    if !ActivateAndClick(settingsWin, 51, 212)
        return

    ; ── 第三步：激活「打印机属性」并依次点击两个按钮 ────────────────
    if !ActivateAndClick(propertyWin, 314, 258)
        return
    Sleep(50)
    Click(638, 692)
}

!3::  ; Alt+3 —— 保存照片到桌面
{
    CoordMode("Mouse", "Client")

    weiXinWin := "微信 ahk_class Qt51514QWindowIcon ahk_exe Weixin.exe"
    selectWin := "选择文件夹 ahk_class #32770 ahk_exe Weixin.exe"

    ; ── 第一步：点击保存按钮
    if !ActivateAndClick(weiXinWin, 808, 702)
        return

    ; ── 第二步：点击桌面
    if !ActivateAndClick(selectWin, 88, 202)
        return

    ; ── 第三步: 新建文件夹
		Send("^+n")
		Click(1054, 634, 2)
}

; ────────────────────────────────────────────────────────────────
; 辅助函数：等待窗口出现 → 激活 → 等待激活完成 → 延迟 → 点击
; 返回 true 表示成功，false 表示超时（并弹出提示）
; ────────────────────────────────────────────────────────────────
ActivateAndClick(winTitle, x, y, timeout := 4, delay := 100) {
    if !WinWait(winTitle, , timeout) {
        MsgBox("窗口未找到：" winTitle)
        return false
    }
    WinActivate(winTitle)
    WinWaitActive(winTitle, , timeout)
    Sleep(delay)
    Click(x, y)
    return true
}