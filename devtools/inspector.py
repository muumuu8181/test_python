import ast
import subprocess
import sys
import os
import argparse
import json
from dataclasses import dataclass
from typing import List, Optional, Callable
from shutil import which


@dataclass
class Issue:
    """Represents a code quality issue found by a tool."""
    tool: str
    file: str
    line: int
    message: str
    severity: str  # 'CRITICAL', 'WARNING', 'INFO'


class CodeInspector(ast.NodeVisitor):
    """Internal AST-based code inspector."""

    def __init__(self, filename):
        self.filename = filename
        self.issues = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        # Check Docstring
        if not ast.get_docstring(node):
            self.issues.append(Issue(
                tool='InternalAST',
                file=self.filename,
                line=node.lineno,
                message=f"Missing docstring in function '{node.name}'",
                severity='WARNING'
            ))

        # Check Argument Count
        arg_count = len(node.args.args)
        if arg_count > 5:
            self.issues.append(Issue(
                tool='InternalAST',
                file=self.filename,
                line=node.lineno,
                message=f"Function '{node.name}' has too many arguments ({arg_count} > 5)",
                severity='WARNING'
            ))

        # Check Nesting Depth
        self.check_nesting(node, 0)

        self.generic_visit(node)
        self.current_function = None

    def check_nesting(self, node, current_depth):
        """Recursively checks nesting depth."""
        if current_depth > 3:
            self.issues.append(Issue(
                tool='InternalAST',
                file=self.filename,
                line=node.lineno if hasattr(node, 'lineno') else 0,
                message=f"High nesting depth ({current_depth}) in function '{self.current_function}'",
                severity='WARNING'
            ))
            return

        for name, field in ast.iter_fields(node):
            if isinstance(field, list):
                for item in field:
                    if isinstance(item, ast.AST):
                        if isinstance(item, (ast.For, ast.While, ast.If, ast.With, ast.Try)):
                            self.check_nesting(item, current_depth + 1)
                        else:
                            self.check_nesting(item, current_depth)
            elif isinstance(field, ast.AST):
                if isinstance(field, (ast.For, ast.While, ast.If, ast.With, ast.Try)):
                    self.check_nesting(field, current_depth + 1)
                else:
                    self.check_nesting(field, current_depth)

    def visit_ClassDef(self, node):
        if not ast.get_docstring(node):
            self.issues.append(Issue(
                tool='InternalAST',
                file=self.filename,
                line=node.lineno,
                message=f"Missing docstring in class '{node.name}'",
                severity='WARNING'
            ))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec']:
                self.issues.append(Issue(
                    tool='InternalAST',
                    file=self.filename,
                    line=node.lineno,
                    message=f"Dangerous function call used: '{node.func.id}'",
                    severity='CRITICAL'
                ))
        self.generic_visit(node)


