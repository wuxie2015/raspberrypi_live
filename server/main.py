#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
import string
import ctypes
import datetime
import logging
from logging.handlers import RotatingFileHandler

class Daemon(object):
    def __init__(self, name, runCmd, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.findCmd = 'ps -fe |grep ' + name + ' | grep -v grep | wc -l'
        self.runCmd = runCmd
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.logger = self.logger_init()

    def logger_init(self):
        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        log_file = 'raspberrypi.log'
        Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
        Rthandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(Rthandler)
        logger.setLevel(logging.DEBUG)
        return logger

    def daemonize(self):
        try:
            # fork 生成子进程脱离父进程，成为init进程的子进程
            if os.fork() > 0:#错误
                raise SystemExit(0)#退出主进程
        except OSError as e:
            self.logger.error("fork #1 failed")
            raise RuntimeError('fork #1 faild: {0} ({1})\n'.format(e.errno, e.strerror))
        #setsid该方法做一系列的事：首先它使得该进程成为一个新会话的领导者，接下来它将进程转变一个新进程组的领导者
                    #最后该进程不再控制终端, 运行的时候，建立一个进程，linux会分配个进程号。然后调用os.fork()创建子进程。若pid>0就是自己，自杀。子进程跳过if语句，通过os.setsid()成为linux中的独立于终端的进程（不响应sigint，sighup等）。
        os.setsid()#设置新的会话连接 sid = session id 生成一个新的session
        os.umask(0)#重新设置文件创建权限
        try:
            if os.fork() > 0:
                if os.fork() > 0:  # 错误
                    raise SystemExit(0)  # 退出主进程
        except OSError as e:
            self.logger.error("fork #2 failed")
            raise RuntimeError('fork #2 faild: {0} ({1})\n'.format(e.errno, e.strerror))
        os.chdir("/")  # 修改工作目录
        # Flush I/O buffers
        sys.stdout.flush()
        sys.stderr.flush()

        # Replace file descriptors for stdin, stdout, and stderr
        with open(self.stdin, 'rb', 0) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())#os.dup2() 方法用于将一个文件描述符 fd 复制到另一个 fd2。
        with open(self.stdout, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(self.stderr, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        return

    def start(self):
        # 检查pid文件是否存在以探测是否存在进程
        esb = os.popen(self.findCmd).read().strip()
        if not (esb == '0'):
            print("the deamon is already running!!!")
            return
        else:
            # 启动监控
            self.daemonize()
            self.run()

    def run(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        while True:
            try:
                esb = os.popen(self.findCmd).read().strip()
                if (esb == '0'):
                    self.logger.info("deamon on  %s" % now)
                    os.system(self.runCmd)
            except:
                pass
            time.sleep(10)

    def KillPid(self, name):
        ps_str = 'ps aux |grep ' + name + ' | grep -v grep'
        x = os.popen(ps_str).read()
        if x:
            proc = x.split('\n')
            for line in proc:
                print(line)
                try:
                    proc_id = line.split()[1]
                    os.system('kill -9 %s' % proc_id)
                except:
                    pass
        else:
            return

    def checkpid(self, name):
        findCmd = 'ps -fe |grep ' + name + ' | grep -v grep | wc -l'
        esb = os.popen(findCmd).read().strip()
        if not (esb == '0'):
            # 杀进程
            try:
                self.KillPid(name)
            except:
                print("kill %s failed!!!" % name)
                self.logger.error("the deamon  %s  kill failed" % name)
                return
        return

    def stop(self):
        self.checkpid('main.py')
        self.checkpid('deamon.py')
        return

    def restart(self):
        self.stop()
        self.start()

def watch_dog(name,run_cmd):
    ps_str = 'ps -fe |grep ' + name + ' | grep -v grep | wc -l'
    esb = os.popen(ps_str).read().strip()
    if esb == '0':
        # 重启或启动
        daemon_obj = Daemon(name,run_cmd)
        daemon_obj.start()

def start_all():
    name_dict = {
        'socket_server.py':'python /usr/local/project/raspberrypi_video/server/socket_server.py',
        'scan_file.py':'python /usr/local/project/raspberrypi_video/server/scan_file.py'
        # 'watchdog_scan_file.py':'python /usr/local/project/raspberrypi_video/server/watchdog_scan_file.py',
        # 'watchdog_socket_server.py': 'python /usr/local/project/raspberrypi_video/server/watchdog_scan_file.py'
                 }
    daemon_list = []
    for k in name_dict:
        log_name = k.split('.')[0] + '.log'
        daemon_list.append(
            Daemon(k, name_dict[k], stdout=log_name, stderr=log_name)
        )
    for daemon in daemon_list:
        daemon.start()

def stop_all():
    name_dict = {
        'socket_server.py':'python /usr/local/project/raspberrypi_video/server/socket_server.py',
        'scan_file.py':'python /usr/local/project/raspberrypi_video/server/scan_file.py',
        'watchdog_scan_file.py':'python /usr/local/project/raspberrypi_video/server/watchdog_scan_file.py',
        'watchdog_socket_server.py': 'python /usr/local/project/raspberrypi_video/server/watchdog_scan_file.py'
                 }
    daemon_list = []
    for k in name_dict:
        log_name = k.split('.')[0] + '.log'
        daemon_list.append(
            Daemon(k, name_dict[k], stdout=log_name, stderr=log_name)
        )
    for daemon in daemon_list:
        daemon.stop()


if __name__ == "__main__":
    start_all()
    # if len(sys.argv) != 1:
    #     print('Usage: [start|stop]')
    #     raise SystemExit(1)
    # if 'start' == sys.argv[0]:
    #     start_all()
    # elif 'stop' == sys.argv[0]:
    #     stop_all()
    # else:
    #     print('Unknown command {0}'.format(sys.argv[1]))
    #     raise SystemExit(1)
