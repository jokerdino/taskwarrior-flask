from flask import Flask
from waitress import serve

import task_views


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.jinja_env.filters["format_dates"] = task_views.format_dates
    app.add_url_rule(
        "/tasks/pending", view_func=task_views.pending_tasks, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/tasks/waiting", view_func=task_views.waiting_tasks, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/tasks/completed",
        view_func=task_views.completed_tasks,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/tasks/all", view_func=task_views.all_tasks, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/tasks/<int:task_id>", view_func=task_views.view_task, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/tasks/add_task", view_func=task_views.add_task, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/tasks/<int:task_id>/edit",
        view_func=task_views.edit_task,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/tags/<string:tag>", view_func=task_views.view_tags, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/projects/<string:project>",
        view_func=task_views.view_projects,
        methods=["GET", "POST"],
    )
    app.add_url_rule("/projects", view_func=task_views.list_projects)
    app.add_url_rule("/tags", view_func=task_views.list_tags)
    return app


if __name__ == "__main__":
    app = create_app()
    serve(app, host="0.0.0.0", port=5000)
