import os
import time

def start_fake_ap():
    # Устанавливаем интерфейс в режим монитора (если еще не в нем)
    os.system("ip link set wlan0 down")
    os.system("ip link set wlan0 up")
    os.system("iw dev wlan0 set type monitor")

    # Настроим точку доступа с помощью hostapd
    hostapd_config = """
    interface=wlan0
    driver=nl80211
    ssid=FakeAP
    channel=6
    hw_mode=g
    wpa=2
    wpa_passphrase=FakePassword123
    """
    with open("hostapd.conf", "w") as file:
        file.write(hostapd_config)

    # Запускаем точку доступа
    os.system("hostapd hostapd.conf &")

    # Настроим DNS и DHCP сервер с помощью dnsmasq
    dnsmasq_config = """
    interface=wlan0
    dhcp-range=192.168.1.50,192.168.1.150,12h
    dhcp-option=3,192.168.1.1
    dhcp-option=6,8.8.8.8
    """
    with open("dnsmasq.conf", "w") as file:
        file.write(dnsmasq_config)

    # Запускаем dnsmasq
    os.system("dnsmasq -C dnsmasq.conf &")

    print("Fake Access Point started with SSID: FakeAP")

if __name__ == "__main__":
    start_fake_ap()
    time.sleep(60)  # Держим точку доступа включенной в течение 60 секунд
    os.system("pkill hostapd")
    os.system("pkill dnsmasq")
    print("Fake Access Point stopped.")
