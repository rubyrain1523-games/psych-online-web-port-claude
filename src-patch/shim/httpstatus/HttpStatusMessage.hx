package httpstatus;

abstract HttpStatusMessage(String) from String to String {
	@:from public static function fromCode(code:Int):HttpStatusMessage return switch (code) {
		case 200: "OK"; case 201: "Created"; case 204: "No Content"; case 301: "Moved Permanently"; case 302: "Found";
		case 400: "Bad Request"; case 401: "Unauthorized"; case 403: "Forbidden"; case 404: "Not Found";
		case 500: "Internal Server Error"; case 503: "Service Unavailable"; default: "Status " + code;
	}
}
