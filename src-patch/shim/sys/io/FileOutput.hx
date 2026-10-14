package sys.io;
#if macro


// This class is not extern because externs overriding non-externs messes with DCE
@:coreApi
class FileOutput extends haxe.io.Output {
	extern public override function close():Void;

	extern public override function flush():Void;

	extern public function seek(p:Int, pos:FileSeek):Void;

	extern public function tell():Int;

	extern public override function writeByte(c:Int):Void;

	extern public override function writeBytes(bytes:haxe.io.Bytes, pos:Int, len:Int):Int;
}

#else


import haxe.io.Bytes;
import haxe.io.BytesBuffer;

class FileOutput extends haxe.io.Output {
	var path:String;
	var buf:BytesBuffer = new BytesBuffer();

	public function new(path:String, existing:Bytes) {
		this.path = path;
		if (existing != null) buf.add(existing);
	}

	override public function writeByte(c:Int):Void buf.addByte(c);

	override public function writeBytes(s:Bytes, pos:Int, len:Int):Int {
		buf.addBytes(s, pos, len);
		return len;
	}

	override public function flush():Void File.saveBytes(path, buf.getBytes());
	override public function close():Void flush();
	public function seek(p:Int, pos:FileSeek):Void {}
	public function tell():Int return 0;
}

#end