class QualityTool:
    """Main quality assurance tool orchestrator."""

    def __init__(self, target_path):
        self.target_path = target_path
        self.issues = []

    def run_ast_check(self, filepath):
        """Runs internal AST checks."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content, filename=filepath)
            inspector = CodeInspector(filepath)
            inspector.visit(tree)
            self.issues.extend(inspector.issues)
        except SyntaxError as e:
            self.issues.append(Issue(
                tool='InternalAST',
                file=filepath,
                line=e.lineno,
                message=f"Syntax Error: {e.msg}",
                severity='CRITICAL'
            ))
        except Exception as e:
            self.issues.append(Issue(
                tool='InternalAST',
                file=filepath,
                line=0,
                message=f"Failed to parse: {str(e)}",
                severity='CRITICAL'
            ))

    def run_command(self, command: List[str], tool_name: str, parse_func: Optional[Callable]):
        """Runs an external command and parses its output."""
        if not self._is_tool_installed(command[0]):
            return

        try:
            # Run without check=True so we capture output even on exit code 1
            result = subprocess.run(command, capture_output=True, text=True)
            if parse_func:
                parse_func(result.stdout, result.stderr)
        except Exception as e:
            self.issues.append(Issue(
                tool=tool_name,
                file=self.target_path,
                line=0,
                message=f"Failed to run {tool_name}: {str(e)}",
                severity='WARNING'
            ))

    def _is_tool_installed(self, tool):
        return which(tool) is not None

    def parse_flake8(self, stdout, stderr):
        """Parses Flake8 output."""
        for line in stdout.splitlines():
            parts = line.split(':')
            if len(parts) >= 4:
                file = parts[0]
                try:
                    line_no = int(parts[1])
                except ValueError:
                    line_no = 0
                message = ':'.join(parts[3:]).strip()
                self.issues.append(Issue(tool='flake8', file=file, line=line_no, message=message, severity='WARNING'))

    def parse_mypy(self, stdout, stderr):
        """Parses Mypy output."""
        for line in stdout.splitlines():
            if "error:" in line:
                parts = line.split(':')
                # mypy output: file:line: error: message
                if len(parts) >= 3:
                    file = parts[0]
                    try:
                        line_no = int(parts[1])
                    except ValueError:
                        line_no = 0

                    # Extract message
                    msg_part = line.split('error:', 1)
                    if len(msg_part) > 1:
                        message = msg_part[1].strip()
                    else:
                        message = line

                    self.issues.append(Issue(tool='mypy', file=file, line=line_no, message=message, severity='WARNING'))

    def parse_bandit(self, stdout, stderr):
        """Parses Bandit JSON output."""
        try:
            data = json.loads(stdout)
            if 'results' in data:
                for res in data['results']:
                    self.issues.append(Issue(
                        tool='bandit',
                        file=res['filename'],
                        line=res['line_number'],
                        message=f"{res['issue_text']} ({res['test_id']})",
                        severity=res['issue_severity'].upper()
                    ))
        except json.JSONDecodeError:
            pass

    def parse_radon(self, stdout, stderr):
        """Parses Radon JSON output."""
        try:
            data = json.loads(stdout)
            for filename, metrics in data.items():
                for m in metrics:
                    complexity = m['complexity']
                    if complexity > 10:
                        self.issues.append(Issue(
                            tool='radon',
                            file=filename,
                            line=m['lineno'],
                            message=f"High Cyclomatic Complexity: {complexity} ({m['rank']}) in '{m['name']}'",
                            severity='WARNING' if complexity < 20 else 'CRITICAL'
                        ))
        except json.JSONDecodeError:
            pass

    def run(self):
        """Runs all checks."""
        # 1. Internal AST Check
        files_to_check = []
        if os.path.isfile(self.target_path):
            files_to_check.append(self.target_path)
        else:
            for root, dirs, files in os.walk(self.target_path):
                for file in files:
                    if file.endswith('.py'):
                        files_to_check.append(os.path.join(root, file))

        for f in files_to_check:
            self.run_ast_check(f)

        # 2. External Tools
        # Flake8
        self.run_command(['flake8', self.target_path], 'flake8', self.parse_flake8)

        # Mypy
        self.run_command(['mypy', self.target_path, '--ignore-missing-imports', '--show-error-codes'], 'mypy', self.parse_mypy)

        # Bandit
        self.run_command(['bandit', '-r', self.target_path, '-f', 'json'], 'bandit', self.parse_bandit)

        # Radon
        self.run_command(['radon', 'cc', self.target_path, '-j'], 'radon', self.parse_radon)

    def report(self):
        """Prints the quality report."""
        print(f"=== Quality Report for {self.target_path} ===\n")

        if not self.issues:
            print("No issues found! Great job.")
            return

        # Sort issues by severity then file then line
        severity_order = {'CRITICAL': 0, 'WARNING': 1, 'INFO': 2}
        sorted_issues = sorted(self.issues, key=lambda x: (severity_order.get(x.severity, 3), x.file, x.line))

        by_tool = {}
        for issue in sorted_issues:
            by_tool.setdefault(issue.tool, []).append(issue)

        for tool, issues in by_tool.items():
            print(f"--- {tool.upper()} ({len(issues)} issues) ---")
            for issue in issues:
                print(f"[{issue.severity}] {issue.file}:{issue.line} - {issue.message}")
            print("")

        print("=== End Report ===")


def main():
    parser = argparse.ArgumentParser(description="Comprehensive Python Quality Inspector")
    parser.add_argument("target", help="File or directory to inspect")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Error: Target '{args.target}' does not exist.")
        sys.exit(1)

    tool = QualityTool(args.target)
    tool.run()
    tool.report()


if __name__ == "__main__":
    main()
