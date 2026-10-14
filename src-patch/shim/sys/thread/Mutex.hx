package sys.thread;
#if macro


#if (!target.threaded)
#error "This class is not available on this target"
#end

/**
	Creates a mutex, which can be used to acquire a temporary lock
	to access some ressource. The main difference with a lock is
	that a mutex must always be released by the owner thread.
**/
extern class Mutex {
	/**
		Creates a mutex.
	**/
	function new():Void;

	/**
		The current thread acquire the mutex or wait if not available.
		The same thread can acquire several times the same mutex but
		must release it as many times it has been acquired.
	**/
	function acquire():Void;

	/**
		Try to acquire the mutex, returns true if acquire or false
		if it's already locked by another thread.
	**/
	function tryAcquire():Bool;

	/**
		Release a mutex that has been acquired by the current thread.
		The behavior is undefined if the current thread does not own
		the mutex.
	**/
	function release():Void;
}

#else


class Mutex {
	public function new() {}
	public function acquire():Void {}
	public function tryAcquire():Bool return true;
	public function release():Void {}
}

#end
