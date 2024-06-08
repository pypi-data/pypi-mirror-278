import os
import re
from pathlib import Path
import pyshark
from serialization_utils import Serializer


class BlockJetBrains:
    def __init__(self, interface: str):
        self.interface = interface

    @staticmethod
    def _extract_substring(string: str, search_string: str):
        result = []
        start = 0
        while True:
            index = string.find(search_string, start)
            if index == -1:
                break
            # extract the search string until to the \n
            end_index = string.find('\n', index)
            if end_index == -1:
                end_index = len(string)
            substring = string[index + len(search_string):end_index].strip()
            result.append(substring)
            start = end_index + 1
        return result

    @staticmethod
    def _p_os_system(command: str) -> None:
        print(command)
        os.system(command)

    def _flush_dns(self):
        self._p_os_system('ipconfig /flushdns')

    @staticmethod
    def _remove_ansi_escapes(text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def append_dns_ip(self):
        self._flush_dns()
        s = Serializer(Path(__file__), data_type=dict, embedded=True)
        current_ip_dict = s.load_json()
        print(current_ip_dict)
        capture_filter = 'dns'
        capture = pyshark.LiveCapture(interface=self.interface, display_filter=capture_filter)
        capture.sniff(timeout=1)

        print('Start capture')
        for packet in capture.sniff_continuously():
            has_added = False
            content = self._remove_ansi_escapes(str(packet))
            if 'Standard query response' in content:
                name_list = self._extract_substring(content, 'Name: ')
                name = None
                if name_list:
                    name = name_list[0]
                ip_result = self._extract_substring(content, ' addr ')
                print(f'{name}: {ip_result}')
                if name in ['www.jetbrains.com', 'account.jetbrains.com']:
                    for ip in ip_result:
                        if not current_ip_dict.get(name):
                            current_ip_dict[name] = []
                        current_ip_list = current_ip_dict[name]
                        if ip not in current_ip_list:
                            current_ip_list.append(ip)
                            print(f'Appended: {ip}')
                            has_added = True
                    if has_added:
                        s.dump_json(current_ip_dict)

                        rule_name = 'jetbrains'
                        total_ip_list = []
                        for ip_list in current_ip_dict.values():
                            total_ip_list.extend(ip_list)
                        self._p_os_system(f'netsh advfirewall firewall delete rule name="{rule_name}"')
                        self._p_os_system(f'netsh advfirewall firewall add rule name="{rule_name}" '
                                          f'dir=out action=block remoteip={",".join(total_ip_list)}')
                        self._p_os_system(f'netsh advfirewall firewall add rule name="{rule_name}" '
                                          f'dir=in action=block remoteip={",".join(total_ip_list)}')
                        self._flush_dns()
        capture.close()


if __name__ == '__main__':
    interface_name = 'WLAN'
    BlockJetBrains(interface_name).append_dns_ip()

"""2qIgKf9iDsVrsTMS
{
    "www.jetbrains.com": [
        "13.225.183.89",
        "13.225.183.104",
        "13.225.183.35",
        "13.225.183.60",
        "65.8.161.4",
        "65.8.161.125",
        "65.8.161.122",
        "65.8.161.71",
        "108.138.85.120",
        "108.138.85.118",
        "108.138.85.7",
        "108.138.85.106",
        "216.137.39.88",
        "216.137.39.118",
        "216.137.39.11",
        "216.137.39.60",
        "18.66.102.125",
        "18.66.102.36",
        "18.66.102.54",
        "18.66.102.75",
        "108.156.133.13",
        "108.156.133.59",
        "108.156.133.65",
        "108.156.133.6"
    ],
    "account.jetbrains.com": [
        "76.223.63.197",
        "13.248.188.196",
        "108.128.182.4",
        "34.248.135.53"
    ]
}
2qIgKf9iDsVrsTMS"""