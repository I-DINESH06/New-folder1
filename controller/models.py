from controller.database import db
from datetime import datetime

# ---------------- USERS ----------------
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- QUIZ ----------------
class Quiz(db.Model):
    __tablename__ = "quiz"

    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_questions = db.Column(db.Integer)
    time_limit = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- QUESTIONS ----------------
class Question(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    question_text = db.Column(db.Text, nullable=False)


# ---------------- OPTIONS ----------------
class Option(db.Model):
    __tablename__ = "options"

    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    option_text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


# ---------------- QUIZ ATTEMPTS ----------------
class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    attempt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    score = db.Column(db.Integer)
    attempt_date = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- USER ANSWERS ----------------
class UserAnswer(db.Model):
    __tablename__ = "user_answers"

    answer_id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("quiz_attempts.attempt_id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    selected_option_id = db.Column(db.Integer, db.ForeignKey("options.option_id"))


# ---------------- RESULTS ----------------
class Result(db.Model):
    __tablename__ = "results"

    result_id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("quiz_attempts.attempt_id"))
    total_questions = db.Column(db.Integer)
    correct_answers = db.Column(db.Integer)
    wrong_answers = db.Column(db.Integer)
    percentage = db.Column(db.Float)
  