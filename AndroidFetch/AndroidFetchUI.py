from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ColorProperty, StringProperty, BooleanProperty
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex

import subprocess
import webbrowser
import ast
from functools import lru_cache

ButtonPressNum = 0
TitleSecret = ""
CustomFlavour = ""
CustomCPUName = ""
CustomButtonColour = ""
PickedFont = ""

@lru_cache(maxsize=None)
def GetProp(Prop):
    result = subprocess.run(f"getprop {Prop}", shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else f"Error: {Prop} not found or failed to execute."

SDKInfo = GetProp("ro.build.version.sdk")
AndroidInfo = GetProp("ro.build.version.release")
ModelName = GetProp("ro.product.model")
VNDKInfo = GetProp("ro.vndk.version")
KernelInfo = GetProp("ro.kernel.version")
BootloaderInfo = GetProp("sys.oem_unlock_allowed")
BootloaderInfo = "Unlocked" if BootloaderInfo == "1" else "Locked"
SELinux = GetProp("ro.boot.selinux")
Language = GetProp("persist.sys.locale")
TimeZone = GetProp("persist.sys.timezone")
KnoxVersion = ""
AndroidFlavour = "Unknown"
PhoneMaker = GetProp("ro.product.brand")
ArchInfo = GetProp("ro.product.cpu.abi")
CPUInfo = GetProp("ro.hardware")
CPUMaker = GetProp("ro.hardware.egl")
HDRInfo = GetProp("ro.surface_flinger.has_HDR_display")
HDRInfo = "supported" if HDRInfo == "true" else "unsupported"
WideColourInfo = GetProp("ro.surface_flinger.has_wide_color_display")
WideColourInfo = WideColourInfo.replace("true", "supported")
WideColourInfo = WideColourInfo.replace("false", "unsupported")
VariableFPS = GetProp("ro.surface_flinger.use_content_detection_for_refresh_rate")
VariableFPS = VariableFPS.replace("true", "supported")
VariableFPS = VariableFPS.replace("false", "unsupported")
if PhoneMaker == "samsung":
	KnoxVersion = GetProp("net.knoxvpn.version")
	KnoxVersion = "\nKnox Version: " + KnoxVersion
	OneUiVersion = GetProp("ro.build.version.oneui")
	OneUiVersion = OneUiVersion.replace("0", ".")
	OneUiVersion = OneUiVersion.replace("..", "")
	AndroidFlavour = "OneUi " + OneUiVersion
	
AndroidIcon = "Icons/Android/" + AndroidInfo + ".png"   
with open("config.txt", "r") as file:
    lines = file.readlines()
if lines:
    if len(lines) > 7 and lines[7].strip():
        AndroidIcon = lines[7].strip()
    else:
        lines.append(AndroidIcon)

class MainScreen(Screen):
    AndroidIconShow = StringProperty(AndroidIcon)

class SettingsScreen(Screen):
    pass
            
class SettingsSubStyleScreen(Screen):
    pass
    
class SettingsSubNameScreen(Screen):
    flavour = StringProperty(CustomFlavour)
    cpu_name = StringProperty(CustomCPUName)
    def save_config_name(self):
        try:
            with open("config.txt", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = [""] * 13
        except Exception as e:
            print(f"Error reading config file: {e}")
            lines = [""] * 13
        
        if self.flavour:
            lines[1] = f"{self.flavour}\n"
        if self.cpu_name:
            lines[3] = f"{self.cpu_name}\n"
        with open("config.txt", "w") as file:
            file.writelines(lines)
            
class SettingsStyleScreen(Screen):
    TextColour = ColorProperty([1, 1, 1, 1])
    ButtonColour = ColorProperty([0.2, 0.2, 0.2, 0.2])
    ButtonDownColour = ColorProperty([0.4, 0.4, 0.4, 0.4])
    BackgroundColour = ColorProperty([0, 0, 0, 0])

    def save_config_theme(self):
        with open("config.txt", "r") as file:
            lines = file.readlines()

        if self.ButtonColour:
            lines[9] = str(self.ButtonColour)
        with open("config.txt", "w") as file:
            file.writelines(lines)

    def on_color_pick(self, instance, value):
        r, g, b, a = value
        self.selected_color_hex = "#{:02x}{:02x}{:02x}".format(
            int(r * 255), int(g * 255), int(b * 255))
        self.ButtonColour = [r, g, b, a]
        
def get_color_stuff(CustomButtonColour):
    r = int(CustomButtonColour[0] * 255)
    g = int(CustomButtonColour[1] * 255)
    b = int(CustomButtonColour[2] * 255)
    a = int(CustomButtonColour[3] * 255)
    CustomButtonColour = f'#{r:02X}{g:02X}{b:02X}{a:02X}'

class FontPickerScreen(Screen):
    def select_font(self, selection):
        app = App.get_running_app()
        if selection:
            app.PickedFont = selection[0] 
            try:
                with open("config.txt", "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                lines = ["\n"] * 13
            except Exception as e:
                print(f"Error reading config file: {e}")
                lines = ["\n"] * 13
            lines[5] = f"{app.PickedFont}\n"
            try:
                with open("config.txt", "w") as file:
                    file.writelines(lines)
                print(f"Font '{app.PickedFont}' successfully written to config.txt")
            except Exception as e:
                print(f"Error writing to config file: {e}")
                
class IconPickerScreen(Screen):
    def select_icon(self, selection):
        app = App.get_running_app()
        if selection:
            app.PickedIcon = selection[0] 
            try:
                with open("config.txt", "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                lines = ["\n"] * 13
            except Exception as e:
                print(f"Error reading config file: {e}")
                lines = ["\n"] * 13
            lines[7] = f"{app.PickedIcon}\n"
            try:
                with open("config.txt", "w") as file:
                    file.writelines(lines)
                print(f"Font '{app.PickedFont}' successfully written to config.txt")
            except Exception as e:
                print(f"Error writing to config file: {e}")
            
class SettingsAboutScreen(Screen):
	pass
	
with open('config.txt', 'r') as file:
    lines = file.readlines()
    CustomFlavour = lines[1].strip()
    CustomCPUName = lines[3].strip()
    CustomButtonColour = str(get_color_stuff(ast.literal_eval(lines[9].strip()))) if lines[9] != "" else [0.2, 0.2, 0.2, 1]

if CustomFlavour != "":
	AndroidFlavour = CustomFlavour
if CustomCPUName != "":
	CPUInfo = CustomCPUName
if CustomButtonColour != "":
	ButtonColour = CustomButtonColour

Font = "Fonts/NotoSans-Regular.ttf"
with open("config.txt", "r") as file:
    lines = file.readlines()
if lines:
    if len(lines) > 5 and lines[5].strip():
        Font = lines[5].strip()
    else:
        lines.append(Font)

LabelBase.register(name="Default", fn_regular=Font)
LabelBase.register(name="NotoEmojis", fn_regular="Fonts/NotoEmoji-Regular.ttf")

class RoundedButton(ButtonBehavior, Label):
    colour_normal = ButtonColour
    colour_down = ButtonColour
    text = StringProperty('')
    
class RoundedNonButton(ButtonBehavior, Label):
    colour_normal = ButtonColour
    colour_down = ButtonColour
    text = StringProperty('')

kv = """
ScreenManager:
    id: screen_manager
    MainScreen:
    SettingsScreen:
    SettingsAboutScreen:
    SettingsStyleScreen:
    SettingsSubNameScreen:
    FontPickerScreen:
    IconPickerScreen:

<RoundedButton>:
    canvas.before:
        Color:
            rgb: {'normal': self.colour_normal, 'down': self.colour_down}[self.state]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [30]
            
<RoundedNonButton>:
    canvas.before:
        Color:
            rgb: {'normal': self.colour_normal, 'down': self.colour_down}[self.state]
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
        font_name: "Default"
        font_size: '20sp'
        on_press: app.secret_title(self)
    Image:
        source: root.AndroidIconShow
        size: dp(250), dp(250)
        size_hint: None, None
        pos_hint: {'x': 0.2, 'y': 0.58}
    RoundedButton:
        text: app.button1_text
        size_hint: None, None
        size: dp(150), dp(100)
        font_name: "Default"
        font_size: '16sp'
        pos_hint: {'x': 0.1, 'y': 0.4}
    RoundedButton:
        text: app.button2_text
        size_hint: None, None
        size: dp(150), dp(100)
        font_name: "Default"
        pos_hint: {'x': 0.55, 'y': 0.4}
    RoundedButton:
        text: app.button3_text
        size_hint: None, None
        size: dp(150), dp(100)
        font_name: "Default"
        pos_hint: {'x': 0.55, 'y': 0.25}
    RoundedButton:
        text: app.button4_text
        size_hint: None, None
        size: dp(150), dp(100)
        font_name: "Default"
        pos_hint: {'x': 0.1, 'y': 0.25}
    RoundedButton:
        text: app.button5_text
        size_hint: None, None
        size: dp(150), dp(100)
        font_name: "Default"
        pos_hint: {'x': 0.1, 'y': 0.1}
    RoundedButton:
        text: app.button6_text
        font_name: "Default"
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
        RoundedButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.2}
            text: "About AndroidFetch"
            font_name: "Default"
            font_size: '18sp'
            on_release:
            	app.root.transition.direction = "left"
            	app.root.current = "settingsabout"
        RoundedButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.8}
            text: "Custom Names"
            font_name: "Default"
            font_size: '18sp'
            on_release:
            	app.root.transition.direction = "left"
            	app.root.current = "settingsname"
        RoundedButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.65}
            text: "Custom Theme"
            font_name: "Default"
            font_size: '18sp'
            on_release:
            	app.root.transition.direction = "left"
            	app.root.current = "settingsstyle"
        RoundedButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.5}
            text: "Custom Fonts"
            font_name: "Default"
            font_size: '18sp'
            on_release:
            	app.root.transition.direction = "left"
            	app.root.current = "font picker"
        RoundedButton:
            size_hint: None, None
            size: dp(25), dp(25)
            pos_hint: {'x': 0.88, 'y': 0.58}
            text: "×"
            font_size: '36sp'
            on_press: app.wipe_custom_font(self)
        RoundedButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.35}
            text: "Custom Version Icon"
            font_name: "Default"
            font_size: '18sp'
            on_release:
            	app.root.transition.direction = "left"
            	app.root.current = "icon picker"
        RoundedButton:
            size_hint: None, None
            size: dp(25), dp(25)
            pos_hint: {'x': 0.88, 'y': 0.43}
            text: "×"
            font_size: '36sp'
            on_press: app.wipe_custom_icon(self)
        RoundedButton:
            size_hint: None, None
            size: dp(25), dp(25)
            pos_hint: {'x': 0.88, 'y': 0.58}
            text: "×"
            font_size: '36sp'
            on_press: app.wipe_custom_icon(self)
        RoundedButton:
            text: "Go Back"
            size_hint: None, None
            size: dp(320), dp(60)
            pos_hint: {'x': 0.11, 'y': 0.1}
            font_name: "Default"
            font_size: '24sp'
            on_release:
                app.root.transition.direction = "right"
                app.root.current = "main"
                
<SettingsSubNameScreen>:
    name: "settingsname"
    FloatLayout:
        RoundedNonButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.8}
        Label:
            text: "Custom android flavour:"
            pos_hint: {'x': 0.08, 'y': 0.83}
            size_hint: None, None
            size: dp(150), dp(50)
            font_name: "Default"
            font_size: '18sp'
	    TextInput:
 		   id: flavour
   		 multiline: False
 		   size_hint: None, None
   		 font_name: "Default"
		    font_size: "36sp"
 		   size: dp(150), dp(50)
            pos_hint: {'x': 0.48, 'y': 0.83}
            on_text: root.flavour = self.text
        RoundedButton:
            size_hint: None, None
            size: dp(25), dp(25)
            pos_hint: {'x': 0.88, 'y': 0.88}
            text: "×"
            font_size: '36sp'
            on_press: app.wipe_custom_flavour(self)
        RoundedNonButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.65}
        Label:
            text: "Custom CPU name:"
            pos_hint: {'x': 0.08, 'y': 0.68}
            size_hint: None, None
            size: dp(150), dp(50)
            font_name: "Default"
            font_size: '18sp'
        TextInput:
            id: cpu_name
            multiline: False
            text: root.cpu_name
            size_hint: None, None
            font_name: "Default"
            font_size: "36sp"
            size: dp(150), dp(50)
            pos_hint: {'x': 0.48, 'y': 0.68}
            on_text_validate: root.cpu_name = self.text 
        RoundedButton:
            size_hint: None, None
            size: dp(25), dp(25)
            pos_hint: {'x': 0.88, 'y': 0.73}
            text: "×"
            font_size: '36sp'
            on_press: app.wipe_custom_cpu_name(self)
        RoundedButton:
            text: "Save and Go Back"
            size_hint: None, None
            size: dp(320), dp(60)
            pos_hint: {'x': 0.11, 'y': 0.1}
            font_name: "Default"
            font_size: '24sp'
            on_release:
                root.save_config_name()
                app.root.transition.direction = "right"
                app.root.current = "settings"
                
<SettingsAboutScreen>:
	name: "settingsabout"
	FloatLayout:
        RoundedButton:
            text: "AndroidFetch is a project developed by cocobo1. It is built on Python and Kivy and aims to give you a detailed overview of your device with a clean UI"
            size_hint: None, None
            size: dp(300), dp(300)
            pos_hint: {'x': 0.13, 'y': 0.5}
            font_name: "Default"
            font_size: '18sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.size
        RoundedButton:
            text: "About AndroidFetch"
            size_hint: None, None
            size: dp(400), dp(60)
            pos_hint: {'x': 0, 'y': 0.944}
            font_name: "Default"
            font_size: '25sp'
            on_release:
                app.root.transition.direction = "right"
                app.root.current = "settings"
        Label:
            text: "⬅"
            pos_hint: {'x': 0.001, 'y': 0.945}
            size_hint: None, None
            size: dp(50), dp(50)
            font_name: "NotoEmojis"
            font_size: '32sp'
        RoundedButton:
            size_hint: None, None
            size: dp(370), dp(100)
            pos_hint: {'x': 0.05, 'y': 0.35}
            text: "AndroidFetch Github"
            font_name: "Default"
            font_size: '18sp'
            on_release: app.open_website("https://github.com/FastCocobo/AndroidFetch")
        Image:
        	source: 'Icons/Textures/Github.png'
        	pos_hint: {'x': 0.1, 'y': 0.375}
        	size_hint: None, None
        	size: dp(60), dp(60)
        	
<FontPickerScreen>:
    name: "font picker"
    FloatLayout:
        FileChooserListView:
            id: filechooser
            filters: ['*.ttf']
            path: "/storage/emulated/0/"
        	pos_hint: {'x': 0, 'y': 0.2}
        	size_hint: None, None
        	size: dp(400), dp(700)
            font_name: "Default"
            font_size: '18sp'
        RoundedButton:
            text: "Use Selected Font"
            on_press: root.select_font(filechooser.selection)
        	pos_hint: {'x': 0.04, 'y': 0.05}
        	size_hint: None, None
        	size: dp(240), dp(80)
            font_name: "Default"
            font_size: '18sp'
        RoundedButton:
            text: "⬅"
            on_release:
                app.root.transition.direction = "right"
                app.root.current = "settings"
        	pos_hint: {'x': 0.65, 'y': 0.05}
        	size_hint: None, None
        	size: dp(100), dp(80)
            font_name: "NotoEmojis"
            font_size: '30sp'
            
<IconPickerScreen>:
    name: "icon picker"
    FloatLayout:
        FileChooserListView:
            id: filechooser
            filters: ['*.png']
            path: "/storage/emulated/0/"
        	pos_hint: {'x': 0, 'y': 0.2}
        	size_hint: None, None
        	size: dp(400), dp(700)
            font_name: "Default"
            font_size: '18sp'
        RoundedButton:
            text: "Use Selected PNG"
            on_press: root.select_icon(filechooser.selection)
        	pos_hint: {'x': 0.04, 'y': 0.05}
        	size_hint: None, None
        	size: dp(240), dp(80)
            font_name: "Default"
            font_size: '18sp'
        RoundedButton:
            text: "⬅"
            on_release:
                app.root.transition.direction = "right"
                app.root.current = "settings"
        	pos_hint: {'x': 0.65, 'y': 0.05}
        	size_hint: None, None
        	size: dp(100), dp(80)
            font_name: "NotoEmojis"
            font_size: '30sp'

<SettingsStyleScreen>:
    name: "settingsstyle"
    FloatLayout:
    	ColorPicker:
    		id: color_picker
    		on_color: root.temp_colour = self.color
        	pos_hint: {'x': 0, 'y': 0.29}
        	size_hint: None, None
        	size: dp(410), dp(600)
        RoundedButton:
            text: "Use for buttons"
            on_press: root.ButtonColour = root.temp_colour
        	pos_hint: {'x': 0.04, 'y': 0.05}
        	size_hint: None, None
        	size: dp(240), dp(80)
            font_name: "Default"
            font_size: '18sp'
        RoundedButton:
            text: "Save and go back"
            on_release:
 		       root.on_color_pick(self, self.color)
                root.save_config_theme()
                app.root.transition.direction = "right"
                app.root.current = "settings"
        	pos_hint: {'x': 0.65, 'y': 0.05}
        	size_hint: None, None
        	size: dp(200), dp(80)
            font_name: "Default"
"""

class AndroidFetch(App):
    button_title = StringProperty(f"AndroidFetch v0.9")
    button1_text = StringProperty(f"Android {AndroidInfo} \n{AndroidFlavour} \nSDK {SDKInfo}")
    button2_text = StringProperty(f"VNDK Version: {VNDKInfo} \nKernel Version: {KernelInfo}")
    button3_text = StringProperty(f"Phone: {ModelName} \nManufactorer: {PhoneMaker}")
    button4_text = StringProperty(f"Bootloader: {BootloaderInfo} {KnoxVersion} \nSELinux: {SELinux}")
    button5_text = StringProperty(f"CPU: {CPUInfo} \nManufactorer: {CPUMaker} \nArch: {ArchInfo}")
    button6_text = StringProperty(f"HDR: {HDRInfo} \nWide Colour: {WideColourInfo} \nVariable FPS: {VariableFPS}")
        
    def secret_title(self, instance):
        global ButtonPressNum
        ButtonPressNum += 1
        if ButtonPressNum > 4:
            self.button_title = "AndroidFetch v0.9 - Made by cocobo1 :)"
             
    def open_website(self, url):
    	webbrowser.open(url)
    	
    def wipe_custom_flavour(self, instance):
        with open("config.txt", "r") as file:
            lines = file.readlines()
            if lines:
                lines[1] = "\n"
        with open("config.txt", "w") as file:
             file.writelines(lines)
    
    def wipe_custom_cpu_name(self, instance):
        with open("config.txt", "r") as file:
            lines = file.readlines()
        if lines:
            lines[3] = "\n"
        with open("config.txt", "w") as file:
             file.writelines(lines)
             
    def wipe_custom_font(self, instance):
        with open("config.txt", "r") as file:
            lines = file.readlines()
        if lines:
            lines[5] = "\n"
        with open("config.txt", "w") as file:
             file.writelines(lines)
             
    def wipe_custom_icon(self, instance):
        with open("config.txt", "r") as file:
            lines = file.readlines()
        if lines:
            lines[7] = "\n"
        with open("config.txt", "w") as file:
             file.writelines(lines)

    def build(self):
        return Builder.load_string(kv)

AndroidFetch().run()