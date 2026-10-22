param([string]$Target)
# Appends the "one room's lights" LVGL page (6 light rows) to the firmware YAML.
$nl = "`n"
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append(@'

    # ================================================================ One room's lights
    # Opened by holding a room's row on Areas. One row per light: name and
    # state, bulb button (on/off) and brightness bar (tap where you want it).
    # Filled in by repaint_detail; rows the room doesn't need are hidden.
    - id: area_detail_page
      scrollable: false
      scrollbar_mode: "OFF"
      widgets:
        # Back to Areas
        - obj:
            styles: plain
            x: 12
            y: 12
            width: SIZE_CONTENT
            height: 56
            pad_right: 16
            scrollable: false
            layout: { type: FLEX, flex_flow: ROW, flex_align_cross: CENTER, pad_column: 8 }
            on_press:
              - script.execute: { id: show_page, idx: 0 }
            widgets:
              - label: { styles: area_icon, text: "\U000F004D" }
              - label: { text: "Areas", text_font: font_name, text_color: 0x000000 }
        - label: { id: dt_title, x: 20, y: 72, width: 500, text: "", text_font: font_title, text_color: 0x000000, long_mode: DOT }

        - obj:
            styles: plain
            x: 16
            y: 120
            width: 508
            height: 750
            scrollable: false
            clickable: false
            layout: { type: FLEX, flex_flow: COLUMN, pad_row: 6 }
            widgets:
'@)
for ($r = 0; $r -lt 6; $r++) {
  $row = @'
              # ---- light {N1}
              - obj:
                  id: dt_row{N}
                  styles: row_style
                  width: 100%
                  height: 120
                  pad_top: 8
                  pad_bottom: 8
                  scrollable: false
                  clickable: false
                  layout: { type: FLEX, flex_flow: COLUMN, pad_row: 6 }
                  widgets:
                    - obj:
                        styles: plain
                        width: 100%
                        height: 52
                        scrollable: false
                        clickable: false
                        layout: { type: FLEX, flex_flow: ROW, flex_align_cross: CENTER, pad_column: 14 }
                        widgets:
                          - obj:
                              styles: plain
                              flex_grow: 1
                              height: SIZE_CONTENT
                              scrollable: false
                              clickable: false
                              layout: { type: FLEX, flex_flow: COLUMN, pad_row: 2 }
                              widgets:
                                - label: { id: dt_name{N}, styles: area_name, text: "", width: 100%, long_mode: DOT }
                                - label: { id: dt_state{N}, styles: area_sub, text: "", width: 100%, long_mode: DOT }
                          - button:
                              id: dt_btn{N}
                              width: 72
                              height: 48
                              on_press:
                                - script.execute: { id: light_tap, row: {N} }
                              widgets:
                                - label: { id: dt_bulb{N}, styles: bulb_icon, align: CENTER, text: "\U000F0E50" }
                    - bar:
                        id: dt_bar{N}
                        styles: bri_bar
                        width: 100%
                        height: 40
                        min_value: 0
                        max_value: 100
                        value: 0
                        clickable: true
                        indicator:
                          bg_color: 0x000000
                          bg_opa: COVER
                          radius: 4
                        on_press:
                          - script.execute: { id: light_bri_tap, row: {N} }

'@
  [void]$sb.Append($row.Replace('{N1}', [string]($r + 1)).Replace('{N}', [string]$r))
}
$text = $sb.ToString().Replace("`r`n", "`n")
$orig = [IO.File]::ReadAllText($Target, [Text.Encoding]::UTF8)
if ($orig.Contains("id: area_detail_page")) { throw "detail page already present" }
if ($orig.Contains("`r`n")) { $text = $text.Replace("`n", "`r`n") }
$orig = $orig.TrimEnd("`r", "`n") + ($(if ($orig.Contains("`r`n")) { "`r`n" } else { "`n" }))
[IO.File]::WriteAllText($Target, $orig + $text, (New-Object Text.UTF8Encoding($false)))
"appended " + ($text.Split("`n").Count) + " lines"
