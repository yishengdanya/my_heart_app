import math
import random
import json
import os
import sys
import re
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty

# ---------- 配置路径（适配 Android 沙盒目录） ----------
class Config:
    def __init__(self):
        self.app = App.get_running_app()
        self.config_dir = self.app.user_data_dir  # Android 私有目录 /data/data/包名/files/
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "total_windows": 200,
            "messages_file": ""
        }
        self.MAX_WINDOWS = 370
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self.default_config.copy()

    def save_config(self, new_config):
        self.config = new_config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4)
        except:
            pass


# ---------- 自定义气泡标签（仿 Tkinter Toplevel） ----------
class Bubble(Label):
    bg_color = StringProperty("#FFB6C1")  # 默认暖色

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = kwargs.get('bg_color', "#FFB6C1")
        self.text = kwargs.get('text', "")
        self.bind(size=self.update_rect, pos=self.update_rect)
        with self.canvas.before:
            Color(*self.hex_to_rgba(self.bg_color))
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    @staticmethod
    def hex_to_rgba(hex_code):
        """将 #FFB6C1 转为 (1.0, 0.71, 0.76, 1.0)"""
        hex_code = hex_code.lstrip('#')
        lv = len(hex_code)
        if lv == 6:
            r, g, b = int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
            return (r/255.0, g/255.0, b/255.0, 1.0)
        return (1.0, 0.71, 0.76, 1.0)


