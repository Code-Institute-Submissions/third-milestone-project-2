from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from bson.objectid import ObjectId
from semgmtapp.helpers import users_collection, properties_collection

profile = Blueprint("profile", __name__)


@profile.route("/view_profile", methods=["GET", "POST"])
def view_profile():

    if session.get("username"):

        agent = session["username"]
        agent_details = users_collection.find({"username": agent})

        return render_template(
            "view_profile.html", agent=agent, agent_details=agent_details
        )

    else:
        flash("You must be logged in to view this page.")
        return redirect(url_for("reg_login.login"))


@profile.route("/view_profile/<username>/change_photo", methods=["GET", "POST"])
def change_photo(username):

    users_collection.update(
        {"username": username}, {"$set": {"photoUrl": request.form.get("photoUrl")}}
    )
    flash(
        " {} your profile photo was successfully updated.".format(username.capitalize())
    )

    return redirect(url_for("profile.view_profile"))


@profile.route("/view_profile/<username>/delete_account", methods=["GET", "POST"])
def delete_account(username):

    # Delete user from Users collection
    users_collection.delete_one({"username": username})

    # Delete all Ads from this Agent
    properties_collection.delete_many({"agent": username.upper()})

    # Clear session data
    session.pop("username", None)

    # Flash Alert with confirmation
    flash("Your account has been successfully deleted.")

    return redirect(url_for("main.index"))