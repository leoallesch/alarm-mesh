import threading
from common.comms.protocol import Alarm, AlarmEvent, EventType


class AlarmManager:
    """Manages alarm state and handles alarm-related events"""
    
    def __init__(self, event_callback):
        """
        Initialize the alarm manager.
        
        Args:
            event_callback: Function to call when broadcasting events.
                           Takes (event: AlarmEvent) as argument.
        """
        self.current_alarm = None  # Single Alarm object scheduled
        self.alarm_active = False  # Is an alarm currently triggered?
        self.snooze_responses = set()  # Addresses that have sent snooze
        self.lock = threading.Lock()
        self.event_callback = event_callback

    def set_alarm(self, alarm: Alarm):
        """Set the alarm to be scheduled"""
        with self.lock:
            self.current_alarm = alarm
        print(f"[ALARM] Alarm scheduled for {alarm}")
        # Broadcast alarm set to nodes so they can update indicators
        try:
            event = AlarmEvent(EventType.ALARM_SET, {"alarm": alarm.to_dict()})
            self.event_callback(event)
        except Exception as e:
            print(f"[ALARM] Failed to broadcast ALARM_SET: {e}")

    def remove_alarm(self):
        """Remove the currently scheduled alarm"""
        with self.lock:
            self.current_alarm = None
            self.alarm_active = False
            self.snooze_responses.clear()
        print("[ALARM] Alarm removed")
        # Optionally broadcast a clear event when alarm is removed
        try:
            event = AlarmEvent(EventType.ALARM_CLEARED, {"reason": "alarm removed by user"})
            self.event_callback(event)
        except Exception as e:
            print(f"[ALARM] Failed to broadcast ALARM_CLEARED: {e}")

    def trigger_alarm(self, alarm: Alarm):
        """Trigger an alarm and broadcast to all nodes"""
        with self.lock:
            if self.alarm_active:
                print("[ALARM] An alarm is already active, ignoring new trigger")
                return
            
            self.alarm_active = True
            self.snooze_responses.clear()
        
        print(f"[ALARM] ALARM TRIGGERED for {alarm}")
        event = AlarmEvent(
            EventType.ALARM_TRIGGERED,
            {"alarm": alarm.to_dict()},
            expires_at=alarm.get_next_trigger_time()
        )
        self.event_callback(event)

    def handle_snooze(self, addr, connected_nodes_count: int):
        """Handle a snooze event from a node"""
        print(f"[ALARM] Snooze pressed by {addr}")
        with self.lock:
            self.snooze_responses.add(addr)
            # Check if all nodes + host have sent snooze (addr=None for host)
            if len(self.snooze_responses) > connected_nodes_count:
                print(f"[ALARM] All nodes and host have snoozed. Alarm cleared.")
                self._clear_alarm()

    def handle_host_snooze(self):
        """Handle snooze button press on the host"""
        print(f"[ALARM] Host snooze button pressed")
        with self.lock:
            if not self.alarm_active:
                print("[ALARM] Alarm not active, ignoring snooze")
                return
            self.snooze_responses.add("host")
    
    def _clear_alarm(self):
        """Clear the active alarm (must be called with lock held)"""
        self.alarm_active = False
        self.snooze_responses.clear()
        
        print("[ALARM] Alarm cleared, resetting for next scheduled alarm")
        event = AlarmEvent(EventType.ALARM_CLEARED, {"reason": "all nodes snoozed"})
        self.event_callback(event)

    def is_alarm_active(self) -> bool:
        """Check if an alarm is currently active"""
        with self.lock:
            return self.alarm_active

    def get_current_alarm(self) -> Alarm:
        """Get the currently scheduled alarm"""
        with self.lock:
            return self.current_alarm
