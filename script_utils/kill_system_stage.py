import psutil


def trading_system_shutdown_job():
    PROCNAME = "trading_system.py"
    for proc in psutil.process_iter():
        # check whether the process name matches
        try:
            cmdline = proc.cmdline()
            for arg in cmdline:
                if PROCNAME in arg:
                    if 'Administrator' in proc.username():
                        print("killing:")
                        print(proc)
                        proc.kill()
        except:
            print("can no get process due to permission")
    print("trading system shut down by scheduler")

trading_system_shutdown_job()