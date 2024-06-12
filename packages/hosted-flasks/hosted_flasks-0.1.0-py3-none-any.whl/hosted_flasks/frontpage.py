import logging

import os

from pathlib import Path

from flask import Flask, render_template, send_from_directory

from hosted_flasks.loader import get_apps

logger = logging.getLogger(__name__)

FRONTPAGE_FOLDER = os.environ.get("HOSTED_FLASKS_FRONTPAGE_FOLDER", None)
if not FRONTPAGE_FOLDER:
  FRONTPAGE_FOLDER = Path(__file__).resolve().parent / "frontpage"
  logger.debug("📰 using default frontpage folder")
else:
  FRONTPAGE_FOLDER = Path(FRONTPAGE_FOLDER).resolve()
  logger.info(f"📰 using custom frontpage folder: {FRONTPAGE_FOLDER.relative_to(Path.cwd())}")

app = Flask(
  "hosted-flasks",
  template_folder=FRONTPAGE_FOLDER,
  static_folder=f"{FRONTPAGE_FOLDER}/static",
  static_url_path=""
)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def show_frontpage():
  return render_template("index.html", apps=get_apps())

@app.route("/hosted/<path:filename>")
def send_frontpage_static(filename):
  # static folder from root of app that uses hosted flasks to serve apps
  return send_from_directory("", filename)
