# autopep8: off
import argparse
import os
import signal
import subprocess
import sys
import MainShortcuts as ms
from . import Launcher,__version__,__version_tuple__
__dir__=os.path.dirname(__file__)
def server():
  p=subprocess.Popen([sys.executable,__dir__+"/server.py"])
  try:
    return p.wait()
  except:
    pass
  p.send_signal(signal.SIGINT)
def client():
  argp=argparse.ArgumentParser(
    description=f"MainServiceManager {__version__} client",
    epilog="Creator: MainPlay_TG\nContact: https://t.me/MainPlay_TG\nMade in Russia",
    formatter_class=argparse.RawTextHelpFormatter,
    prog="MSVC-client",
    )
  argp.add_argument("-v","--version",
    action="store_true",
    help="print the version and exit",
    )
  argp.add_argument("-c","--config",
    default=None,
    help='config file. Default "~/.config/MainServiceManager/cfg.json"',
    )
  argp.add_argument("--host",
    default=None,
    help="host on which the server is launched. Default 127.0.0.1",
    )
  argp.add_argument("-p","--port",
    default=None,
    help="port on which the server is launched. Default 8960",
    )
  argp.add_argument("-U","--user",
    default=None,
    help='username. Default "admin"',
    )
  argp.add_argument("-P","--pass",
    default=None,
    help="password. If absent, the input from the keyboard will be requested",
    )
  argp.add_argument("action",
    help="the action performed with the service",
    )
  argp.add_argument("service",
    help='service name. To control the server, write "admin"',
    )
  args=argp.parse_args()
  try:
    if args.config:
      cfg=ms.json.read(args.config)
    else:
      cfg=ms.json.read(os.path.expanduser("~/.config/MainServiceManager/cfg.json"))
  except:
    print("Failed to read the config file",file=sys.stderr)
    cfg={}
  if args.host:
    cfg["host"]=args.host
  if args.port:
    cfg["port"]=args.port
  if args.user:
    cfg["user"]=args.user
  if getattr(args,"pass"):
    cfg["password"]=getattr(args,"pass")
  if not cfg.get("host"):
    print('"host" was not found in the config file. I use the value "127.0.0.1"',file=sys.stderr)
    cfg["host"]="127.0.0.1"
  if not cfg.get("port"):
    print('"port" was not found in the config file. I use the value 8960',file=sys.stderr)
    cfg["port"]=8960
  if not cfg.get("user"):
    print('"user" was not found in the config file. I use the value "admin"',file=sys.stderr)
    cfg["user"]="admin"
  if not cfg.get("password"):
    print('"password" was not found in the config file',file=sys.stderr)
    cfg["password"]=input('Enter the password from the user "{user}" =>'.format(**cfg))
  launcher=Launcher(cfg)
  if args.service=="admin":
    if args.action=="kill":
      ms.json.print(launcher.admin_kill())
      return
    if args.action=="list_name":
      ms.json.print(launcher.admin_list_name())
      return
    if args.action=="list_svc":
      ms.json.print(launcher.admin_list_svc())
      return
    if args.action=="reload":
      ms.json.print(launcher.admin_reload())
      return
    if args.action=="status":
      ms.json.print(launcher.admin_status())
      return
    if args.action=="stop":
      ms.json.print(launcher.admin_stop())
      return
    print("Unknown action\nAvailable actions for the server: "+", ".join(["kill","list_name","list_svc","reload","status","stop"]),file=sys.stderr)
    return
  else:
    if args.action=="close":
      ms.json.print(launcher.svc_close(args.service))
      return
    if args.action=="disable":
      ms.json.print(launcher.svc_disable(args.service))
      return
    if args.action=="enable":
      ms.json.print(launcher.svc_enable(args.service))
      return
    if args.action=="info":
      ms.json.print(launcher.svc_info(args.service))
      return
    if args.action=="kill":
      ms.json.print(launcher.svc_kill(args.service))
      return
    if args.action=="restart":
      ms.json.print(launcher.svc_restart(args.service))
      return
    if args.action=="start":
      ms.json.print(launcher.svc_start(args.service))
      return
    if args.action=="stop":
      ms.json.print(launcher.svc_stop(args.service))
      return
    print("Unknown action\nAvailable actions for the service: "+", ".join(["close","disable","enable","info","kill","restart","start","stop"]),file=sys.stderr)
    return