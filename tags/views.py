from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from DB import data_base
from core import app


@app.route('/edit_interest', methods=["GET", "POST"])
@jwt_required()
def edit_interest():
    user_name: str = get_jwt_identity()
    if user_name != 'ADMIN':
        return {"response": "500", "message": "401"}
    if request.method == 'POST':
        new_interests = request.json.get("new_interests", None)
        edit_interests = request.json.get("edit_interests", None)
        if new_interests is None or edit_interests is None:
            return {"response": "500", "message": "401"}
        if type(new_interests) is not list or type(edit_interests) is not list:
            return {"response": "500", "message": "401"}
        for interest in new_interests:
            if type(interest) is not str or data_base.has_tag(interest):
                return {"response": "500", "message": "401"}
            data_base.create_tag(interest)
        for interest in edit_interests:
            try:
                old_interest = interest["interest_name"]
                new_interest = interest["new_name"]
                if type(old_interest) is not str or type(new_interest) is not str:
                    return {"response": "500", "message": "401"}
                if not data_base.has_tag(old_interest) or data_base.has_tag(new_interest):
                    return {"response": "500", "message": "401"}
                data_base.delete_tag_as(old_interest)
                if new_interest != "":
                    data_base.create_tag(new_interest)
                return {"response": "200", "message": "OK"}
            except TypeError:
                return {"response": "500", "message": "401"}
        return {"response": "200", "message": "OK"}
    return {"interests": data_base.get_tags()}
