import datetime
import json
from markupsafe import Markup
import os
import secrets
import uuid

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
)
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import MultipleFileField, SubmitField, StringField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)  # cross-site scripting protection, somehow


class FrontForm(FlaskForm):
    uploader = MultipleFileField(
        "choose some replay files for processing.",
        validators=[DataRequired()],
    )
    tourney_slug_input = StringField(
        description="URL slug for the tournament, e.g. black-tie-9",
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


class SubmitForm(FlaskForm):
    titlefield = StringField(
        description="Title for the YouTube upload.",
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = FrontForm()
    if "user_id" not in session:
        # just got here, generate a UID.
        session["user_id"] = str(uuid.uuid4())
    message = ""
    auth_status = (
        f"Logged in as {session['credentials']['account']}"
        if "credentials" in session
        else "Not logged in. -->"
    )

    # if form.validate_on_submit():
    #     if "credentials" not in session:
    #         # TODO: this doesnt work. i think i have a poor understanding of how to
    #         # do these types of messages.
    #         message = "<b>Log in with your Google account to use the uploader.</b>"
    #         return redirect(url_for("index"))

    #     # --- Slippi parsing
    #     files_received_list = request.files.to_dict(flat=False)["uploader"]
    #     organized_replays_list = slippi.process_files(
    #         files_received_list, form.tourney_slug_input.data
    #     )
    #     # ** NOTE ref: data schema for the replay entries here is:
    #     # characters costumes tags stage timestamp duration winner filename
    #     # --- Start.gg parsing
    #     raw_response = startgg.send_request(form.tourney_slug_input.data)
    #     (organized_sets_list, tournament_name) = startgg.organize_result(
    #         raw_response.content
    #     )

    #     # If we got here, ready to go! ========================
    #     session["tournament_slug"] = form.tourney_slug_input.data
    #     session["tournament_name"] = tournament_name
    #     user_id = session["user_id"]
    #     # Fill up redis with user data.
    #     for replay_info in organized_replays_list:
    #         redis_client.lpush(f"user:{user_id}:replays", json.dumps(replay_info))
    #     redis_client.expire(f"user:{user_id}:replays", 3600)
    #     for set_info in organized_sets_list:
    #         redis_client.lpush(f"user:{user_id}:sets", json.dumps(set_info))
    #     redis_client.expire(f"user:{user_id}:sets", 3600)

    #     return redirect(url_for("sorting"))

    return render_template(
        "index.html",
        form=form,
        message=message,
        auth_status=auth_status,
    )


# @app.route("/sorting", methods=["POST", "GET"])
# def sorting():
#     tourney_name = session["tournament_slug"] if "tournament_slug" in session else None
#     user_id = session["user_id"] if "user_id" in session else None

#     submit_form = SubmitForm()
#     if submit_form.validate_on_submit():
#         ...  # ensure user_id exists, it may be None if things were done out of order
#         submissions = []
#         while True:
#             popresult = redis_client.lpop(f"user:{user_id}:selectedreplays")
#             if popresult is None:
#                 break
#             submissions.append(json.loads(popresult))

#         queue_item = {
#             "user_id": user_id,
#             "filename": submit_form.titlefield.data,
#             "files": [replay["filename"] for replay in submissions],
#         }
#         redis_client.lpush("conversion_queue", json.dumps(queue_item))
#         return redirect(url_for("sorting"))

#     redis_replays_list = redis_client.lrange(f"user:{user_id}:replays", 0, -1)
#     redis_sets_list = redis_client.lrange(f"user:{user_id}:sets", 0, -1)
#     redis_selected_replays_list = redis_client.lrange(
#         f"user:{user_id}:selectedreplays", 0, -1
#     )
#     redis_selected_set = redis_client.get(f"user:{user_id}:selectedset") or ""

#     replays_table = []
#     for i, e1 in enumerate(redis_replays_list):
#         if "SELECTED" in e1:
#             continue
#         decoded = json.loads(e1)
#         decoded["_index"] = i
#         # silly place to do this, but it's a one-off.
#         image_prefix = "<img src='static/icons/"
#         decoded["character_icons"] = Markup(
#             f"{image_prefix}{decoded['characters'][0]}{decoded['costumes'][0]}.png'>"
#             + " vs "
#             + f"{image_prefix}{decoded['characters'][1]}{decoded['costumes'][1]}.png'>"
#         )
#         # * two one-offs.
#         decoded["duration_minsec"] = str(
#             datetime.timedelta(seconds=decoded["duration"] // 60)
#         ).lstrip("0:")
#         replays_table.append(decoded)

#     sets_table = []
#     for i, e2 in enumerate(redis_sets_list):
#         if "SELECTED" in e2:
#             continue
#         decoded = json.loads(e2)
#         decoded["_index"] = i
#         sets_table.append(decoded)

#     # Convert selectedset to a title string, and put it in the form:
#     if redis_selected_set:
#         sel_data = json.loads(redis_selected_set)
#         title_string = (
#             f"{session['tournament_name']} "
#             f"{sel_data['Round Name']} -- "
#             f"{sel_data['Player 1']} vs. "
#             f"{sel_data['Player 2']}"
#         )
#         submit_form.titlefield.data = title_string

#     selections_table = []
#     for i, selected_element in enumerate(redis_selected_replays_list):
#         # follow the same format as the "replays" table
#         # TODO: LOTS OF REPETITION HERE!
#         decoded = json.loads(selected_element)
#         decoded["_index"] = i
#         image_prefix = "<img src='static/icons/"
#         decoded["character_icons"] = Markup(
#             f"{image_prefix}{decoded['characters'][0]}{decoded['costumes'][0]}.png'>"
#             + " vs "
#             + f"{image_prefix}{decoded['characters'][1]}{decoded['costumes'][1]}.png'>"
#         )
#         decoded["duration_minsec"] = str(
#             datetime.timedelta(seconds=decoded["duration"] // 60)
#         ).lstrip("0:")
#         selections_table.append(decoded)

#     return render_template(
#         "sorting.html",
#         replays_table=replays_table,
#         sets_table=sets_table,
#         selections_table=selections_table,
#         tournament=tourney_name,
#         submit_form=submit_form,
#     )


# @app.route("/auth/google")
# def auth_initiate():
#     initial_flow = flow.Flow.from_client_config(
#         json.loads(os.environ["GOOGLE_CLIENT_SECRET_JSON"]),
#         scopes=SCOPES,
#         redirect_uri="https://slp.heatherspacek.com/auth/callback",
#     )
#     authorization_url, state = initial_flow.authorization_url(
#         access_type="offline", include_granted_scopes="true", prompt="consent"
#     )
#     session["state"] = state
#     return redirect(authorization_url)


# @app.route("/auth/callback")
# def auth_callback():
#     state = session["state"]
#     reconstructed_flow = flow.Flow.from_client_config(
#         json.loads(os.environ["GOOGLE_CLIENT_SECRET_JSON"]),
#         scopes=SCOPES,
#         state=state,
#         redirect_uri="https://slp.heatherspacek.com/auth/callback",
#     )

#     authorization_response = request.url.replace("http://", "https://")
#     reconstructed_flow.fetch_token(authorization_response=authorization_response)
#     credentials = reconstructed_flow.credentials
#     some_credentials = {
#         "_uid": session["user_id"],
#         "account": credentials.account,
#         "token": credentials.token,
#         "refresh_token": credentials.refresh_token,
#         "granted_scopes": credentials.granted_scopes,
#     }

#     session["credentials"] = some_credentials
#     redis_client.rpush("credentials", json.dumps(some_credentials))
#     return redirect(url_for("index"))


# # #####     #####     #####     #####     #####     #####     #####
# # Interactivity endpoints. (clickies for tables on /sorting/)
# #      #####     #####     #####     #####     #####     #####


# @app.route("/sorting/select_r/<int:index>/")
# def select_set(index):
#     user_id = session["user_id"] if "user_id" in session else None
#     # If one is already selected, swap it out (put it back in the sets list)
#     prev_selection = redis_client.get(f"user:{user_id}:selectedset")
#     if prev_selection is not None:
#         redis_client.linsert(
#             f"user:{user_id}:sets", "BEFORE", "SELECTED", prev_selection
#         )
#         redis_client.lrem(f"user:{user_id}:sets", 1, "SELECTED")

#     new_selection = redis_client.lindex(f"user:{user_id}:sets", index)
#     redis_client.lset(f"user:{user_id}:sets", index, "SELECTED")
#     redis_client.set(f"user:{user_id}:selectedset", new_selection)

#     return redirect(url_for("sorting"))


# @app.route("/sorting/select_l/<int:index>/")
# def select_replay(index):
#     user_id = session["user_id"] if "user_id" in session else None
#     if len(redis_client.lrange(f"user:{user_id}:selectedreplays", 0, -1)) <= 5:
#         chosen_replay = redis_client.lindex(f"user:{user_id}:replays", index)
#         redis_client.lpush(f"user:{user_id}:selectedreplays", chosen_replay)
#         redis_client.lset(f"user:{user_id}:replays", index, "SELECTED")
#     return redirect(url_for("sorting"))


# @app.route("/sorting/move_up/<int:index>/")
# def reorder_selection_up(index):
#     if index != 0:
#         user_id = session["user_id"] if "user_id" in session else None
#         list_name = f"user:{user_id}:selectedreplays"
#         lower_elem = redis_client.lindex(list_name, index)
#         higher_elem = redis_client.lindex(list_name, index - 1)
#         redis_client.lrem(list_name, 1, lower_elem)
#         redis_client.linsert(list_name, "BEFORE", higher_elem, lower_elem)
#     return redirect(url_for("sorting"))


# @app.route("/sorting/move_down/<int:index>/")
# def reorder_selection_down(index):
#     user_id = session["user_id"] if "user_id" in session else None
#     list_name = f"user:{user_id}:selectedreplays"
#     n_elem = len(redis_client.lrange(list_name, 0, -1))
#     if index != n_elem - 1:
#         higher_elem = redis_client.lindex(list_name, index)
#         lower_elem = redis_client.lindex(list_name, index + 1)
#         redis_client.lrem(list_name, 1, higher_elem)
#         redis_client.linsert(list_name, "AFTER", lower_elem, higher_elem)
#     return redirect(url_for("sorting"))


# @app.route("/sorting/deselect_replay/<int:index>/")
# def deselect_replay(index):
#     user_id = session["user_id"] if "user_id" in session else None
#     # this can make them get "put back" into weird spots, but who cares :p
#     put_this_back = redis_client.lindex(f"user:{user_id}:selectedreplays", index)
#     redis_client.linsert(f"user:{user_id}:replays", "BEFORE", "SELECTED", put_this_back)
#     redis_client.lrem(f"user:{user_id}:replays", 1, "SELECTED")
#     return redirect(url_for("sorting"))


# @app.route("/queue")
# def view_queue():
#     """
#     https://github.com/helloflask/bootstrap-flask/blob/main/examples/bootstrap5/templates/table.html
#     https://github.com/helloflask/bootstrap-flask/blob/main/examples/bootstrap5/app.py
#     """
#     titles = [("id", "#"), ("text", "Message")]
#     table_data = []
#     queue_length = redis_client.llen("conversion_queue")

#     if queue_length > 0:
#         contents = redis_client.lrange("conversion_queue", 0, -1)
#         for idx, data in enumerate(contents):
#             table_data.append({"id": idx, "text": data})
#     return render_template("queue.html", data=table_data, titles=titles)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
