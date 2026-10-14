package online.s3d;

class View3DHandler {
	public static var instance:View3DHandler = new View3DHandler();
	public var debugMode:Bool = false;
	public var onDebug:Bool->Void;
	public function new() {}
}
