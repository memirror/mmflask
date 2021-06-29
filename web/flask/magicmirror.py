# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/29

import os
import sys
import logging

from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
from flask import jsonify
from flask.views import MethodView

from magicmirror.runme import mm
from magicmirror.runme import Record
from magicmirror.runme import LimitExecuteDuration

here = os.path.dirname(__file__)
logger = logging.getLogger("magicmirror")
app = Flask("magicmirror", template_folder=os.path.join(here, "templates"))


class MagicMirror(MethodView):

    def get(self):
        question = request.args.get('question')
        ret = LimitExecuteDuration(5).run(mm, question)._result
        record = Record(question=question, answer="", source="")
        if ret:
            logger.info("[from] %s", ret["source"])
            record.source = ret["source"]
            record.answer = ret["out"]
        else:
            ret = {"out": "i donot know either"}
        record.save()
        return jsonify(ret["out"])


class MMIcon(MethodView):
    def get(self):
        return send_file(os.path.join(here, "templates\magicmirror.ico"), mimetype="image/x-icon")


@app.route("/")
def home():
    return render_template("home.html")


app.add_url_rule('/mm', view_func=MagicMirror.as_view('mm'))
app.add_url_rule("/icon", view_func=MMIcon.as_view("icon"))
  
