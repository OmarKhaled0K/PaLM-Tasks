import re
import json
import sqlite3
import types
from collections import Counter
from json_repair import repair_json

class Evaluator:
    @staticmethod
    def normalize_text(x):
        """Normalize text by removing extra whitespace and converting to lowercase."""
        if x is None:
            return ""
        return re.sub(r"\s+", " ", x.strip()).lower()

    @staticmethod
    def normalize_json(obj):
        """Normalize JSON objects by sorting and standardizing structure."""
        if isinstance(obj, dict):
            return {k: Evaluator.normalize_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # normalize each element, then sort so order doesn't matter
            return sorted((Evaluator.normalize_json(v) for v in obj), key=lambda x: json.dumps(x, sort_keys=True))
        else:
            return obj

    @staticmethod
    def clean_sql(query: str) -> str:
        """Clean SQL query by removing markdown fences and leading/trailing spaces."""
        # Remove triple backtick blocks like ```sql ... ``` or ``` ...
        query = re.sub(r"```(?:sql)?", "", query, flags=re.IGNORECASE)
        # Strip whitespace
        return query.strip()

    def eval_exact(self, resp, expected):
        """Evaluate exact text match after normalization."""
        return self.normalize_text(resp) == self.normalize_text(expected)

    def eval_sql(self, resp_query, validation):
        """Evaluate SQL query against reference implementation."""
        conn = sqlite3.connect(":memory:")
        cur = conn.cursor()
        try:
            for s in validation.get("setup", []):
                cur.execute(s)
            conn.commit()
            cleaned_query = self.clean_sql(resp_query)
            # run returned query - if it fails, return False
            try:
                cur.execute(cleaned_query)
                resp_rows = cur.fetchall()
            except Exception as e:
                return False, {"error": str(e)}
            # run reference
            cur.execute(validation.get("reference_query"))
            ref_rows = cur.fetchall()
            # compare sorted sets (order not important)
            return sorted(resp_rows) == sorted(ref_rows), {"resp_rows": resp_rows, "ref_rows": ref_rows}
        finally:
            conn.close()

    def eval_json(self, resp, expected):
        """Evaluate JSON response against expected JSON."""
        parsed = None
        try:
            parsed = json.loads(resp)
        except Exception:
            parsed = repair_json(resp)
        if parsed is None:
            return False, None

        return self.normalize_json(parsed) == self.normalize_json(expected), parsed

    def evaluate_response(self, resp, test_case):
        """Main evaluation method that routes to appropriate evaluator based on match_type."""
        match_type = test_case.get("match_type")
        ok = False
        meta = {}

        if match_type == "exact":
            ok = self.eval_exact(resp, test_case.get("expected", ""))
        elif match_type == "sql":
            ok, meta = self.eval_sql(resp, test_case.get("sql_validation", {}))
        elif match_type == "json":
            ok, parsed = self.eval_json(resp, test_case.get("expected_json"))
            meta["parsed"] = parsed
        else:
            # default to exact
            ok = self.eval_exact(resp, test_case.get("expected", ""))

        return ok, meta
