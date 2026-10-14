package sys.net;
#if macro


import haxe.io.Error;
import eval.vm.NativeSocket;

private class SocketOutput extends haxe.io.Output {
	var socket:NativeSocket;

	public function new(socket:NativeSocket) {
		this.socket = socket;
	}

	public override function writeByte(c:Int) {
		try {
			socket.sendChar(c);
		} catch (e:Dynamic) {
			if (e == "Blocking")
				throw Blocked;
			else if (e == "EOF")
				throw new haxe.io.Eof();
			else
				throw Custom(e);
		}
	}

	public override function writeBytes(buf:haxe.io.Bytes, pos:Int, len:Int) {
		return try {
			socket.send(buf, pos, len);
		} catch (e:Dynamic) {
			if (e == "Blocking")
				throw Blocked;
			else
				throw Custom(e);
		}
	}

	public override function close() {
		super.close();
		socket.close();
	}
}

private class SocketInput extends haxe.io.Input {
	var socket:NativeSocket;

	public function new(socket:NativeSocket) {
		this.socket = socket;
	}

	public override function readByte() {
		return try {
			socket.receiveChar();
		} catch (e:Dynamic) {
			if (e == "Blocking")
				throw Blocked;
			else
				throw new haxe.io.Eof();
		}
	}

	public override function readBytes(buf:haxe.io.Bytes, pos:Int, len:Int) {
		var r;
		try {
			r = socket.receive(buf, pos, len);
		} catch (e:Dynamic) {
			if (e == "Blocking")
				throw Blocked;
			else
				throw Custom(e);
		}
		if (r == 0)
			throw new haxe.io.Eof();
		return r;
	}

	public override function close() {
		super.close();
		socket.close();
	}
}

@:coreApi
class Socket {
	public var input(default, null):haxe.io.Input;
	public var output(default, null):haxe.io.Output;
	public var custom:Dynamic;

	@:ifFeature("sys.net.Socket.select") var socket:NativeSocket;

	public function new() {
		init(new NativeSocket());
	}

	private function init(socket:NativeSocket):Void {
		this.socket = socket;
		input = new SocketInput(socket);
		output = new SocketOutput(socket);
	}

	public function close():Void {
		socket.close();
	}

	public function read():String {
		return input.readAll().toString();
	}

	public function write(content:String):Void {
		output.writeString(content);
	}

	public function connect(host:Host, port:Int):Void {
		socket.connect(host.ip, port);
	}

	public function listen(connections:Int):Void {
		socket.listen(connections);
	}

	public function shutdown(read:Bool, write:Bool):Void {
		socket.shutdown(read, write);
	}

	public function bind(host:Host, port:Int):Void {
		socket.bind(host.ip, port);
	}

	public function accept():Socket {
		var nativeSocket = socket.accept();
		var socket:Socket = Type.createEmptyInstance(Socket);
		socket.init(nativeSocket);
		return socket;
	}

	@:access(sys.net.Host.init)
	public function peer():{host:Host, port:Int} {
		var info = socket.peer();
		var host:Host = Type.createEmptyInstance(Host);
		host.init(info.ip);
		return {host: host, port: info.port};
	}

	@:access(sys.net.Host.init)
	public function host():{host:Host, port:Int} {
		var info = socket.host();
		var host:Host = Type.createEmptyInstance(Host);
		host.init(info.ip);
		return {host: host, port: info.port};
	}

	public function setTimeout(timeout:Float):Void {
		socket.setTimeout(timeout);
	}

	public function waitForRead():Void {
		select([this], null, null, -1);
	}

	public function setBlocking(b:Bool):Void {} // TODO: Don't know how to implement this...

	public function setFastSend(b:Bool):Void {
		socket.setFastSend(b);
	}

	public static function select(read:Array<Socket>, write:Array<Socket>, others:Array<Socket>,
			?timeout:Float):{read:Array<Socket>, write:Array<Socket>, others:Array<Socket>} {
		return NativeSocket.select(read, write, others, timeout);
	}
}

#else


class Socket {
	public var input:haxe.io.Input;
	public var output:haxe.io.Output;
	public var custom:Dynamic;
	public function new() { throw "Raw sockets are not available in the browser"; }
	public function connect(host:Host, port:Int):Void {}
	public function close():Void {}
	public function write(s:String):Void {}
	public function read():String return "";
	public function peer():{host:Host, port:Int} return null;
	public function setBlocking(b:Bool):Void {}
	public function setTimeout(t:Float):Void {}
	public function shutdown(r:Bool, w:Bool):Void {}
	public function bind(host:Host, port:Int):Void {}
	public function listen(n:Int):Void {}
	public function accept():Socket return null;
	public function waitForRead():Void {}
	public static function select(read:Array<Socket>, write:Array<Socket>, others:Array<Socket>, ?timeout:Float):{read:Array<Socket>, write:Array<Socket>, others:Array<Socket>} return {read: [], write: [], others: []};
}

#end
