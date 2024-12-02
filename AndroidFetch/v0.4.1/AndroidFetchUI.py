# Made by cocobo1

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ColorProperty, StringProperty
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty, BooleanProperty

# Register the custom font (you can replace with any .ttf file you prefer)
LabelBase.register(name="Default", fn_regular="NotoSans-Regular.ttf")

LabelBase.register(name="NotoEmojis", fn_regular="NotoEmoji-Regular.ttf")

import subprocess
import platform

def GetProp(Prop):
    result = subprocess.run(f"getprop {Prop}", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {Prop} not found or failed to execute."

ButtonPressNum = 0
TitleSecret = ""
CustomFlavour = ""

SDKInfo = GetProp("ro.build.version.sdk")
AndroidInfo = GetProp("ro.build.version.release")
ModelName = GetProp("ro.product.model")
VNDKInfo = GetProp("ro.vndk.version")
KernelInfo = GetProp("ro.kernel.version")
BootloaderInfo = GetProp("sys.oem_unlock_allowed")
BootloaderInfo = BootloaderInfo.replace("0", "Locked")
BootloaderInfo = BootloaderInfo.replace("1", "Unlocked")
Languege = GetProp("persist.sys.locale")
TimeZone = GetProp("persist.sys.timezone")
KnoxVersion = ""
AndroidFlavour = "Unknown"
PhoneMaker = GetProp("ro.product.brand")
ArchInfo = GetProp("ro.product.cpu.abi")
CPUInfo = GetProp("ro.netflix.bsp_rev")
HDRInfo = GetProp("ro.surface_flinger.has_HDR_display")
HDRInfo = HDRInfo.replace("true", "supported")
HDRInfo = HDRInfo.replace("false", "unsupported")
WideColourInfo = GetProp("ro.surface_flinger.has_wide_color_display")
WideColourInfo = WideColourInfo.replace("true", "supported")
WideColourInfo = WideColourInfo.replace("false", "unsupported")
VariableFPS = GetProp("ro.surface_flinger.use_content_detection_for_refresh_rate")
VariableFPS = VariableFPS.replace("true", "supported")
VariableFPS = VariableFPS.replace("false", "unsupported")

OneUiVersion = GetProp("ro.build.version.oneui")
OneUiVersion = OneUiVersion.replace("0", ".")
OneUiVersion = OneUiVersion.replace("..", "")
if OneUiVersion != "":
	AndroidFlavour = "OneUi " + OneUiVersion
if PhoneMaker == "samsung":
	KnoxVersion = GetProp("net.knoxvpn.version")
	KnoxVersion = "Knox Version: " + KnoxVersion

class MainScreen(Screen):
	pass

class SettingsScreen(Screen):
    flavour = StringProperty(CustomFlavour)

    def save_settings(self):
        if self.flavour:
            with open('config.txt', 'w') as file:
                file.write(self.flavour)

with open('config.txt', 'r') as file:
    CustomFlavour = file.read().strip()
if CustomFlavour != "":
	AndroidFlavour = CustomFlavour
else:
	AndroidFlavour = AndroidFlavour

kv = """
ScreenManager:
    id: screen_manager
    MainScreen:
    SettingsScreen:

<RoundedButton>:
    canvas.before:
        Color:
            rgb: {'normal': self.color_normal, 'down': self.color_down}[self.state]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [30]
<RoundedNonButton>:
    canvas.before:
        Color:
            rgb: {'normal': self.color_normal, 'down': self.color_down}[self.state]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [30]

<MainScreen>:
    name: "main"
    FloatLayout:
    RoundedButton:
        text: app.button_title
        size_hint: None, None
        size: dp(300), dp(50)
        pos_hint: {'x': 0.05, 'y': 0.92}
        font_size: '20sp'
        on_press: app.secret_title(self)
    RoundedButton:
        text: app.button0_text
        size_hint: None, None
        size: dp(300), dp(300)
        font_size: '30sp'
        pos_hint: {'x': 0.14, 'y': 0.55}
    RoundedButton:
        text: app.button1_text
        size_hint: None, None
        size: dp(150), dp(100)
        pos_hint: {'x': 0.1, 'y': 0.4}
    RoundedButton:
        text: app.button2_text
        size_hint: None, None
        size: dp(150), dp(100)
        pos_hint: {'x': 0.55, 'y': 0.4}
    RoundedButton:
        text: app.button3_text
        size_hint: None, None
        size: dp(150), dp(100)
        pos_hint: {'x': 0.55, 'y': 0.25}
    RoundedButton:
        text: app.button4_text
        size_hint: None, None
        size: dp(150), dp(100)
        pos_hint: {'x': 0.1, 'y': 0.25}
    RoundedButton:
        text: app.button5_text
        size_hint: None, None
        size: dp(150), dp(100)
        pos_hint: {'x': 0.1, 'y': 0.1}
    RoundedButton:
        text: app.button6_text
        size_hint: None, None
        size: dp(150), dp(100)
        pos_hint: {'x': 0.55, 'y': 0.1}
        
    RoundedButton:
   	 text: '⚙'
   	 font_name: 'NotoEmojis'
        size_hint: None, None
        size: dp(50), dp(50)
        pos_hint: {'x': 0.8, 'y': 0.92}
        font_size: '20sp'
        on_release:
            app.root.transition.direction = "left"
            app.root.current = "settings"
            
<SettingsScreen>:
    name: "settings"
    FloatLayout:
        RoundedNonButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.7}
        Label:
            text: "Custom android flavour:"
            pos_hint: {'x': 0.08, 'y': 0.73}
            size_hint: None, None
            size: dp(150), dp(50)
            font_size: '18sp'
        RoundedButton:
            text: "Save and Go Back"
            size_hint: None, None
            size: dp(320), dp(60)
            pos_hint: {'x': 0.1, 'y': 0.1}
            font_size: '20sp'
            on_release:
                root.save_settings()
                app.root.transition.direction = "right"
                app.root.current = "main"
        TextInput:
            id: flavour
            text: root.flavour
            multiline: False
            size_hint: None, None
            size: dp(150), dp(50)
            pos_hint: {'x': 0.45, 'y': 0.73}
            on_text_validate: root.flavour = self.text
        RoundedButton:
            size_hint: None, None
            size: dp(25), dp(25)
            pos_hint: {'x': 0.88, 'y': 0.78}
            text: "×"
            font_size: '30sp'
            on_press: app.wipe_custom_flavour(self)
"""

class RoundedButton(ButtonBehavior, Label):
    color_normal = ColorProperty([0.2, 0.2, 0.2, 0.2])
    color_down = ColorProperty([0.4, 0.4, 0.4, 0.2])
    text = StringProperty('')
    
class RoundedNonButton(ButtonBehavior, Label):
    color_normal = ColorProperty([0.2, 0.2, 0.2, 0.2])
    color_down = ColorProperty([0.2, 0.2, 0.2, 0.2])
    text = StringProperty('')

class AndroidFetch(App):
    button_title = StringProperty(f"AndroidFetch v0.4")
    button0_text =StringProperty(f"Android {AndroidInfo} \n{AndroidFlavour} \nSDK {SDKInfo}")
    button1_text = StringProperty(f"Bootloader Status: {BootloaderInfo} \n{KnoxVersion}")
    button2_text = StringProperty(f"VNDK Version: {VNDKInfo} \nKernel Version: {KernelInfo}")
    button3_text = StringProperty(f"Phone: {ModelName} \nManufactorer: {PhoneMaker}")
    button4_text = StringProperty(f"CPU: {CPUInfo} \nArch: {ArchInfo}")
    button5_text = StringProperty(f"Language: {Languege} \nTime Zone: {TimeZone}")
    button6_text = StringProperty(f"HDR: {HDRInfo} \nWide Colour: {WideColourInfo} \nVariable FPS: {VariableFPS}")
        
    def secret_title(self, instance):
        global ButtonPressNum
        ButtonPressNum += 1
        if ButtonPressNum > 4:
            self.button_title = "AndroidFetch v0.4 - Made by cocobo1 :)"

    def wipe_custom_flavour(self, instance):
        with open("config.txt", "r") as file:
            lines = file.readlines()
            if lines:
                lines[0] = "\n"
        with open("config.txt", "w") as file:
             file.writelines(lines)

    def build(self):
        return Builder.load_string(kv)

AndroidFetch().run()