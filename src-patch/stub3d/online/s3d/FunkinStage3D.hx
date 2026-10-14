package online.s3d;

import flixel.FlxBasic;
import flixel.FlxSprite;
import flx3d.FlxSprite3D;

/** HTML5 stub: load() always returns null so the game uses its normal 2D stage path. */
class FunkinStage3D extends FlxBasic {
	var view2:View3DHandler = new View3DHandler();

	public static function load(stageData:Dynamic):FunkinStage3D return null;

	public function add(sprite:FlxSprite, ?keep2D:Bool = false):FlxSprite3D return new FlxSprite3D();
	public function remove(sprite:FlxSprite3D):Void {}
	public function setPositionFromArray(object:FlxSprite3D, pos:Array<Float>):Void {}
	public function setFollowCamera(char:String, ?object:Dynamic):Void {}
	public function onDeath():Void {}
}
