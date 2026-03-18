import re
from typing import Dict, Any, List

class LogAnalyzer:
    def __init__(self):
        self.error_patterns = [
            ("Dependency Error", re.compile(r"(npm ERR!|pip install|Could not resolve dependencies|mvn dependency|gradle error)", re.I)),
            ("Test Failure", re.compile(r"(FAILURES|AssertionError|Test failed|JUnit|pytest|jest)", re.I)),
            ("Docker Error", re.compile(r"(docker build|docker push|docker pull|Error response from daemon)", re.I)),
            ("Permission Error", re.compile(r"(Permission denied|chmod|sudo|Operation not permitted)", re.I)),
            ("Git Error", re.compile(r"(fatal:|git clone|git checkout|could not resolve host)", re.I)),
            ("Compilation Error", re.compile(r"(javac|Compilation failed|TypeScript error|tsc|error:)", re.I)),
        ]

    def analyze(self, console_log: str) -> Dict[str, Any]:
        truncated_log = self._truncate_log(console_log)
        error_type = "Unknown"
        summary = "No error detected."
        root_cause = ""
        fix_suggestions = []
        relevant_stage = ""

        for etype, pattern in self.error_patterns:
            match = pattern.search(truncated_log)
            if match:
                error_type = etype
                summary = self._extract_summary(truncated_log, match)
                root_cause = self._extract_root_cause(truncated_log, etype)
                fix_suggestions = self._suggest_fixes(etype)
                relevant_stage = self._extract_stage(truncated_log)
                break

        return {
            "error_type": error_type,
            "summary": summary,
            "root_cause": root_cause,
            "fix_suggestions": fix_suggestions,
            "relevant_stage": relevant_stage
        }

    def _truncate_log(self, log: str) -> str:
        tokens = log.split()
        if len(tokens) > 4000:
            return " ".join(tokens[:4000])
        return log

    def _extract_summary(self, log: str, match) -> str:
        lines = log.splitlines()
        for i, line in enumerate(lines):
            if match.group(0) in line:
                return line.strip()
        return "Error detected, but summary unavailable."

    def _extract_root_cause(self, log: str, error_type: str) -> str:
        if error_type == "Dependency Error":
            return "Dependency installation failed. Check package versions and network access."
        elif error_type == "Test Failure":
            return "Test suite failed. Review test output for details."
        elif error_type == "Docker Error":
            return "Docker command failed. Check Dockerfile and permissions."
        elif error_type == "Permission Error":
            return "Permission denied. Ensure correct user and file permissions."
        elif error_type == "Git Error":
            return "Git operation failed. Check repository URL and credentials."
        elif error_type == "Compilation Error":
            return "Compilation failed. Review syntax and dependencies."
        return "Unknown root cause."

    def _suggest_fixes(self, error_type: str) -> List[str]:
        suggestions = {
            "Dependency Error": ["Check package versions.", "Verify network connectivity.", "Clear cache and retry."],
            "Test Failure": ["Review test output.", "Fix failing tests.", "Check test dependencies."],
            "Docker Error": ["Check Dockerfile syntax.", "Verify Docker daemon is running.", "Check user permissions."],
            "Permission Error": ["Run as correct user.", "Check file permissions.", "Avoid using sudo unnecessarily."],
            "Git Error": ["Check repository URL.", "Verify credentials.", "Check network access."],
            "Compilation Error": ["Fix syntax errors.", "Check dependencies.", "Review compiler output."]
        }
        return suggestions.get(error_type, ["No suggestions available."])

    def _extract_stage(self, log: str) -> str:
        stage_match = re.search(r"stage\s*\(\s*['\"]?([\w\s]+)['\"]?\s*\)", log, re.I)
        if stage_match:
            return stage_match.group(1)
        return "Unknown"
