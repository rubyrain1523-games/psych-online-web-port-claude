package online.mods;

/** Mods in the browser version are opt-in: the launcher menu sets window.__psychModsEnabled. */
class WebMods {
	public static function enabled():Bool {
		#if html5
		return js.Syntax.code("!!window.__psychModsEnabled");
		#else
		return true;
		#end
	}

	/** Returns true (and tells the player) when mods are unavailable. */
	public static function blocked():Bool {
		#if html5
		if (!enabled()) {
			online.gui.Alert.alert("Not implemented yet", "Mods are off in this mode. Reload and pick a Modded option to use them.");
			return true;
		}
		#end
		return false;
	}
}
