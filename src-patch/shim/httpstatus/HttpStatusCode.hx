package httpstatus;

enum abstract HttpStatusCode(Int) from Int to Int {
	var Continue = 100;
	var OK = 200;
	var Created = 201;
	var Accepted = 202;
	var NoContent = 204;
	var MovedPermanently = 301;
	var Found = 302;
	var NotModified = 304;
	var BadRequest = 400;
	var Unauthorized = 401;
	var Forbidden = 403;
	var NotFound = 404;
	var MethodNotAllowed = 405;
	var RequestTimeout = 408;
	var Conflict = 409;
	var TooManyRequests = 429;
	var InternalServerError = 500;
	var NotImplemented = 501;
	var BadGateway = 502;
	var ServiceUnavailable = 503;
	var GatewayTimeout = 504;
}
