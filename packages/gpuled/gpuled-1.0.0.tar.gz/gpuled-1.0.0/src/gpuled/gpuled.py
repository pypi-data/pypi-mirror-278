import psutil
import pynvml
UNIT = 1024 * 1024

def main():
    pynvml.nvmlInit() #初期化
    gpuDeriveInfo = pynvml.nvmlSystemGetDriverVersion()
    print("Drive device: ", str(gpuDeriveInfo)) #Drive device を確認

    gpuDeviceCount = pynvml.nvmlDeviceGetCount() #Nvidia カードを数える
    print("GPU 数:", gpuDeviceCount )
    handle = pynvml.nvmlDeviceGetHandleByIndex(0) #GPU 0 を扱う

    memoryInfo = pynvml.nvmlDeviceGetMemoryInfo(handle) #handle 处理

    gpuName = str(pynvml.nvmlDeviceGetName(handle)) #名前
    print("GPU 名:", gpuName)
    import pyfirmata
    from time import sleep
    b=pyfirmata.Arduino('COM5')
    #i=pyfirmata.util.Iterator(b)
    while True:
    gpuTemperature = pynvml.nvmlDeviceGetTemperature(handle, 0)
    print("温度:", gpuTemperature, "度")
    t = 45/gpuTemperature
    cycle1 = t**9 #GPU 温度によってピカピカの周期を決める
    b.digital[9].write(1)
    sleep(cycle1)
    b.digital[9].write(0)
    sleep(cycle1)
    if gpuTemperature<50: #50 度以下のとき LED2が点灯
    b.digital[2].write(1)
    b.digital[3].write(0)
    else: #ほかの場合 LED3が点灯
    b.digital[2].write(0)
    b.digital[3].write(1)
    # b.analog[0].read()

if __name__ == '__main__':
    main()