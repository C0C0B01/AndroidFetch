# Made by cocobo1

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

import subprocess
import psutil
import GPUtil
import platform
import cpuinfo

def GetProp(Prop):
    result = subprocess.run(f"getprop {Prop}", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {Prop} not found or failed to execute."



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
Archinfo = GetProp("ro.product.cpu.abi")
CPUInfo = platform.processor
# open("/proc/cpuinfo")
# CPUInfo = file.read()
GPUInfo = "Not working currently"

OneUiVersion = GetProp("ro.build.version.oneui")
OneUiVersion = OneUiVersion.replace("0", ".")
OneUiVersion = OneUiVersion.replace("..", "")
if OneUiVersion != "":
	AndroidFlavour = "OneUi " + OneUiVersion
if PhoneMaker == "samsung":
	KnoxVersion = GetProp("net.knoxvpn.version")






class MyApp(App):
    def build(self):

        scroll_view = ScrollView()
        layout = FloatLayout()
        
        title = Button(
            text=f'AndroidFetch',
            size_hint=(None, None),
            size=(1100, 200),
            pos=(-15, 2100),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
         )
        layout.add_widget(title)
        
        button0 = Button(
            text=f' Android {AndroidInfo} \n {AndroidFlavour} \n SDK Version {SDKInfo}',
            size_hint=(None, None),
            size=(800, 600),
            pos=(140, 1400),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
         )
        layout.add_widget(button0)
        
        button1 = Button(
            text=f' Languege: {Languege} \n Time Zone: {TimeZone}',
            size_hint=(None, None),
            size=(400, 300),
            pos=(50, 550),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
         )
        layout.add_widget(button1)
        
        button2 = Button(
            text=f'Phone: {ModelName}',
            size_hint=(None, None),
            size=(400, 300),
            pos=(625, 550),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
            )
        layout.add_widget(button2)
        
        button3 = Button(
            text=f' Bootloader status: {BootloaderInfo} \n Knox Version: {KnoxVersion}',
            size_hint=(None, None),
            size=(400, 300),
            pos=(625, 950),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
            )
        layout.add_widget(button3)
        
        button4 = Button(
            text=f' VNDK Version: {VNDKInfo} \n Kernel Version: {KernelInfo}',
            size_hint=(None, None),
            size=(400, 300),
            pos=(50, 950),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
            )
        layout.add_widget(button4)

        button5 = Button(
            text=f'I need more stuff',
            size_hint=(None, None),
            size=(400, 300),
            pos=(50, 150),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
         )
        layout.add_widget(button5)
        
        button6 = Button(
            text=f' CPU: {CPUInfo} \n Arch: {Archinfo} \n GPU: {GPUInfo}',
            size_hint=(None, None),
            size=(400, 300),
            pos=(625, 150),
            background_normal='',
            background_down='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            )
        layout.add_widget(button6)
        
        scroll_view.add_widget(layout)

        return scroll_view
        
if __name__ == '__main__':
    MyApp().run()