# Psych Online – web (HTML5) port

Patches that build Friday Night Funkin' Psych Online (Snirozu/Funkin-Psych-Online) for the browser with Lime/OpenFL html5.

- `src-patch/` – files changed/added versus upstream (overlay them on the upstream checkout): browser shims (`shim/`), 3D/Lua stubs (`stub3d/`), patched `source/`, `Project.xml`.
- `scripts/` – build (`rebuild.sh`), VFS manifest, boot loader, local server and browser test scripts.
- Build: `haxelib run lime build html5 -Dweb -nolaunch`.
- Mods: Online → Mod Downloader; downloads persist in browser IndexedDB.
- Not supported: Lua mods, videos, Discord, 3D stages, RAR/7z, raw-socket online play.

## Download the playable build
The full playable build is in the `PsychOnline-Web/` folder. Use **Code → Download ZIP** (or clone), then inside `PsychOnline-Web/` run `python3 serve.py` (or `start-server.bat`) and open http://localhost:8000.
