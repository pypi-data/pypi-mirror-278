# autopep8: off
import os
import sys
from flask import Flask,request,Response
if not os.path.dirname(os.path.dirname(__file__)) in sys.path:
  sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MainServiceManager import __version__,__version_tuple__
from MainServiceManager.server_utils import *
args=get_args()
if args.version:
  print(f"MainServiceManager {__version__}")
  sys.exit(0)
if args.config:
  cfg=cfg_load(args.config)
else:
  cfg=cfg_load()
services["admin"]=service("admin",cfg["password"])
app=Flask("MainServiceManager")
def init():
  for k,v in services.items():
    if v["autostart"]:
      v()
@app.route("/admin/status",methods=["GET"])
def admin_status(internal=False):
  r=make_r()
  return r
@app.route("/admin/list/svc",methods=["GET"])
def admin_list_svc(internal=False):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
  if user!="admin":
    return make_r(code=403)
  d=[]
  for k,v in services.items():
    if not v.closed:
      if k!="admin":
        d.append(v.to_dict())
  r=make_r(d)
  return r
@app.route("/admin/list/name",methods=["GET"])
def admin_list_name(internal=False):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
  if user!="admin":
    return make_r(code=403)
  d=[]
  for k,v in services.items():
    if not v.closed:
      if k!="admin":
        d.append(k)
  r=make_r(d)
  return r
@app.route("/admin/stop",methods=["POST"])
def admin_stop(internal=False,threaded=False):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
  if user!="admin":
    return make_r(code=403)
  if threaded:
    for k,v in services.items():
      if not v.closed:
        v.disable()
    sleep(5)
    os.kill(os.getpid(),signal.SIGINT)
    sys.exit(0)
  else:
    Thread(target=admin_stop,kwargs={"internal":True,"threaded":True}).start()
  r=make_r()
  return r
@app.route("/admin/kill",methods=["POST"])
def admin_kill(internal=False,threaded=False):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
  if user!="admin":
    return make_r(code=403)
  if threaded:
    for k,v in services.items():
      if not v.closed:
        v.disable()
    sleep(5)
    os.kill(os.getpid(),signal.SIGKILL)
  else:
    Thread(target=admin_kill,kwargs={"internal":True,"threaded":True}).start()
  r=make_r()
  return r
@app.route("/admin/reload",methods=["POST"])
def admin_reload(internal=False):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
  if user!="admin":
    return make_r(code=403)
  for k,v in list(services.items()):
    if v.closed:
      services.pop(k)
    else:
      v.reload()
      if v.closed:
        services.pop(k)
  for i in ms.dir.list(cfg["services_dir"],["json","msvc"],dirs=False):
    name=os.path.basename(i)
    if not name in services:
      services[name]=service(i)
  r=make_r()
  return r
@app.route("/svc/info",methods=["GET"])
def svc_info(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  r=make_r(svc.to_dict())
  return r
@app.route("/svc/enable",methods=["POST"])
def svc_enable(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  svc.enable()
  r=make_r()
  return r
@app.route("/svc/disable",methods=["POST"])
def svc_disable(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  svc.disable()
  r=make_r()
  return r
@app.route("/svc/start",methods=["POST"])
def svc_start(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  svc.start()
  r=make_r()
  return r
@app.route("/svc/restart",methods=["POST"])
def svc_restart(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  svc.restart()
  r=make_r()
  return r
@app.route("/svc/stop",methods=["POST"])
def svc_stop(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  svc.stop()
  r=make_r()
  return r
@app.route("/svc/kill",methods=["POST"])
def svc_kill(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  svc.kill()
  r=make_r()
  return r
@app.route("/svc/close",methods=["POST"])
def svc_close(internal=False,svc:service=None):
  if internal:
    user="admin"
  else:
    user=auth(cfg,request)
    if not user:
      return make_r(code=401)
    if "svc" in request.args:
      if request.args["svc"] in services:
        svc=services[request.args["svc"]]
      else:
        return make_r(code=404)
    else:
      return make_r(code=400)
  if not access(user,svc):
    return make_r(code=403)
  name=svc.name
  svc.close()
  if name in services:
    services.pop(name)
  r=make_r()
  return r
if __name__=="__main__":
  check_port(cfg)
  admin_reload(True)
  init()
  try:
    app.run(cfg["host"],cfg["port"],False)
  except:
    pass
  for k,v in services.items():
    try:
      v.close()
    except:
      pass