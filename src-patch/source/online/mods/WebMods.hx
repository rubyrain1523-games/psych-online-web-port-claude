package online.mods;

/** Mods are not implemented in the browser version yet. */
class WebMods {
	public static inline var DISABLED:Bool = #if html5 true #else false #end;

	/** Returns true (and tells the player) when mods are unavailable. */
	public static function blocked():Bool {
		#if html5
		online.gui.Alert.alert("Not implemented yet", "Mods aren't available in the web version yet.");
		return true;
		#else
		return false;
		#end
	}
}
