# Made by cocobo1

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ColorProperty, StringProperty


import subprocess
import psutil
import GPUtil
import platform

def GetProp(Prop):
    result = subprocess.run(f"getprop {Prop}", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {Prop} not found or failed to execute."

ButtonPressNum = 0
TitleSecret = ""

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





kv = """
<RoundedButton>:
    canvas.before:
        Color:
            rgb: {'normal': self.color_normal, 'down': self.color_down}[self.state]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [30]

FloatLayout:
    RoundedButton:
        text: app.button_title
        size_hint: None, None
        size: dp(410), dp(50)
        pos_hint: {'x': 0, 'y': 0.95}
        font_size: '20sp'
        on_press: app.on_press(self)
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
"""

class RoundedButton(ButtonBehavior, Label):
    color_normal = ColorProperty('grey')
    color_down = ColorProperty([0.8, 0.8, 0.8, 1])
    text = StringProperty('')

if ButtonPressNum > 4:
	TitleSecret = " - Made by cocobo1 :)"

class AndroidFetch(App):
    button_title = StringProperty(f"AndroidFetch v0.3 {TitleSecret}")
    button0_text =StringProperty(f"Android {AndroidInfo} \n{AndroidFlavour} \nSDK {SDKInfo}")
    button1_text = StringProperty(f"Bootloader Status: {BootloaderInfo} \nKnox Version: {KnoxVersion}")
    button2_text = StringProperty(f"VNDK Version: {VNDKInfo} \nKernel Version: {KernelInfo}")
    button3_text = StringProperty(f"Phone: {ModelName} \nManufactorer: {PhoneMaker}")
    button4_text = StringProperty(f"CPU: {CPUInfo} \nArch: {ArchInfo}")
    button5_text = StringProperty(f"Language: {Languege} \nTime Zone: {TimeZone}")
    button6_text = StringProperty(f"HDR: {HDRInfo} \nWide Colour: {WideColourInfo} \nVariable FPS: {VariableFPS}")
        
    def on_press(self, instance):
        global ButtonPressNum
        ButtonPressNum += 1
        if ButtonPressNum > 4:
            self.button_title = "AndroidFetch v0.3 - Made by cocobo1 :)"

    def build(self):
        return Builder.load_string(kv)

AndroidFetch().run()