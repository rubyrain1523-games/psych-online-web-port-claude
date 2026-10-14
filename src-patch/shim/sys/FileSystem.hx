package sys;
#if macro


// This class is here so it re-shadows other FileSystem classes in macros,
// e.g. from hxnodejs.
@:coreApi
class FileSystem {
	extern static public function exists(path:String):Bool;

	extern static public function rename(path:String, newPath:String):Void;

	extern static public function stat(path:String):FileStat;

	extern static public function fullPath(relPath:String):String;

	static public function absolutePath(relPath:String):String {
		if (haxe.io.Path.isAbsolute(relPath))
			return relPath;
		return haxe.io.Path.join([Sys.getCwd(), relPath]);
	}

	extern static public function isDirectory(path:String):Bool;

	extern static public function createDirectory(path:String):Void;

	extern static public function deleteFile(path:String):Void;

	extern static public function deleteDirectory(path:String):Void;

	extern static public function readDirectory(path:String):Array<String>;
}

#else
import sys.io.File;


import haxe.io.Bytes;

class FileSystem {
	public static function exists(path:String):Bool {
		Vfs.init();
		var p = Vfs.norm(path);
		if (p == "") return true;
		if (Vfs.deleted.exists(p)) return false;
		return Vfs.overlay.exists(p) || Vfs.files.exists(p) || Vfs.dirs.exists(p) || Vfs.overlayDirs.exists(p);
	}

	public static function isDirectory(path:String):Bool {
		Vfs.init();
		var p = Vfs.norm(path);
		if (p == "") return true;
		return !Vfs.deleted.exists(p) && (Vfs.dirs.exists(p) || Vfs.overlayDirs.exists(p));
	}

	public static function readDirectory(path:String):Array<String> {
		Vfs.init();
		var p = Vfs.norm(path);
		var out:Array<String> = [];
		var base = Vfs.dirs.get(p);
		if (base != null) for (n in base) if (!Vfs.deleted.exists(p == "" ? n : p + "/" + n)) out.push(n);
		var prefix = p == "" ? "" : p + "/";
		for (k in Vfs.overlay.keys()) {
			if (StringTools.startsWith(k, prefix)) {
				var rest = k.substr(prefix.length);
				var n = rest.split("/")[0];
				if (n != "" && out.indexOf(n) < 0) out.push(n);
			}
		}
		for (k in Vfs.overlayDirs.keys()) {
			if (StringTools.startsWith(k, prefix) && k != p) {
				var n = k.substr(prefix.length).split("/")[0];
				if (n != "" && out.indexOf(n) < 0) out.push(n);
			}
		}
		return out;
	}

	public static function createDirectory(path:String):Void {
		Vfs.init();
		var p = Vfs.norm(path);
		var acc = "";
		for (s in p.split("/")) {
			acc = acc == "" ? s : acc + "/" + s;
			Vfs.overlayDirs.set(acc, true);
			Vfs.deleted.remove(acc);
		}
	}

	public static function deleteFile(path:String):Void {
		Vfs.init();
		var p = Vfs.norm(path);
		Vfs.overlay.remove(p);
		Vfs.deleted.set(p, true);
		Vfs.unpersist(p);
	}

	public static function deleteDirectory(path:String):Void {
		Vfs.init();
		var p = Vfs.norm(path);
		Vfs.overlayDirs.remove(p);
		Vfs.deleted.set(p, true);
	}

	public static function rename(from:String, to:String):Void {
		var b = File.getBytes(from);
		File.saveBytes(to, b);
		deleteFile(from);
	}

	public static function fullPath(path:String):String return "/" + Vfs.norm(path);
	public static function absolutePath(path:String):String return "/" + Vfs.norm(path);

	public static function stat(path:String):FileStat {
		Vfs.init();
		var p = Vfs.norm(path);
		var size = Vfs.overlay.exists(p) ? Vfs.overlay.get(p).length : (Vfs.files.exists(p) ? Vfs.files.get(p) : 0);
		var d = Date.now();
		return {gid: 0, uid: 0, atime: d, mtime: d, ctime: d, size: size, dev: 0, ino: 0, nlink: 1, rdev: 0, mode: 0};
	}
}

#end
