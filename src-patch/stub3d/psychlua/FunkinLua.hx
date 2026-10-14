package psychlua;

/** HTML5 stub: Lua scripting is desktop-only (needs native LuaJIT). HScript still works. */
class FunkinLua {
	public static var Function_Stop:Dynamic = "##PSYCHLUA_FUNCTIONSTOP";
	public static var Function_Continue:Dynamic = "##PSYCHLUA_FUNCTIONCONTINUE";
	public static var Function_StopLua:Dynamic = "##PSYCHLUA_FUNCTIONSTOPLUA";
	public static var Function_StopHScript:Dynamic = "##PSYCHLUA_FUNCTIONSTOPHSCRIPT";
	public static var Function_StopAll:Dynamic = "##PSYCHLUA_FUNCTIONSTOPALL";

	public var scriptName:String = '';
	public var modFolder:String = null;
	public var closed:Bool = true;
	public var lua:Dynamic = null;
	public var hscript:Dynamic = null;
	public var callbacks:Map<String, Dynamic> = new Map<String, Dynamic>();
	public static var customFunctions:Map<String, Dynamic> = new Map<String, Dynamic>();
	public static var lastCalledScript:FunkinLua = null;
	public var lastCalledFunction:String = '';

	public static function trace(text:String, ?ignoreCheck:Bool, ?deprecated:Bool, ?color:Dynamic):Void {}
	public static function getBuildTarget():String return 'browser';
	public static var modchartSprites:Map<String, Dynamic> = new Map();

	public function new(scriptName:String, ?skipPsychStuff:Bool = false) { this.scriptName = scriptName; }
	public function call(func:String, args:Array<Dynamic>):Dynamic return Function_Continue;
	public function set(variable:String, data:Dynamic):Void {}
	public function stop():Void {}
	public function quickGC():Void {}
	public function addLocalCallback(name:String, myFunction:Dynamic):Void {}
	public function luaTrace(text:String, ignoreCheck:Bool = false, deprecated:Bool = false, ?color:Dynamic):Void {}
}
