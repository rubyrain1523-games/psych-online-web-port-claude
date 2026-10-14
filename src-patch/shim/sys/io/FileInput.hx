package sys.io;
#if macro


// This class is not extern because externs overriding non-externs messes with DCE
@:coreApi
class FileInput extends haxe.io.Input {
	extern public override function close():Void;

	extern public function eof():Bool;

	extern public function seek(p:Int, pos:FileSeek):Void;

	extern public function tell():Int;

	extern public override function readByte():Int;

	extern public override function readBytes(bytes:haxe.io.Bytes, pos:Int, len:Int):Int;
}

#else


import haxe.io.Bytes;

class FileInput extends haxe.io.BytesInput {
	public function new(b:Bytes) super(b);

	public function seek(p:Int, pos:FileSeek):Void {
		switch (pos) {
			case SeekBegin: this.position = p;
			case SeekCur: this.position += p;
			case SeekEnd: this.position = this.length + p;
		}
	}

	public function tell():Int return this.position;
	public function eof():Bool return this.position >= this.length;
}

#end
