package sys.thread;
#if macro


import eval.vm.NativeThread;

private typedef ThreadImpl = NativeThread;

abstract Thread(ThreadImpl) from ThreadImpl {
	public var events(get,never):EventLoop;

	static function __init__() {
		NativeThread.self().events = new EventLoop();
	}

	inline function new(h:NativeThread):Void {
		this = h;
	}

	public inline function sendMessage(msg:Dynamic):Void {
		this.sendMessage(msg);
	}

	public static inline function current():Thread {
		return new Thread(NativeThread.self());
	}

	public static inline function create(job:()->Void):Thread {
		return new Thread(new NativeThread(job));
	}

	public static function runWithEventLoop(job:()->Void):Void {
		var thread = NativeThread.self();
		if(thread.events == null) {
			thread.events = new EventLoop();
			try {
				job();
				thread.events.loop();
				thread.events = null;
			} catch(e) {
				thread.events = null;
				throw e;
			}
		} else {
			job();
		}
	}

	public static inline function createWithEventLoop(job:()->Void):Thread {
		return new Thread(new NativeThread(() -> {
			var thread = NativeThread.self();
			thread.events = new EventLoop();
			job();
			thread.events.loop();
		}));
	}

	public static inline function readMessage(block:Bool):Dynamic {
		return NativeThread.readMessage(block);
	}

	public static inline function yield():Void {
		NativeThread.yield();
	}

	@:op(A == B)
	public inline function equals(other:Thread):Bool {
		return getHandle().id() == other.getHandle().id();
	}

	inline function getHandle():NativeThread {
		return this;
	}

	function get_events():EventLoop {
		if(this.events == null)
			throw new NoEventLoopException();
		return this.events;
	}

	@:keep
	static function processEvents():Void {
		NativeThread.self().events.loop();
	}
}

#else


/** Single-threaded browser shim: "threads" run on the next tick. */
class Thread {
	static var main_:Thread = new Thread();
	public function new() {}
	public static function create(fn:Void->Void):Thread {
		js.Browser.window.setTimeout(function() fn(), 0);
		return new Thread();
	}
	public static function current():Thread return main_;
	public static function runWithEventLoop(fn:Void->Void):Void fn();
	public function sendMessage(msg:Dynamic):Void {}
	public static function readMessage(block:Bool):Dynamic return null;
}

#end
