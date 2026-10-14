package sys.io;
#if macro


@:coreApi
class File {
	extern static public function getContent(path:String):String;

	extern static public function saveContent(path:String, content:String):Void;

	extern static public function getBytes(path:String):haxe.io.Bytes;

	extern static public function saveBytes(path:String, bytes:haxe.io.Bytes):Void;

	extern static public function read(path:String, binary:Bool = true):FileInput;

	extern static public function write(path:String, binary:Bool = true):FileOutput;

	extern static public function append(path:String, binary:Bool = true):FileOutput;

	extern static public function update(path:String, binary:Bool = true):FileOutput;

	static public function copy(srcPath:String, dstPath:String):Void {
		var s = read(srcPath, true);
		var d = write(dstPath, true);
		d.writeInput(s);
		s.close();
		d.close();
	}
}

#else


import haxe.io.Bytes;
import sys.Vfs;

class File {
	public static function getBytes(path:String):Bytes {
		Vfs.init();
		var p = Vfs.norm(path);
		if (Vfs.deleted.exists(p)) throw "File not found: " + path;
		if (Vfs.overlay.exists(p)) return Vfs.overlay.get(p);
		if (Vfs.files.exists(p)) {
			var b = Vfs.fetch(p);
			if (b != null) return b;
		}
		throw "File not found: " + path;
	}

	public static function getContent(path:String):String return getBytes(path).toString();

	public static function saveBytes(path:String, bytes:Bytes):Void {
		Vfs.init();
		var p = Vfs.norm(path);
		Vfs.deleted.remove(p);
		Vfs.overlay.set(p, bytes);
		Vfs.markDirs(p);
		Vfs.persist(p, bytes);
	}

	public static function saveContent(path:String, content:String):Void saveBytes(path, Bytes.ofString(content));

	public static function append(path:String, binary:Bool = true):FileOutput {
		var old:Bytes = null;
		try old = getBytes(path) catch (e:Dynamic) {}
		var o = new FileOutput(path, old);
		return o;
	}

	public static function write(path:String, binary:Bool = true):FileOutput return new FileOutput(path, null);

	public static function read(path:String, binary:Bool = true):FileInput return new FileInput(getBytes(path));

	public static function copy(src:String, dst:String):Void saveBytes(dst, getBytes(src));
}

#end
