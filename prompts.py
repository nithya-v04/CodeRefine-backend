def build_prompt(diff):
    return f"""
You are a senior software engineer reviewing a pull request.

Analyze the following code diff.

Return STRICT JSON format like:

{{
  "bugs": [],
  "performance": [],
  "security": [],
  "best_practices": []
}}

Code Diff:
{diff}
"""
