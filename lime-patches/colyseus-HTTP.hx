package io.colyseus;

using io.colyseus.events.EventHandler;
using io.colyseus.error.HttpException;

typedef HttpOptions = {
    ?headers: Map<String, String>,
    ?body: Dynamic
}

enum abstract Method(String) from String to String {
    var GET = "GET";
    var POST = "POST";
    var PUT = "PUT";
    var DELETE = "DELETE";
}

/** Patched for browser builds: uses haxe.Http instead of tink_http. */
@:keep
class HTTP {
    public var authToken: String;
    private var client: Client;

    public function new (client: Client) {
        this.client = client;
    }

    public function get(segments: String, ?options: HttpOptions, callback: (HttpException,Dynamic)->Void) {
		this.request(Method.GET, segments, options, callback);
    }

    public function post(segments: String, ?options: HttpOptions, callback: (HttpException,Dynamic)->Void) {
		this.request(Method.POST, segments, options, callback);
    }

    public function put(segments: String, ?options: HttpOptions, callback: (HttpException,Dynamic)->Void) {
		this.request(Method.PUT, segments, options, callback);
    }

    public function delete(segments: String, ?options: HttpOptions, callback: (HttpException,Dynamic)->Void) {
		this.request(Method.DELETE, segments, options, callback);
    }

    public function request(method: Method, segments: String, ?options: HttpOptions, callback: (HttpException,Dynamic)->Void) {
        var body: String = "";
        var h = new haxe.Http(this.buildHttpEndpoint(segments));

        if (options != null && options.body != null) {
            body = Std.isOfType(options.body, String) ? cast options.body : haxe.format.JsonPrinter.print(options.body);
            h.setHeader("Content-Type", "application/json");
            h.setPostData(body);
        }
        if (options != null && options.headers != null) {
            for (header in options.headers.keys())
                h.setHeader(header, options.headers.get(header));
        }
        if (this.authToken != null)
            h.setHeader("Authorization", 'Bearer ${this.authToken}');
        h.setHeader("Accept", "application/json");

        var status = 0;
        h.onStatus = function(s) status = s;
        h.onData = function(data:String) {
            try {
                var response = haxe.Json.parse(data);
                if (response.error) {
                    var code:Int = status;
                    if (response.code != null) code = cast response.code;
                    callback(new HttpException(code, cast response.error), null);
                } else {
                    callback(null, response);
                }
            } catch (e:Dynamic) {
                callback(new HttpException(status, Std.string(e)), null);
            }
        };
        h.onError = function(msg:String) {
            var message = msg;
            try {
                var response = haxe.Json.parse(h.responseData);
                if (response != null && response.error != null) message = cast response.error;
            } catch (e:Dynamic) {}
            callback(new HttpException(status, message), null);
        };
        h.request(method == Method.POST || method == Method.PUT || (options != null && options.body != null));
    }

    public function buildHttpEndpoint(segments: String, ?protocol: String = "http") {
        if (segments.charAt(0) == "/") {
            segments = segments.substr(1);
        }
        return '${protocol}${(this.client.settings.useSSL) ? "s" : ""}://${this.client.settings.hostname}${this.getEndpointPort()}/${segments}';
    }

    public function getEndpointPort() {
        return (this.client.settings.port != 80 && this.client.settings.port != 443)
            ? ':${this.client.settings.port}'
            : '';
    }
}
