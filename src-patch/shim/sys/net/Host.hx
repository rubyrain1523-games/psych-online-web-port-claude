package sys.net;
#if macro


class Host {
	public var host(default, null):String;
	public var ip(default, null):Int;

	public function new(name:String) {
		host = name;
		init(resolve(name));
	}

	public function toString() {
		return hostToString(ip);
	}

	public function reverse() {
		return hostReverse(ip);
	}

	function init(ip:Int) {
		this.ip = ip;
	}

	extern static public function localhost():String;

	extern static function hostReverse(ip:Int):String;

	extern static function hostToString(ip:Int):String;

	extern static function resolve(name:String):Int;
}

#else


class Host {
	public var host(default, null):String;
	public function new(name:String) { host = name; }
	public function toString():String return host;
	public static function localhost():String return "localhost";
}

#end
