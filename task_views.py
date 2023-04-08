import datetime

from flask import redirect, render_template, request, url_for
from tasklib import Task, TaskWarrior
from tasklib.task import local_zone

from task_forms import TaskEditForm

tw = TaskWarrior("~/.task")  # make it configurable

now = local_zone.localize(datetime.datetime.now())


def favicon():
    return url_for("static", filename="favicon.ico")


def pending_tasks():
    title = "List of pending tasks"
    tasks_pending = tw.tasks.pending()
    now_time = datetime.datetime.now(datetime.timezone.utc)
    if request.method == "POST":
        list_task_ids = request.form.getlist("task_ids")
        for task_id in list_task_ids:
            task = tasks_pending.filter(id=task_id)
            task[0].done()
        return redirect(url_for("pending_tasks"))
    return render_template(
        "list_pending.html", title=title, now_time=now_time, tasks=tasks_pending
    )


def completed_tasks():
    title = "List of completed tasks"
    tasks_completed = tw.tasks.completed()
    return render_template("list_tasks.html", title=title, tasks=tasks_completed)


def all_tasks():
    title = "List of all tasks"
    tasks_all = tw.tasks.all()
    return render_template("list_tasks.html", title=title, tasks=tasks_all)


def waiting_tasks():
    # filtering using raw command -
    title = "List of waiting tasks"
    tasks_waiting = tw.tasks.all().filter("+WAITING")
    return render_template("list_pending.html", title=title, tasks=tasks_waiting)


def view_task(task_id):
    task = tw.tasks.filter(id=task_id)
    if request.method == "POST":
        task[0].delete()
        return redirect(url_for("pending_tasks"))
    return render_template("task_page.html", task=task)


def add_task():
    form = TaskEditForm()
    if form.validate_on_submit():
        new_task = Task(tw)
        new_task["description"] = form.data["description"]
        new_task["due"] = form.data["due_date"]
        new_task["priority"] = form.data["priority"]
        new_task["project"] = form.data["project"]
        form_tags = form.data["tags"]  # .replace(" ","")#strip()
        tags_list = form_tags.split(",")
        new_task["tags"] = tags_list
        # new_task["email"] = form.data["email_date"]
        new_task["wait"] = form.data["wait_date"]
        new_task.save()
        if form.data["annotate"] != "":
            new_task.add_annotation(form.data["annotate"])

        new_task.save()

        return redirect(url_for("view_task", task_id=new_task["id"]))
    return render_template(
        "task_edit.html", title="Create new task", form=form, new_task=True
    )


def edit_task(task_id):
    task = tw.tasks.filter(id=task_id)
    form = TaskEditForm()

    if form.validate_on_submit():
        task[0]["description"] = form.data["description"]
        task[0]["due"] = form.data["due_date"]

        task[0]["priority"] = form.data["priority"]
        task[0]["project"] = form.data["project"]
        form_tags = form.data["tags"]
        tags_list = form_tags.split(",")
        task[0]["tags"] = tags_list
        # task[0]["email"] = form.data["email_date"]
        task[0]["wait"] = form.data["wait_date"]
        task[0].save()
        if form.data["annotate"] != "":
            task[0].add_annotation(form.data["annotate"])

        task[0].save()
        return redirect(url_for("view_task", task_id=task[0]["id"]))

    form.description.data = task[0]["description"]
    form.due_date.data = task[0]["due"]
    form.priority.data = task[0]["priority"]
    form.project.data = task[0]["project"]
    tag_string = ""
    for tag in task[0]["tags"]:
        tag_string += tag + ","
    form.tags.data = tag_string
    form.wait_date.data = task[0]["wait"]

    # if task[0]["email"] != None:
    #    form.email_date.data = format_dates(task[0]["email"])

    return render_template("task_edit.html", title="Edit task", task=task, form=form)


def view_tags(tag):
    title = "List of tasks with " + tag + " tag"
    tasks_pending = tw.tasks.pending().filter(tags__contains=[tag])
    print(tasks_pending)
    if request.method == "POST":
        list_task_ids = request.form.getlist("task_ids")
        for task_id in list_task_ids:
            task = tasks_pending.filter(id=task_id)
            task[0].done()
        return redirect(url_for("pending_tasks"))
    return render_template("list_pending.html", title=title, tasks=tasks_pending)


def view_projects(project):
    title = "List of tasks in project " + project
    tasks_pending = tw.tasks.pending().filter(project=project)
    if request.method == "POST":
        list_task_ids = request.form.getlist("task_ids")
        for task_id in list_task_ids:
            task = tasks_pending.filter(id=task_id)
            task[0].done()
        return redirect(url_for("pending_tasks"))
    return render_template("list_pending.html", title=title, tasks=tasks_pending)


def list_projects():
    tasks_all = tw.tasks.all()
    projects = []
    for task in tasks_all:
        projects.append(task["project"])
    filtered_list = [x for x in projects if x is not None]
    unique_projects_list = list(set(filtered_list))
    return render_template("projects.html", projects=unique_projects_list)


def list_tags():
    tasks_all = tw.tasks.all()
    tags = []
    for task in tasks_all:
        for tag in task["tags"]:
            tags.append(tag)
    unique_tag_list = list(set(tags))
    return render_template("tags.html", tags=unique_tag_list)


def format_dates(string):
    try:
        date_value = datetime.datetime.strptime(string, "%Y%m%dT%H%M%SZ")
        return date_value + datetime.timedelta(days=1)
    except ValueError as e:
        ...
        # print("Value error")
