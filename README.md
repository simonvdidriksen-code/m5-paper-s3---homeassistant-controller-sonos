# M5Paper S3 – Home Assistant controller (lights, scenes, Sonos)

An ESPHome firmware that turns the **M5Stack M5Paper S3** (4.7" 540×960 e-ink, touch) into a battery-powered wall/desk panel for Home Assistant.

**▶ Live demo (clickable):** https://simonvdidriksen-code.github.io/m5-paper-s3---homeassistant-controller-sonos/

## Features

- **Areas page:** up to 12 rooms. A tap switches all of a room's lights on or off; a hold opens the room with every light (on/off and a 10-step brightness bar) and up to 4 scenes. The row shows temperature, humidity and CO₂.
- **Sonos page:** tick rooms, then play a Sonos favorite or radio station on them, step the volume (−5 / −2 / +2 / +5 %), play/pause, and group or split all zones.
- **Everything is set up from Home Assistant:** names, icons, lights, scenes and sensors per area, the four playlist buttons, sleep and wake behaviour. Nothing needs editing in the YAML for that.
- **E-ink tuned:** pure black and white, so every refresh uses the fast mode (~0.25 s); LVGL draws straight into the e-ink driver's buffer and only changed rows are refreshed.
- **Battery friendly:** sleeps with Wi-Fi off after a set time. A tap or picking it up wakes it (~0.3 s to Wi-Fi, ~1.2 s to HA). Taps made while it reconnects are queued and sent once HA is back.
- **Power off** from HA or the battery icon leaves a "Slukket" (off) screen on the e-ink.

## Files

| Path | What |
|---|---|
| `m5paper-areas.yaml` | The ESPHome firmware (one file) |
| `secrets.example.yaml` | The secrets it needs: copy to `secrets.yaml` and fill in |
| `docs/index.html` | The clickable demo (GitHub Pages) |
| `design/` | Source of the screen design (Claude Design artifact) |
| `tools/` | Helper scripts used while developing (area YAML generator, stack-frame check, …) |

## Install

1. In **ESPHome Device Builder** (Home Assistant add-on or desktop app), open *Secrets* and add the keys from `secrets.example.yaml` with your own values:
   ```yaml
   wifi_ssid: "your-wifi-name"
   wifi_password: "your-wifi-password"
   api_encryption_key: "32 random bytes, base64"
   ```
2. Create a device and paste the whole `m5paper-areas.yaml` into it. Change `static_ip`, `gateway`, `subnet` and `dns` under `substitutions` to fit your network.
3. Install. In Home Assistant: *Settings → Devices & services → ESPHome → M5Paper Areas → Configure* → enable **Allow the device to perform Home Assistant actions** (without it, taps do nothing).

Needs ESPHome 2026.10 or newer (ESP-IDF, LVGL 9). The e-ink driver comes from [patrick3399/esphome_components](https://github.com/patrick3399/esphome_components) (`ed047tc1`) and [patrick3399/epdiy](https://github.com/patrick3399/epdiy).

## Setting up areas in Home Assistant

On the device page, under **Configuration**, per area 1–12:

| Setting | What to enter |
|---|---|
| Area N name | Shown on the row and as the room screen's title |
| Area N icon | Pick from the list (Kitchen, Living room, Bedroom, Garage, …) |
| Area N lights | Up to 6 entity ids, comma separated: `light.kitchen_spots, light.dining_table`. `light.` may be left out. `light.x=Spots` shows "Spots" instead of HA's name. Switches work too (no brightness bar). |
| Area N scenes | Up to 4 scenes (or scripts): `scene.cozy, scene.dinner=Dinner` |
| Area N sensors | `temperature, humidity, CO2` by position: `climate.x, sensor.y_humidity`. Leave one out with an empty place (`, ,`). A climate entity gives its current temperature / humidity. |

An area with nothing set is hidden, and so are empty light and scene places. Changes show on the panel within about a second. New entities make HA reconnect once, about 3 s after the last change, so it subscribes to them.

The playlist buttons are "Playlist button 1–4"; the list to pick from is the Sonos favorites in `fav_options` / `fav_ids` in the YAML (see `sensor.sonos_favorites` in HA).

## Credits

- [ESPHome](https://esphome.io) and [LVGL](https://lvgl.io)
- [epdiy](https://github.com/vroland/epdiy) e-ink driver (patrick3399 fork) and the `ed047tc1` ESPHome component
- Icons: [Material Design Icons](https://pictogrammers.com/library/mdi/)
- Font: [Atkinson Hyperlegible](https://www.brailleinstitute.org/freefont/)
