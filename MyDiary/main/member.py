from main import *
from flask import Blueprint

blueprint = Blueprint("member", __name__, url_prefix="/member")


@blueprint.route("/join", methods=["POST", "GET"])
def join():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pw = request.form.get("PW", type=str)
        pw2 = request.form.get("PW2", type=str)

        if name == "" or email == "" or pw == "" or pw2 == "":
            flash("입력을 다시 확인해주세요.")
            return render_template("join.html", title="회원가입")
        if pw != pw2:
            flash("비밀번호를 다시 확인해주세요")
            return render_template("join.html", title="회원가입")

        # 중복가입 방지
        members = mongo.db.members
        cnt = members.find({"email": email}).count()
        if cnt > 0:
            flash("이미 존재하는 계정입니다.")
            return render_template("join.html", title="회원가입")
        else:
            flash("가입이 완료되었습니다, 환영합니다!")
            # return render_template("login.html",title="login")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        post = {
            "name": name,
            "email": email,
            "pw": pw,
            "joindate": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }

        members.insert_one(post)
        return render_template("login.html", title="login")

    else:
        return render_template("join.html", title="회원가입")


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("id")
        password = request.form.get("pass")
        next_url = request.form.get("next_url")

        members = mongo.db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원 정보를 찾을 수 없습니다")
            return redirect(url_for("member.login"))
        else:
            if data.get("pass") == password:
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True  # 자원의 효율적 운영을 위해 true로 놓음
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for("board.lists"))
            else:
                flash("비밀번호 오류입니다, 다시 입력해주세요")
                return redirect(url_for("member.login"))
    else:
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url, title="로그인")
        else:
            return render_template("login.html", title="로그인")


@blueprint.route("/logout")
def logout():

    try:  # 로그아웃 상태에서 다시 로그아웃을 눌렀을 때 오류 방지
        del session["name"]
        del session["id"]
        del session["email"]
    except:
        pass
    return redirect(url_for("member.login"))
