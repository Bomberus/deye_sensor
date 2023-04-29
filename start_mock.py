# pylint: skip-file
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64

status_page = """
var webdata_sn = "2210250828";
var webdata_msvn = "";
var webdata_ssvn = "";
var webdata_pv_type = "";
var webdata_rate_p = "";
var webdata_now_p = "111";
var webdata_today_e = "0.60";
var webdata_total_e = "12.3";
var webdata_alarm = "";
var webdata_utime = "0";
var cover_mid = "4173291202";
var cover_ver = "MW3_15U_5406_1.49R";
var cover_wmode = "APSTA";
var cover_ap_ssid = "AP_4173291202";
var cover_ap_ip = "10.10.100.254";
var cover_ap_mac = "EC:FD:F8:7C:AC:A0";
var cover_sta_ssid = "Reichsfunkantenne";
var cover_sta_rssi = "28%";
var cover_sta_ip = "192.168.178.98";
var cover_sta_mac = "E8:FD:F8:7C:AC:A0";
var status_a = "1";
var status_b = "0";
var status_c = "0";
""".encode()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        username = "test"
        password = "test"
        self._auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"no auth header received")
        elif self.headers.get("Authorization") == "Basic " + self._auth:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(status_page)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get("Authorization").encode())
            self.wfile.write(b"not authenticated")


httpd = HTTPServer(("localhost", 8888), SimpleHTTPRequestHandler)
httpd.serve_forever()
