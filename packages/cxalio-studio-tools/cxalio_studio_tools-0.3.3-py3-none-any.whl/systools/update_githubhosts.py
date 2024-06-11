import os
import urllib.request
from argparse import ArgumentParser

from rich_argparse import RichHelpFormatter

from cx_core import DataPackage
from cx_core.app import OSInfo, AbstractApp
from .env import env


class GithubHostsUpdaterApp(AbstractApp):
    URL = "https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts"

    APP_NAME = 'update_githubhosts'
    APP_VERSION = '0.1.10'

    def __init__(self):
        super(GithubHostsUpdaterApp, self).__init__()
        self.osinfo = OSInfo()
        parser = ArgumentParser(prog=GithubHostsUpdaterApp.APP_NAME, formatter_class=RichHelpFormatter,
                                description='自动更新githubhosts', epilog='Designed by xiii_1991')
        parser.add_argument('-p', '--pretend', action='store_true', dest='pretend',
                            help='模拟执行并输出结果')
        parser.add_argument('-s', '--save', action='append', dest='side_save', metavar='PATH',
                            help='输出到指定位置')
        parser.add_argument('--version', action='version', version=GithubHostsUpdaterApp.APP_VERSION,
                            help="显示版本号")
        self._parser = parser
        self.status = None
        self.args = None

    def refresh_dns(self):
        self.status.update('尝试刷新DNS...')
        if self.osinfo.system == 'Darwin':
            os.system("killall -HUP mDNSResponder")
            env.print('杀死 mDNSResponder')
        elif self.osinfo.system == 'Linux':
            os.system("systemctl restart systemd-resolved")
            env.print('重启网络服务')
        elif self.osinfo.system == 'Windows':
            os.system("ipconfig /flushdns")
            env.print('刷新 DNS 信息')
        else:
            env.warning('无法识别操作系统，请手动刷新')

    def __enter__(self):
        self.status = env.console.status('正在启动...')
        env.print(f'[yellow]{GithubHostsUpdaterApp.APP_NAME}[/yellow] [blue]{GithubHostsUpdaterApp.APP_VERSION}[/blue]')
        self.args = DataPackage(**vars(self._parser.parse_args()))
        self.status.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.status.update('执行完毕')
        self.status.stop()
        return False

    def run(self):
        self.status.update('正在下载新的hosts...')
        local_filename, headers = urllib.request.urlretrieve(self.URL)
        env.print("已下载新的 Github Hosts")

        self.status.update('开始解析...')
        github_hosts = []
        with open(local_filename, encoding='utf-8') as new_hosts:
            for line in new_hosts:
                github_hosts.append(line)

        old_hosts = []
        with open(self.osinfo.hosts_file, encoding='utf-8') as host_file:
            inside_github_section = False
            for line in host_file:
                if line == github_hosts[0]:
                    inside_github_section = True
                    continue
                if line == github_hosts[-1]:
                    inside_github_section = False
                    continue
                if not inside_github_section:
                    old_hosts.append(line)

        env.print('解析完毕')

        if self.args.pretend:
            self.status.update('正在预览结果...')
            env.print(''.join(old_hosts + github_hosts))
            return

        self.status.update('正在写入...')
        target = self.osinfo.hosts_file
        if self.args.side_save:
            target = self.args.side_save[0]
            env.print(f'修改输出目标为 {target}')

        with open(target, "w", encoding='utf-8') as new_host:
            new_host.writelines(old_hosts)
            new_host.writelines(github_hosts)
            env.print('写入完毕。')

        self.refresh_dns()


def run():
    with GithubHostsUpdaterApp() as app:
        app.run()
