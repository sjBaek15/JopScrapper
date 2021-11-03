"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from urllib.parse import quote, unquote
from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as get_so_jobs
from ww import get_jobs as get_ww_jobs
from ro import get_jobs as get_ro_jobs
from export import save_to_file

app = Flask("finale")

db = {}
db_so = {}
db_ww = {}
db_ro = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def report():
    word = quote(request.args.get("word"))

    if word:
        exist_word_so = db_so.get(word)
        exist_word_ww = db_ww.get(word)
        exist_word_ro = db_ro.get(word)

        if exist_word_so or exist_word_ww or exist_word_ro:
            jobs_so = exist_word_so
            jobs_ww = exist_word_ww
            jobs_ro = exist_word_ro
        else:
            jobs_so = get_so_jobs(word)
            jobs_ww = get_ww_jobs(word)
            jobs_ro = get_ro_jobs(word)

            total_jobs = jobs_so + jobs_ww + jobs_ro

            db_so[word] = jobs_so
            db_ww[word] = jobs_ww
            db_ro[word] = jobs_ro

            db[word] = total_jobs

        total = len(jobs_so) + len(jobs_ww) + len(jobs_ro)
    else:
        return redirect("/")

    return render_template(
        "search.html",
        total=total,
        word=unquote(word),
        jobs_so=jobs_so,
        so_num=len(jobs_so),
        jobs_ww=jobs_ww,
        ww_num=len(jobs_ww),
        jobs_ro=jobs_ro,
        ro_num=len(jobs_ro))

@app.route("/export")
def export():
  word = request.args.get("word")
  if word:
    word = word.lower()
    jobs = db.get(word)

    if jobs:
      save_to_file(jobs, word)
      return send_file(f"./csv/{word}.csv", as_attachment=True)
    else:
      return redirect("/")




app.run(host="0.0.0.0")