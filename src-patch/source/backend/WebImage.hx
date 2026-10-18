package backend;

import haxe.io.Bytes;
import openfl.display.BitmapData;

/**
 * Browsers can't decode images synchronously, so lime's BitmapData.fromFile/fromBytes return null on html5.
 * This decodes PNGs in Haxe instead (other formats fall back to null on the web).
 */
class WebImage {
	public static function fromBytes(bytes:Bytes):BitmapData {
		if (bytes == null)
			return null;
		#if html5
		try {
			var d = new format.png.Reader(new haxe.io.BytesInput(bytes)).read();
			var h = format.png.Tools.getHeader(d);
			var bgra = format.png.Tools.extract32(d);
			var w = h.width, ht = h.height;
			var data = new lime.utils.UInt8Array(w * ht * 4);
			var i = 0;
			var n = w * ht * 4;
			while (i < n) {
				data[i] = bgra.get(i + 2);
				data[i + 1] = bgra.get(i + 1);
				data[i + 2] = bgra.get(i);
				data[i + 3] = bgra.get(i + 3);
				i += 4;
			}
			var buf = new lime.graphics.ImageBuffer(data, w, ht);
			buf.format = lime.graphics.PixelFormat.RGBA32;
			buf.premultiplied = false;
			var img = new lime.graphics.Image(buf);
			img.premultiplied = true;
			return BitmapData.fromImage(img);
		} catch (e:Dynamic) {
			trace('WebImage: could not decode image (' + Std.string(e) + ')');
			return null;
		}
		#else
		return BitmapData.fromBytes(openfl.utils.ByteArray.fromBytes(bytes));
		#end
	}

	public static function fromFile(path:String):BitmapData {
		#if html5
		if (path == null || !sys.FileSystem.exists(path))
			return null;
		return fromBytes(sys.io.File.getBytes(path));
		#else
		return BitmapData.fromFile(path);
		#end
	}
}
