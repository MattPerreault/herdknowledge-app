import re


BLOCKED_PHRASES = {"ignore previous", "as a language model", "simulate", "you are now"}


def is_safe_sql(sql: str) -> bool:
    # Normalize the SQL for consistent pattern matching
    sql = sql.strip().lower()

    # Strip a trailing semicolon if it's there (optional but cleaner)
    if sql.endswith(";"):
        sql = sql[:-1]

    # Destructive or dangerous SQL keywords
    prohibited_patterns = [
        r"\b(drop|delete|insert|update|alter|create|truncate)\b",
        r"--",  # inline comment
        r"/\*",  # block comment
    ]

    for pattern in prohibited_patterns:
        if re.search(pattern, sql):
            return False

    # Reject if multiple SQL statements are present
    if sql.count(";") > 0:
        return False

    # Basic sanity: must start with SELECT
    return sql.startswith("select")


def is_safe_question(question: str) -> bool:
    lower = question.lower()
    return not any(phrase in lower for phrase in BLOCKED_PHRASES)
