import http.server, socketserver, sys, os
os.chdir(sys.argv[1])
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
class S(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads=True; allow_reuse_address=True
S(('0.0.0.0',8123),H).serve_forever()