# ---------- 核心动画逻辑 ----------
class HeartAnimation:
    def __init__(self, container, total_windows, messages_file):
        self.container = container  # FloatLayout 容器
        self.total_windows = total_windows
        self.messages_file = messages_file
        self.warm_colors = [
            "#FFB6C1", "#FFC0CB", "#F8C8DC", "#FFD1DC", "#FFE4E6",
            "#E6E6FA", "#D8BFD8", "#DDA0DD", "#B0E0E6", "#87CEEB",
            "#AFEEEE", "#98FB98", "#FFE4B5", "#FFDAB9", "#FFA07A",
            "#FFCCCB", "#F5C6CB", "#C1F0F6", "#A3E4D7", "#D0F0C0"
        ]
        self.messages = self.load_messages()
        self.bubbles = []
        self.heart_index = 0
        self.random_index = 0
        self.is_running = True

    def load_messages(self):
        default_msgs = [
            "别熬夜", "我想你了", "保持微笑", "记得吃水果", "每天都要开心",
            "你的微笑很特别", "照顾好自己", "多喝水", "记得想我", "要一直幸福哦",
            "保持好心情", "天天都要元气满满", "记得吃饭", "爱你哟", "晚安",
            "你是最棒的", "注意休息", "保持可爱", "心想事成", "一切顺利",
            "今天也很想你", "要开心哦", "你值得被爱", "永远支持你", "相信自己",
            "你是独一无二的", "今天过得怎么样", "想你想到睡不着", "你笑起来真好看",
            "有你在真好", "我会一直陪着你", "你是我最珍贵的", "爱你每一天",
            "你让世界更美好", "我的心里只有你", "与你相遇好幸运", "你是我的一切",
            "爱你到永远", "你是我最美的风景", "心心念念都是你", "想你每一刻",
            "你是我生命的光", "爱你如初", "你是我唯一的爱", "心中只有你",
            "爱你三千遍", "你是我最甜的梦", "想抱抱你", "你让我心跳加速",
            "爱你胜过一切", "你是我最美的意外", "我的世界因你而亮", "只想和你在一起",
            "每分每秒都想你", "你是我心动的理由", "有你的日子都是晴天", "爱你没商量",
            "你是我所有的温柔", "想和你一起慢慢变老", "你是我最美的遇见", "爱你如命",
            "你是我掌心的宝贝", "我的爱只给你", "你是我永远的牵挂", "爱你到白头",
            "你是我眼中的星辰", "我的世界只有你", "你是我最美的梦想", "爱你无期限"
        ]
        if self.messages_file and os.path.isfile(self.messages_file):
            try:
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                parts = re.split(r'[,，]+', content)
                msgs = [p.strip() for p in parts if p.strip()]
                if msgs:
                    return self._adjust_count(msgs)
            except:
                pass
        return self._adjust_count(default_msgs)

    def _adjust_count(self, msgs):
        if len(msgs) >= self.total_windows:
            return msgs[:self.total_windows]
        else:
            repeats = (self.total_windows // len(msgs)) + 1
            return (msgs * repeats)[:self.total_windows]

    def generate_heart_points(self):
        points = []
        start_t = 0
        screen_w = Window.width
        screen_h = Window.height
        win_w, win_h = 160, 90
        for i in range(self.total_windows):
            t = start_t + i * 2 * math.pi / self.total_windows
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            scale = min(screen_w // 3 / 16, screen_h // 3 / 13)
            offset_x = screen_w // 2
            offset_y = screen_h // 2 - 100
            win_x = int(offset_x + x * scale - win_w // 2)
            win_y = int(offset_y - y * scale - win_h // 2)
            points.append((win_x, win_y))
        return points

    def start(self):
        self.heart_points = self.generate_heart_points()
        self.heart_index = 0
        Clock.schedule_once(self.create_next_heart, 0.3)

    def create_next_heart(self, dt=None):
        if not self.is_running:
            return
        if self.heart_index >= self.total_windows:
            Clock.schedule_once(self.start_random_phase, 3.0)
            return
        x, y = self.heart_points[self.heart_index]
        color = random.choice(self.warm_colors)
        message = self.messages[self.heart_index]
        bubble = Bubble(
            text=message,
            bg_color=color,
            size_hint=(None, None),
            size=(160, 90),
            pos=(x, y),
            font_name="Roboto",
            font_size="12sp",
            halign="center",
            valign="middle"
        )
        self.container.add_widget(bubble)
        self.bubbles.append(bubble)
        self.heart_index += 1
        Clock.schedule_once(self.create_next_heart, 0.05)

    def start_random_phase(self, dt=None):
        self.clear_bubbles()
        self.random_index = 0
        Clock.schedule_once(self.create_next_random, 0.02)

    def create_next_random(self, dt=None):
        if not self.is_running:
            return
        if self.random_index >= self.total_windows:
            Clock.schedule_once(self.start_fade_out, 1.0)
            return
        screen_w = Window.width
        screen_h = Window.height
        margin = 150
        x = random.randint(-margin, screen_w - 160 + margin)
        y = random.randint(-margin, screen_h - 90 + margin)
        color = random.choice(self.warm_colors)
        message = random.choice(self.messages)
        bubble = Bubble(
            text=message,
            bg_color=color,
            size_hint=(None, None),
            size=(160, 90),
            pos=(x, y),
            font_name="Roboto",
            font_size="12sp",
            halign="center",
            valign="middle"
        )
        self.container.add_widget(bubble)
        self.bubbles.append(bubble)
        self.random_index += 1
        Clock.schedule_once(self.create_next_random, 0.02)

    def start_fade_out(self, dt=None):
        self.fade_index = len(self.bubbles) - 1
        self.fade_out_step()

    def fade_out_step(self, dt=None):
        if not self.is_running:
            return
        if self.fade_index < 0:
            self.clear_bubbles()
            self.is_running = False
            return
        bubble = self.bubbles[self.fade_index]
        if bubble in self.container.children:
            # 每一帧逐步降低透明度
            if not hasattr(bubble, '_fade_step'):
                bubble._fade_step = 0
            bubble._fade_step += 1
            if bubble._fade_step >= 5:
                self.container.remove_widget(bubble)
                self.bubbles[self.fade_index] = None
                self.fade_index -= 1
                Clock.schedule_once(self.fade_out_step, 0.03)
            else:
                bubble.opacity = 1.0 - (bubble._fade_step / 5.0)
                Clock.schedule_once(self.fade_out_step, 0.03)
        else:
            self.fade_index -= 1
            Clock.schedule_once(self.fade_out_step, 0.03)

    def clear_bubbles(self):
        for b in self.bubbles:
            if b and b in self.container.children:
                self.container.remove_widget(b)
        self.bubbles.clear()

    def stop(self):
        self.is_running = False
        self.clear_bubbles()


# ---------- 设置弹窗 ----------
class SettingsPopup(Popup):
    def __init__(self, config, on_save_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "爱心弹窗设置"
        self.size_hint = (0.8, 0.6)
        self.config = config
        self.on_save_callback = on_save_callback
        self.build_content()

    def build_content(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 数量设置
        count_box = BoxLayout(size_hint_y=None, height=40)
        count_box.add_widget(Label(text=f"弹窗数量 (最大 370):", size_hint_x=0.4))
        self.count_input = TextInput(text=str(self.config["total_windows"]), multiline=False, input_filter="int")
        count_box.add_widget(self.count_input)
        layout.add_widget(count_box)

        # 消息文件设置
        file_box = BoxLayout(size_hint_y=None, height=40)
        file_box.add_widget(Label(text="消息文件:", size_hint_x=0.3))
        self.file_input = TextInput(text=self.config["messages_file"], multiline=False, size_hint_x=0.5)
        file_box.add_widget(self.file_input)
        browse_btn = Button(text="浏览", size_hint_x=0.2)
        browse_btn.bind(on_press=self.open_file_chooser)
        file_box.add_widget(browse_btn)
        layout.add_widget(file_box)

        # 保存按钮
        save_btn = Button(text="保存", size_hint_y=None, height=50)
        save_btn.bind(on_press=self.save_config)
        layout.add_widget(save_btn)

        self.content = layout

    def open_file_chooser(self, instance):
        # 简单文件选择器，Android 下需在 buildozer 添加读取权限
        chooser = FileChooserIconView()
        popup = Popup(title="选择消息文件", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=lambda *args: self.on_file_selected(args[0], popup))
        popup.open()

    def on_file_selected(self, selection, popup):
        if selection:
            self.file_input.text = selection[0]
        popup.dismiss()

    def save_config(self, instance):
        try:
            total = int(self.count_input.text)
            if total <= 0 or total > 370:
                total = 200
        except:
            total = 200
        new_config = {
            "total_windows": total,
            "messages_file": self.file_input.text.strip()
        }
        self.on_save_callback(new_config)
        self.dismiss()


# ---------- 主应用 ----------
class HeartApp(App):
    def build(self):
        self.config_mgr = Config()
        self.animation = None

        # 主布局
        self.root_layout = FloatLayout()

        # 控制面板（底部居中）
        control_box = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            spacing=20
        )

        start_btn = Button(text="❤️ 开始 ❤️", font_size="18sp")
        start_btn.bind(on_press=self.start_animation)
        control_box.add_widget(start_btn)

        settings_btn = Button(text="⚙️ 设置", font_size="18sp")
        settings_btn.bind(on_press=self.open_settings)
        control_box.add_widget(settings_btn)

        self.root_layout.add_widget(control_box)

        # 启动时自动运行一次（可选，若不想自动运行可注释掉）
        Clock.schedule_once(lambda dt: self.start_animation(None), 0.5)

        return self.root_layout

    def start_animation(self, instance):
        if self.animation and self.animation.is_running:
            return
        # 清除旧的动画
        if self.animation:
            self.animation.stop()
        self.animation = HeartAnimation(
            self.root_layout,
            self.config_mgr.config["total_windows"],
            self.config_mgr.config["messages_file"]
        )
        self.animation.start()

    def open_settings(self, instance):
        def on_save(new_config):
            self.config_mgr.save_config(new_config)
            if self.animation:
                self.animation.stop()
                self.animation = None
        popup = SettingsPopup(self.config_mgr.config, on_save)
        popup.open()

    def on_stop(self):
        if self.animation:
            self.animation.stop()
        sys.exit(0)


if __name__ == "__main__":
    HeartApp().run()