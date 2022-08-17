import schedule
import time
import psutil
import subprocess

def trading_system_job():
    subprocess.Popen(["python", "./../trading_system.py"])
    print("trading system started by job scheduler")


def trading_system_shutdown_job():
    PROCNAME = "trading_system.py"
    for proc in psutil.process_iter():
        # check whether the process name matches
        try:
            cmdline = proc.cmdline()
            for arg in cmdline:
                if PROCNAME in arg:
                    print("killing:")
                    print(proc)
                    proc.kill()
        except:
            print("can no get process due to permission")
    print("trading system shut down by scheduler")


schedule.every().monday.at("09:05").do(trading_system_job)
schedule.every().tuesday.at("09:05").do(trading_system_job)
schedule.every().wednesday.at("09:05").do(trading_system_job)
schedule.every().thursday.at("09:05").do(trading_system_job)
schedule.every().friday.at("09:05").do(trading_system_job)

schedule.every().monday.at("16:00").do(trading_system_shutdown_job)
schedule.every().tuesday.at("16:00").do(trading_system_shutdown_job)
schedule.every().wednesday.at("16:00").do(trading_system_shutdown_job)
schedule.every().thursday.at("16:00").do(trading_system_shutdown_job)
schedule.every().friday.at("16:00").do(trading_system_shutdown_job)


while 1:
    schedule.run_pending()
    time.sleep(10)
