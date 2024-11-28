# Made by cocobo1


import subprocess

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

OneUiVersion = GetProp("ro.build.version.oneui")
OneUiVersion = OneUiVersion.replace("0", ".")
OneUiVersion = OneUiVersion.replace("..", "")
if OneUiVersion != "":
	AndroidFlavour = "OneUi " + OneUiVersion
if PhoneMaker == "samsung":
	KnoxVersion = GetProp("net.knoxvpn.version")

# file1 = open('ASCII.json', 'r')
# Lines = file1.readlines()[3:15]
# print(Lines)

print("Android version: ", AndroidInfo)
print("SDK version: ", SDKInfo)
print("Phone Model: ", ModelName)
print("Android Flavour: ", AndroidFlavour)
print("Kernel Version: ", KernelInfo)
print("VNDK Version: ", VNDKInfo)
print("Bootloader Status: ", BootloaderInfo)
print("CPU Architecture: ", Archinfo)
if KnoxVersion != "":
	print("Knox Version: ", KnoxVersion)
print("Languege: ", Languege)
print("TimeZone: ", TimeZone)
print("Manufactorer: ", PhoneMaker)






