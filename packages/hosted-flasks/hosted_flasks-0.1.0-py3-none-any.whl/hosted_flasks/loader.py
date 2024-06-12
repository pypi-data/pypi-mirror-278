import logging

import os
import sys

from pathlib import Path
from datetime import datetime
import humanize
import markdown

import yaml

from importlib.util import spec_from_file_location, module_from_spec

from dataclasses import dataclass, field
from typing import Union, Dict
from flask import Flask

from hosted_flasks.monkeypatch import Environment

logger = logging.getLogger(__name__)

apps = []

@dataclass
class HostedFlask:
  name         : str
  src          : Union[str, Path]
  path         : str   = None
  hostname     : str   = None
  app          : str   = "app"
  handler      : Flask = field(repr=False, default=None)
  environ      : Dict  = None

  last_updated : str   = None
  title        : str   = None
  description  : str   = None
  image        : str   = None
  github       : str   = None
  docs         : str   = None

  def __post_init__(self):
    if not self.path and not self.hostname:
      logger.fatal(f"⛔️ an app needs at least a path or a hostname: {self.name}")
      return

    self.src = Path(self.src).resolve() # ensure it's a Path

    # we need to add app to apps before loading the handler, because else the
    # monkeypatched os.environ.get won't be able to correct handle calls to it
    # at the time of loading the handler
    apps.append(self)

    # if the handler isn't provided, load it from the source
    if not self.handler:
      self.load_handler()
      
    # without a handler, we remove ourself from the apps
    if not self.handler:
      logger.fatal(f"⛔️ an app needs a handler: {self.src.name}.{self.app}")
      apps.remove(self)
  
  def load_handler(self):
    parts = self.app.split(":", 1)  # app or name:app or name.sub:app
    if len(parts) == 1: # only an app object name
      module = self.src.name  # default module name
      appname = parts[0]
    else: # explicit module path and app object name
      module, appname = parts[0], parts[1]
  
    # construct filepath from module path on top of the parent root path
    module_path = self.src.parent
    for submodule in module.split("."):
      module_path = module_path / submodule

    # create a fresh monkeypatched environment scoped to the app name
    self.environ = Environment.scope(self.src.name)

    # load the module, creating the handler flask app
    try:
      spec = spec_from_file_location(self.src.name, module_path / "__init__.py")
      mod = module_from_spec(spec)
      sys.modules[self.src.name] = mod
      spec.loader.exec_module(mod)
      # extract the handler from the mod using the appname
      self.handler = getattr(mod, appname)
    except FileNotFoundError:
      logger.warning(f"😞 '{module_path}' doesn't provide '__init__.py'")
    except AttributeError:
      logger.warning(f"😞 '{module_path}' doesn't provide flask object: {self.app}")
    except Exception:
      logger.exception(f"😞 '{module_path}' failed to load due to")

def add_app(name, src, **kwargs):
  app = HostedFlask(name, src, **kwargs)
  logger.info(f"🌍 loaded app: {app.name}")

def get_apps(config=None, force=False):
  global apps

  if force:
    apps.clear()

  # lazy load the apps
  if not apps:
    if not config:
      config = os.environ.get("HOSTED_FLASKS_CONFIG", Path() / "hosted-flasks.yaml")
    try:
      with open(config) as fp:
        for name, settings in yaml.safe_load(fp).items():
          src = config.parent / settings.pop("src")
          settings["last_updated"] = get_last_updated(name)
          settings["description"] = markdown.markdown(settings.pop("description", ""))
          add_app(name, src, **settings)
    except FileNotFoundError:
      raise ValueError(f"💀 I need a config file. Tried: {config}")
  return apps

def get_last_updated(name):
  files = list(Path(name).rglob("*"))
  if files:
    last_mtime = max( [ p.lstat().st_mtime for p in files ] )
    last_updated = datetime.now() - datetime.fromtimestamp(last_mtime)
    return humanize.naturaltime(last_updated)
  return None
