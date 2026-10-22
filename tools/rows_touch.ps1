param([string]$Target)
# Light rows on the room lights screen: the whole box switches the light; the
# brightness bar gets a touch zone around it (margin) that sets brightness.
$old = @'
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
$new = @'
              # The whole box switches the light, except the brightness zone
              - obj:
                  id: dt_row{N}
                  styles: row_style
                  width: 100%
                  height: 120
                  pad_left: 0
                  pad_right: 0
                  pad_top: 6
                  pad_bottom: 0
                  scrollable: false
                  layout: { type: FLEX, flex_flow: COLUMN, pad_row: 0 }
                  on_press:
                    - script.execute: { id: light_tap, row: {N} }
                  widgets:
                    - obj:
                        styles: plain
                        width: 100%
                        height: 48
                        pad_left: 16
                        pad_right: 10
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
                              clickable: false
                              widgets:
                                - label: { id: dt_bulb{N}, styles: bulb_icon, align: CENTER, text: "\U000F0E50" }
                    # Brightness zone: the bar plus a margin around it (12 px
                    # above, to the box's edges below and at the sides). A tap
                    # anywhere in it sets brightness, never switches the light.
                    - obj:
                        styles: plain
                        width: 100%
                        height: 62
                        pad_left: 16
                        pad_right: 10
                        pad_top: 12
                        pad_bottom: 10
                        scrollable: false
                        on_press:
                          - script.execute: { id: light_bri_tap, row: {N} }
                        widgets:
                          - bar:
                              id: dt_bar{N}
                              styles: bri_bar
                              width: 100%
                              height: 40
                              min_value: 0
                              max_value: 100
                              value: 0
                              clickable: false
                              indicator:
                                bg_color: 0x000000
                                bg_opa: COVER
                                radius: 4
'@
$t = [IO.File]::ReadAllText($Target, [Text.Encoding]::UTF8)
$crlf = $t.Contains("`r`n")
$n = 0
for ($r = 0; $r -lt 6; $r++) {
  $o = $old.Replace("`r`n", "`n").Replace('{N}', [string]$r)
  $w = $new.Replace("`r`n", "`n").Replace('{N}', [string]$r)
  if ($crlf) { $o = $o.Replace("`n", "`r`n"); $w = $w.Replace("`n", "`r`n") }
  if ($t.Contains($o)) { $t = $t.Replace($o, $w); $n++ }
}
if ($n -ne 6) { throw "matched $n of 6 rows" }
[IO.File]::WriteAllText($Target, $t, (New-Object Text.UTF8Encoding($false)))
"rows updated: $n"
