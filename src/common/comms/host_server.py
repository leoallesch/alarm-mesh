from zeroconf import Zeroconf, ServiceInfo
import socket
import threading
import time


class AlarmHost:
    SERVICE_TYPE = "_alarmhost._tcp.local."
    SERVICE_NAME = "AlarmHostService._alarmhost._tcp.local."

    def __init__(self, port=5000):
        self.port = port
        self.zeroconf = Zeroconf()
        self.service_info = None
        self.running = False

    def start(self):
        ip = socket.gethostbyname(socket.gethostname())

        self.service_info = ServiceInfo(
            type_=self.SERVICE_TYPE,
            name=self.SERVICE_NAME,
            addresses=[socket.inet_aton(ip)],
            port=self.port,
            properties={"role": "host"}
        )

        print(f"[HOST] Registering service at {ip}:{self.port}")
        self.zeroconf.register_service(self.service_info)
        self.running = True

        # Optional: background loop (if you need one)
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.running:
            time.sleep(1)

    def stop(self):
        print("[HOST] Stopping service")
        if self.service_info:
            self.zeroconf.unregister_service(self.service_info)
        self.zeroconf.close()
        self.running = False


if __name__ == "__main__":
    host = AlarmHost(port=5000)
    host.start()
    input("Press Enter to stop host...\n")
    host.stop()
