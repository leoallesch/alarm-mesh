from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
import threading
import time


class AlarmNode:
    SERVICE_TYPE = "_alarmhost._tcp.local."

    def __init__(self):
        self.zeroconf = Zeroconf()
        self.host_info = None
        self.found_host_event = threading.Event()

    def start_discovery(self):
        print("[NODE] Searching for AlarmHost services...")
        ServiceBrowser(
            self.zeroconf,
            self.SERVICE_TYPE,
            handlers=[self._on_service_state_change]
        )

    def _on_service_state_change(self, zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                ip = ".".join(map(str, info.addresses[0]))
                print(f"[NODE] Found host {name} at {ip}:{info.port}")
                self.host_info = info
                self.found_host_event.set()

    def wait_for_host(self, timeout=None):
        """Blocks until host is found or timeout expires."""
        found = self.found_host_event.wait(timeout)
        return found, self.host_info

    def stop(self):
        print("[NODE] Stopping node discovery")
        self.zeroconf.close()


if __name__ == "__main__":
    node = AlarmNode()
    node.start_discovery()

    print("[NODE] Waiting for host...")
    found, info = node.wait_for_host(timeout=10)

    if found:
        ip = ".".join(map(str, info.addresses[0]))
        print(f"[NODE] Connected to host at {ip}:{info.port}")
    else:
        print("[NODE] No host found.")

    node.stop()
