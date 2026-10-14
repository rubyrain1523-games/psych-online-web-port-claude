package openfl.filesystem;

class File {
	public static var applicationDirectory:File = new File();
	public static var applicationStorageDirectory:File = new File();
	public static var userDirectory:File = new File();
	public static var documentsDirectory:File = new File();
	public var nativePath:String = ".";
	public var url:String = "";
	public function new(?path:String) { if (path != null) nativePath = path; }
}
