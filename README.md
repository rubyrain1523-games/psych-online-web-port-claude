# Friday Night Funkin' Psych Online – Play in Browser (HTML5 Web Port, Chromebook Friendly)

**FNF Psych Online web port** – play **Friday Night Funkin' Psych Online** (Snirozu/Funkin-Psych-Online) directly in your browser from **GitHub Pages**, with nothing to install. Works on **Chromebook**, Windows, Mac, Linux and touch screens. Includes **mod support**, an **offline version**, and a built-in **FNF Mod Maker / chart editor**.

**Play online:** https://rubyrain1523-games.github.io/psych-online-web-port-claude/
**Play offline (download everything):** see [OFFLINE-DOWNLOAD.md](OFFLINE-DOWNLOAD.md)

> Unofficial fan-made port. Not affiliated with the Friday Night Funkin' creators or the Psych Online team.

## Features
- FNF Psych Online running as an HTML5 / WebGL (Lime, OpenFL, Flixel) web game, no Flash and no download needed
- Online multiplayer rooms and account sign-in (needs internet)
- **FNF mods in the browser:** import mod `.zip` files or use the in-game mod downloader; Vanilla and Modded start modes
- **Hidden mode:** opens the game in an about:blank tab
- **Play offline** from a folder or a local `index.html`; the hosted version also caches after your first visit
- **Touch controls** for tablets and Chromebooks (one finger per lane, 3-finger pause)
- **FNF Mod Maker** built into the game:
  - piano-roll music maker with synth, 8 drum pads, custom samples and MIDI import
  - note chart editor with fine note snapping, waveform view and hold notes
  - **record your taps** with your own keys (for example A S ; ')
  - play-as-opponent option, exports ready-to-play mod zips
- Fixes: pause/resume audio desync, mania lanes, menu music, mod images and songs

## Search keywords
Friday Night Funkin unblocked, FNF unblocked, FNF Psych Engine online, Psych Online in browser, FNF web port, FNF HTML5, FNF GitHub Pages, FNF Chromebook, FNF school Chromebook, FNF offline, FNF mods in browser, FNF mod maker, FNF chart editor, FNF song maker, FNF multiplayer online, Funkin rhythm game, Haxe Lime OpenFL Flixel.

## Developer notes
Patches that build Friday Night Funkin' Psych Online (Snirozu/Funkin-Psych-Online) for the browser with Lime/OpenFL html5.

- `src-patch/` – files changed/added versus upstream (overlay them on the upstream checkout): browser shims (`shim/`), 3D/Lua stubs (`stub3d/`), patched `source/`, `Project.xml`.
- `scripts/` – build (`rebuild.sh`), VFS manifest, boot loader, local server and browser test scripts.
- Build: `haxelib run lime build html5 -Dweb -nolaunch`.
- Mods: Online → Mod Downloader; downloads persist in browser IndexedDB.
- Not supported: Lua mods, videos, Discord, 3D stages, RAR/7z, raw-socket online play.

## Download the playable build
The full playable build is in the `PsychOnline-Web/` folder. Use **Code → Download ZIP** (or clone), then inside `PsychOnline-Web/` run `python3 serve.py` (or `start-server.bat`) and open http://localhost:8000.

## Mods
Drop zipped mods into the top-level `mods/` folder of this repo. The game installs new/changed zips automatically when it loads (see `mods/README.txt`).
