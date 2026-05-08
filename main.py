import socket
import threading
import struct
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

class ChatClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        self.sock = None
        self.connected = False
        self.cid = 0
        self.h_format = "!BII"
        self.h_size = struct.calcsize(self.h_format)

        # --- Верхняя панель: Комната и Протокол ---
        top_box = BoxLayout(size_hint_y=0.1, spacing=5)
        self.room_input = TextInput(text='101', multiline=False, hint_text="Комната")
        self.proto_btn = Button(text="TCP", size_hint_x=0.3)
        self.proto_btn.bind(on_release=self.toggle_proto)
        top_box.add_widget(self.room_input)
        top_box.add_widget(self.proto_btn)
        self.add_widget(top_box)

        # --- Центр: Лог сообщений ---
        self.scroll = ScrollView(size_hint_y=0.6)
        self.log_label = Label(text="Добро пожаловать!\n", size_hint_y=None, halign='left', valign='top')
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.scroll.add_widget(self.log_label)
        self.add_widget(self.scroll)

        # --- Низ: Ввод сообщения и кнопка ---
        self.msg_input = TextInput(hint_text="Сообщение...", multiline=False, size_hint_y=0.1)
        self.add_widget(self.msg_input)

        btn_box = BoxLayout(size_hint_y=0.1, spacing=5)
        self.conn_btn = Button(text="Войти", background_color=get_color_from_hex('#2ecc71'))
        self.conn_btn.bind(on_release=self.toggle_connection)
        
        send_btn = Button(text="Отправить", background_color=get_color_from_hex('#3498db'))
        send_btn.bind(on_release=lambda x: self.send_message())
        
        btn_box.add_widget(self.conn_btn)
        btn_box.add_widget(send_btn)
        self.add_widget(btn_box)

    def toggle_proto(self, instance):
        instance.text = "UDP" if instance.text == "TCP" else "TCP"

    def write_log(self, text):
        # В Kivy обновление UI должно идти через основной поток
        Clock.schedule_once(lambda dt: self._update_log(text))

    def _update_log(self, text):
        self.log_label.text += f"{text}\n"

    def toggle_connection(self, instance):
        if not self.connected:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        room = self.room_input.get_focus_next() # или просто self.room_input.text
        proto = self.proto_btn.text
        self.cid = int(time.time() * 1000) % 1000000
        
        try:
            if proto == "TCP":
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("127.0.0.1", 50007))
                payload = f"{self.room_input.text}:{self.cid}".encode()
                header = struct.pack(self.h_format, 9, len(payload), self.cid)
                self.sock.sendall(header + payload)
            else:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = f"{self.room_input.text}:{self.cid}".encode()
                header = struct.pack(self.h_format, 9, len(payload), self.cid)
                self.sock.sendto(header + payload, ("127.0.0.1", 50008))

            self.connected = True
            self.conn_btn.text = "Выйти"
            self.conn_btn.background_color = get_color_from_hex('#e74c3c')
            self.write_log(f"Подключено к {self.room_input.text} via {proto}")
            
            threading.Thread(target=self.receive_loop, daemon=True).start()
            # Запускаем Heartbeat
            Clock.schedule_interval(self.send_heartbeat, 15)
        except Exception as e:
            self.write_log(f"Ошибка: {e}")

    def disconnect(self):
        self.connected = False
        if self.sock: self.sock.close()
        self.conn_btn.text = "Войти"
        self.conn_btn.background_color = get_color_from_hex('#2ecc71')
        self.write_log("Отключено.")

    def send_message(self):
        if not self.connected: return
        msg = self.msg_input.text
        if not msg: return
        try:
            payload = msg.encode()
            header = struct.pack(self.h_format, 1, len(payload), self.cid)
            if self.proto_btn.text == "TCP":
                self.sock.sendall(header + payload)
            else:
                self.sock.sendto(header + payload, ("127.0.0.1", 50008))
            self.write_log(f"Вы: {msg}")
            self.msg_input.text = ""
        except Exception as e:
            self.write_log(f"Ошибка отправки: {e}")

    def send_heartbeat(self, dt):
        if not self.connected: return False
        try:
            packet = struct.pack(self.h_format, 255, 0, self.cid)
            if self.proto_btn.text == "TCP": self.sock.sendall(packet)
            else: self.sock.sendto(packet, ("127.0.0.1", 50008))
        except: return False

    def receive_loop(self):
        while self.connected:
            try:
                if self.proto_btn.text == "TCP":
                    header = self.sock.recv(self.h_size)
                    m_type, m_size, sid = struct.unpack(self.h_format, header)
                    payload = self.sock.recv(m_size).decode()
                else:
                    data, _ = self.sock.recvfrom(65535)
                    m_type, m_size, sid = struct.unpack(self.h_format, data[:self.h_size])
                    payload = data[self.h_size:self.h_size+m_size].decode()
                
                if m_type != 255:
                    self.write_log(f"[{sid}]: {payload}")
            except: break

class HybridApp(App):
    def build(self):
        return ChatClient()

if __name__ == '__main__':
    HybridApp().run()
