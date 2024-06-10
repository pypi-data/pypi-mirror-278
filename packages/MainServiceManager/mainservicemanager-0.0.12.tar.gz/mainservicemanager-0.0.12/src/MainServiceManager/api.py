import requests
import os
import MainShortcuts as ms
from hashlib import sha256
from typing import Union


def request(method: str, url: str, *, ignore_error: bool = False, **kw) -> requests.Response:
  url = str(url)
  tmp = True
  for i in ["http://", "https://"]:
    if url.startswith(i):
      tmp = False
  if tmp:
    url = "http://" + url
  if "data" in kw:
    if type(kw["data"]) in [dict, list, tuple]:
      kw["data"] = ms.json.encode(kw["data"])
      if not "headers" in kw:
        kw["headers"] = {}
      kw["headers"]["Content-Type"] = "application/json"
  kw["method"] = method
  kw["url"] = url
  r = requests.request(**kw)
  if not ignore_error:
    r.raise_for_status()
  return r


def auth_header(user: str, password: str) -> str:
  return "Basic " + ":".join([user, sha256(password.encode("utf-8")).hexdigest()])


class AccessDenied(Exception):
  pass


class Launcher:
  """API for MainServicemanager\nIf the user is not an admin, the service name is not necessary"""

  def __init__(self, cfg: Union[str, dict] = None):
    """Give the dictionary or the path to the config file, otherwise the config file is used by default"""
    if cfg == None:
      if os.path.isfile(os.path.expanduser("~/.config/MainServiceManager/cfg.json")):
        cfg = os.path.expanduser("~/.config/MainServiceManager/cfg.json")
      else:
        cfg = {}
    if type(cfg) == str:
      cfg = ms.json.read(cfg)
    if "host" in cfg:
      self.host = cfg["host"]
    else:
      self.host = "127.0.0.1"
    if "port" in cfg:
      self.port = int(cfg["port"])
    else:
      self.port = 8960
    if "user" in cfg:
      self.user = cfg["user"]
    else:
      if "name" in cfg:
        self.user = cfg["name"]
      else:
        self.user = "admin"
    if "password" in cfg:
      self.password = cfg["password"]
    else:
      self.password = ""
    if self.host == "0.0.0.0":
      self.host = "127.0.0.1"

  def request(self, method: str, path: str, **kw) -> Union[dict, requests.Response, bytes]:
    kw["method"] = method
    if not "stream" in kw:
      kw["stream"] = False
    if not "headers" in kw:
      kw["headers"] = {}
    kw["headers"]["Authorization"] = auth_header(self.user, self.password)
    if not path.startswith("/"):
      path = "/" + path
    if self.user != "admin":
      path_split = path.split("/")
      if path_split[1] == "admin":
        if path_split[2] != "status":
          raise AccessDenied("This action is available only to the administrator")
      if path_split[1] == "svc":
        if "params" in kw:
          if "svc" in kw["params"]:
            if kw["params"]["svc"] != self.user:
              raise AccessDenied(f'You have access only to the service "{self.user}"')
    if self.host == "0.0.0.0":
      self.host = "127.0.0.1"
    kw["url"] = f"http://{self.host}:{self.port}{path}"
    r = request(**kw)
    if kw["stream"]:
      return r
    else:
      if r.headers["Content-Type"] == "application/json":
        return ms.json.decode(r.text)
      else:
        return r.content

  def admin_status(self):
    """Check the status of the server. Access rights are not needed"""
    return self.request("GET", "/admin/status")

  def admin_list_svc(self):
    """Get a list of all services and information about them"""
    return self.request("GET", "/admin/list/svc")["data"]

  def admin_list_name(self):
    """Get a list of service names"""
    return self.request("GET", "/admin/list/name")["data"]

  def admin_stop(self):
    """Stop the server"""
    return self.request("POST", "/admin/stop")

  def admin_kill(self):
    """Stop the server forcibly"""
    return self.request("POST", "/admin/kill")

  def admin_reload(self):
    """Update the list of services. Deleted services will be closed"""
    return self.request("POST", "/admin/reload")

  def svc_info(self, svc: str = None):
    """Get information about the service"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("GET", "/svc/info", params={"svc": svc})["data"]

  def svc_enable(self, svc: str = None):
    """Start and turn on the service"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/enable", params={"svc": svc})

  def svc_disable(self, svc: str = None):
    """Stop and turn off the service"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/disable", params={"svc": svc})

  def svc_start(self, svc: str = None):
    """Start the service. Do nothing if the service is already started"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/start", params={"svc": svc})

  def svc_restart(self, svc: str = None):
    """Restart the service. If the service is not started, it still starts"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/restart", params={"svc": svc})

  def svc_stop(self, svc: str = None):
    """Stop the service. Do nothing if the service is not started"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/stop", params={"svc": svc})

  def svc_kill(self, svc: str = None):
    """Stop the service forcibly. Do nothing if the service is not started"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/kill", params={"svc": svc})

  def svc_close(self, svc: str = None):
    """Stop and close the service. If the service is not deleted, after updating the list of services, it will be available again"""
    if svc == None:
      if self.user == "admin":
        raise TypeError("missing 1 required argument: 'svc'")
      else:
        svc = self.user
    return self.request("POST", "/svc/close", params={"svc": svc})
