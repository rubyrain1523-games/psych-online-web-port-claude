package sys;

import haxe.io.Bytes;

/** Browser virtual file system: read-only manifest of shipped files fetched with sync XHR, plus an in-memory write overlay. */
class Vfs {
	static var inited = false;
	public static var files:Map<String, Int> = new Map(); // path -> size
	public static var dirs:Map<String, Array<String>> = new Map(); // dir -> children names
	public static var overlay:Map<String, Bytes> = new Map();
	public static var deleted:Map<String, Bool> = new Map();
	public static var overlayDirs:Map<String, Bool> = new Map();
	public static var baseUrl = "";

	public static function norm(p:String):String {
		p = StringTools.replace(p, "\\", "/");
		while (p.indexOf("//") >= 0) p = StringTools.replace(p, "//", "/");
		var parts = [];
		for (s in p.split("/")) {
			if (s == "." || s == "") continue;
			if (s == "..") { parts.pop(); continue; }
			parts.push(s);
		}
		return parts.join("/");
	}

	public static function init() {
		if (inited) return;
		inited = true;
		#if js
		// restore mods saved in the browser's IndexedDB cache (loaded by index.html before the game starts)
		try {
			var persisted:Dynamic = untyped js.Browser.window.__vfsPersist;
			if (persisted != null) {
				for (k in Reflect.fields(persisted)) {
					var v:Dynamic = Reflect.field(persisted, k);
					overlay.set(k, Bytes.ofData(v.buffer != null ? v.buffer.slice(v.byteOffset, v.byteOffset + v.byteLength) : v));
					markDirs(k);
				}
			}
		} catch (e:Dynamic) {
			trace("VFS cache restore failed: " + e);
		}
		try {
			var x = new js.html.XMLHttpRequest();
			x.open("GET", baseUrl + "vfs_manifest.json", false);
			x.send();
			if (x.status == 200 || x.status == 0) {
				var j:Dynamic = haxe.Json.parse(x.responseText);
				for (f in Reflect.fields(j.files)) files.set(f, Reflect.field(j.files, f));
				for (f in Reflect.fields(j.dirs)) dirs.set(f, Reflect.field(j.dirs, f));
			}
		} catch (e:Dynamic) {
			trace("VFS manifest load failed: " + e);
		}
		#end
	}

	public static function markDirs(p:String):Void {
		var parts = p.split("/");
		parts.pop();
		var acc = "";
		for (s in parts) {
			acc = acc == "" ? s : acc + "/" + s;
			overlayDirs.set(acc, true);
			deleted.remove(acc);
		}
	}

	public static function shouldPersist(p:String):Bool
		return StringTools.startsWith(p, "mods/") || p == "modsList.txt";

	public static function persist(p:String, b:Bytes):Void {
		#if js
		if (!shouldPersist(p)) return;
		try {
			var db:Dynamic = untyped js.Browser.window.__vfsDb;
			if (db == null) return;
			var tx = db.transaction("files", "readwrite");
			var copy = new js.lib.Uint8Array(b.length);
			copy.set(untyped b.b.subarray(0, b.length));
			tx.objectStore("files").put(copy, p);
		} catch (e:Dynamic) {}
		#end
	}

	public static function unpersist(p:String):Void {
		#if js
		if (!shouldPersist(p)) return;
		try {
			var db:Dynamic = untyped js.Browser.window.__vfsDb;
			if (db == null) return;
			var tx = db.transaction("files", "readwrite");
			tx.objectStore("files").delete(p);
		} catch (e:Dynamic) {}
		#end
	}

	public static function fetch(path:String):Bytes {
		#if js
		var x = new js.html.XMLHttpRequest();
		x.open("GET", baseUrl + path, false);
		x.overrideMimeType("text/plain; charset=x-user-defined");
		x.send();
		if (x.status != 200 && x.status != 0) return null;
		var s = x.responseText;
		var b = Bytes.alloc(s.length);
		for (i in 0...s.length) b.set(i, s.charCodeAt(i) & 0xff);
		return b;
		#else
		return null;
		#end
	}
}
