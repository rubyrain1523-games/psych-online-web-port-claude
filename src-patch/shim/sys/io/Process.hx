package sys.io;
#if macro


private extern class NativeProcess {
	function new(cmd:String, ?args:Array<String>):Void;

	function close():Void;
	function exitCode():Int;
	function getPid():Int;
	function kill():Void;

	function readStderr(bytes:haxe.io.Bytes, pos:Int, len:Int):Int;
	function readStdout(bytes:haxe.io.Bytes, pos:Int, len:Int):Int;

	function closeStdin():Void;
	function writeStdin(bytes:haxe.io.Bytes, pos:Int, len:Int):Int;
}

private class Stdin extends haxe.io.Output {
	var proc:NativeProcess;
	var buf:haxe.io.Bytes;

	public function new(proc:NativeProcess) {
		this.proc = proc;
		buf = haxe.io.Bytes.alloc(1);
	}

	public override function close() {
		super.close();
		proc.closeStdin();
	}

	public override function writeByte(c:Int) {
		buf.set(0, c);
		writeBytes(buf, 0, 1);
	}

	public override function writeBytes(buf:haxe.io.Bytes, pos:Int, len:Int) {
		try {
			return proc.writeStdin(buf, pos, len);
		} catch (e:Dynamic) {
			throw new haxe.io.Eof();
		}
	}
}

private class Stdout extends haxe.io.Input {
	var proc:NativeProcess;
	var out:Bool;
	var buf:haxe.io.Bytes;

	public function new(proc:NativeProcess, out:Bool) {
		this.proc = proc;
		this.out = out;
		buf = haxe.io.Bytes.alloc(1);
	}

	public override function readByte() {
		if (readBytes(buf, 0, 1) == 0)
			throw haxe.io.Error.Blocked;
		return buf.get(0);
	}

	public override function readBytes(bytes:haxe.io.Bytes, pos:Int, len:Int):Int {
		try {
			if (out) {
				return proc.readStdout(bytes, pos, len);
			} else {
				return proc.readStderr(bytes, pos, len);
			}
		} catch (e:Dynamic) {
			throw new haxe.io.Eof();
		}
	}
}

@:coreApi
class Process {
	public var stdout(default, null):haxe.io.Input;
	public var stderr(default, null):haxe.io.Input;
	public var stdin(default, null):haxe.io.Output;

	var proc:NativeProcess;

	public function new(cmd:String, ?args:Array<String>, ?detached:Bool):Void {
		if (detached) {
			throw "Detached process is not supported on this platform";
		}
		proc = new NativeProcess(cmd, args);
		stdout = new Stdout(proc, true);
		stderr = new Stdout(proc, false);
		stdin = new Stdin(proc);
	}

	public inline function getPid():Int {
		return proc.getPid();
	}

	public function exitCode(block:Bool = true):Null<Int> {
		if (block == false)
			throw "Non blocking exitCode() not supported on this platform";
		return proc.exitCode();
	}

	public inline function close():Void {
		proc.close();
	}

	public inline function kill():Void {
		proc.kill();
	}
}

#else


class Process {
	public var stdout:haxe.io.Input = new haxe.io.BytesInput(haxe.io.Bytes.alloc(0));
	public var stderr:haxe.io.Input = new haxe.io.BytesInput(haxe.io.Bytes.alloc(0));
	public var stdin:haxe.io.Output = new haxe.io.BytesOutput();
	public function new(cmd:String, ?args:Array<String>, ?detached:Bool) { throw "Processes are not available in the browser"; }
	public function getPid():Int return 0;
	public function exitCode(block:Bool = true):Null<Int> return 1;
	public function close():Void {}
	public function kill():Void {}
}

#end
