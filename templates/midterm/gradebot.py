"""gradebot.py - pick counterbot OR timebot and add the JSON grader.
Every quiz answer: send a grading prompt with response_mime_type="application/json",
parse it with logic.parse_grade, show grade + feedback, and append
{"query", "question", "answer", "grade", "feedback", "time"} to grades.json.
"""
# TODO
