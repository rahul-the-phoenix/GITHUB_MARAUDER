#!/usr/bin/env python3
"""
GitHub Repository Editor
- edit digit N        : picks one digit and changes it N times
- edit commentout N   : picks a random comment line each time, edits N times
- edit line N         : picks one line and changes its content N times
- edit word N         : picks one word and replaces it N times
Each edit is committed and pushed to GitHub separately.
"""

import subprocess
import socket
import time
import random
import re
from pathlib import Path


class GitHubRepoEditor:
    def __init__(self, repo_url, local_path="./github_repo"):
        self.repo_url = repo_url
        self.local_path = Path(local_path)

    # ---------- NETWORK ----------
    def check_network_connection(self):
        """Check if an internet connection is available."""
        try:
            socket.create_connection(("github.com", 443), timeout=5)
            return True
        except (socket.timeout, socket.error, OSError):
            return False

    # ---------- CLONE / PULL ----------
    def ensure_repo_cloned(self):
        """Clone the repo if missing, otherwise pull latest changes."""
        if not self.local_path.exists():
            print(f"Cloning repository into {self.local_path}...")
            try:
                subprocess.run(
                    ["git", "clone", self.repo_url, str(self.local_path)],
                    check=True, capture_output=True, text=True
                )
                print("Repository cloned successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Clone error: {e.stderr}")
                return False
        else:
            try:
                subprocess.run(
                    ["git", "-C", str(self.local_path), "pull"],
                    check=True, capture_output=True, text=True
                )
            except subprocess.CalledProcessError:
                pass
        return True

    # ---------- FILE ----------
    def find_editable_file(self):
        """Find a suitable file to edit inside the repository."""
        extensions = ['.txt', '.md', '.py', '.js', '.html', '.css']
        for ext in extensions:
            files = list(self.local_path.rglob(f"*{ext}"))
            if files:
                return files[0]

        # If no file exists, create a sample one
        new_file = self.local_path / "editable_file.txt"
        new_file.write_text(
            "Hello 1 world this is sample text\n"
            "# old comment one\n"
            "# old comment two\n"
            "first line content\n"
            "second line content\n"
        )
        return new_file

    # ---------- COMMIT & PUSH ----------
    def commit_and_push(self, message):
        """Stage, commit and push changes. Called after every single edit."""
        try:
            subprocess.run(
                ["git", "-C", str(self.local_path), "add", "."],
                check=True, capture_output=True, text=True
            )

            result = subprocess.run(
                ["git", "-C", str(self.local_path), "commit", "-m", message],
                capture_output=True, text=True
            )

            if result.returncode != 0:
                if "nothing to commit" in (result.stdout + result.stderr):
                    return False, "nothing to commit"
                return False, f"Commit error: {result.stderr}"

            subprocess.run(
                ["git", "-C", str(self.local_path), "push"],
                check=True, capture_output=True, text=True
            )
            return True, "pushed successfully"

        except subprocess.CalledProcessError as e:
            return False, f"Git error: {e.stderr}"

    # ---------- EDIT DIGIT ----------
    def edit_digit(self, file_path, count):
        """Pick one digit and change its value `count` times.
        Each change is committed and pushed."""
        with open(file_path, 'r') as f:
            content = f.read()

        digits = list(re.finditer(r'\d', content))
        if not digits:
            return False, "No digit found in the file to edit."

        # Pick ONE digit at random
        target = random.choice(digits)
        target_pos = target.start()
        current_digit = target.group()
        print(f"   Target digit: '{current_digit}' at position {target_pos}")

        success_count = 0
        for i in range(count):
            # Choose a different digit
            new_digit = random.choice([d for d in '0123456789' if d != current_digit])

            with open(file_path, 'r') as f:
                content = f.read()

            content = content[:target_pos] + new_digit + content[target_pos + 1:]

            with open(file_path, 'w') as f:
                f.write(content)

            ok, msg = self.commit_and_push(
                f"Edit digit: {current_digit} -> {new_digit} ({i+1}/{count})"
            )
            if ok:
                success_count += 1
                print(f"   [{i+1}/{count}] {current_digit} -> {new_digit}  ({msg})")
            else:
                print(f"   [{i+1}/{count}] Failed: {msg}")

            current_digit = new_digit
            time.sleep(0.5)  # small delay to avoid GitHub API rate issues

        return True, f"One digit was changed {success_count} time(s)."

    # ---------- EDIT COMMENTOUT ----------
    def edit_commentout(self, file_path, count):
        """Pick a random commented line each iteration and edit it.
        Each edit is committed and pushed."""
        success_count = 0

        for i in range(count):
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # Find commented lines (supports #, //, --)
            comment_indexes = [
                idx for idx, line in enumerate(lines)
                if line.lstrip().startswith(('#', '//', '--'))
            ]

            if not comment_indexes:
                if i == 0:
                    return False, "No commented line found in the file."
                break

            idx = random.choice(comment_indexes)

            stripped = lines[idx].lstrip()
            if stripped.startswith('//'):
                prefix = '//'
            elif stripped.startswith('--'):
                prefix = '--'
            else:
                prefix = '#'

            new_line = (
                f"{prefix} edited comment {random.randint(1000, 9999)} "
                f"at {time.strftime('%H:%M:%S')}\n"
            )
            lines[idx] = new_line

            with open(file_path, 'w') as f:
                f.writelines(lines)

            ok, msg = self.commit_and_push(
                f"Edit commentout: line {idx+1} ({i+1}/{count})"
            )
            if ok:
                success_count += 1
                print(f"   [{i+1}/{count}] line {idx+1} -> '{new_line.strip()}'  ({msg})")
            else:
                print(f"   [{i+1}/{count}] Failed: {msg}")

            time.sleep(0.5)

        return True, f"A random comment line was edited {success_count} time(s)."

    # ---------- EDIT LINE ----------
    def edit_line(self, file_path, count):
        """Pick one line and change its content `count` times.
        Each change is committed and pushed."""
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            return False, "The file is empty."

        target_idx = random.randrange(len(lines))
        print(f"   Target line: {target_idx+1} -> '{lines[target_idx].strip()}'")

        success_count = 0
        for i in range(count):
            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_content = (
                f"Edited line {target_idx+1} time {i+1} "
                f"-> value {random.randint(100, 999)}\n"
            )
            lines[target_idx] = new_content

            with open(file_path, 'w') as f:
                f.writelines(lines)

            ok, msg = self.commit_and_push(
                f"Edit line {target_idx+1} ({i+1}/{count})"
            )
            if ok:
                success_count += 1
                print(f"   [{i+1}/{count}] {new_content.strip()}  ({msg})")
            else:
                print(f"   [{i+1}/{count}] Failed: {msg}")

            time.sleep(0.5)

        return True, f"One line was changed {success_count} time(s)."

    # ---------- EDIT WORD ----------
    def edit_word(self, file_path, count):
        """Pick one word and replace it `count` times.
        Each replacement is committed and pushed."""
        with open(file_path, 'r') as f:
            content = f.read()

        words = list(re.finditer(r'\b[a-zA-Z]{2,}\b', content))
        if not words:
            return False, "No word found in the file."

        target = random.choice(words)
        target_start = target.start()
        target_end = target.end()
        current_word = target.group()
        print(f"   Target word: '{current_word}' at position {target_start}")

        pool = ['alpha', 'bravo', 'charlie', 'delta', 'echo',
                'foxtrot', 'golf', 'hotel', 'india', 'juliet',
                'kilo', 'lima', 'mike', 'november', 'oscar']

        success_count = 0
        for i in range(count):
            new_word = random.choice([w for w in pool if w != current_word])

            with open(file_path, 'r') as f:
                content = f.read()

            content = content[:target_start] + new_word + content[target_end:]

            with open(file_path, 'w') as f:
                f.write(content)

            ok, msg = self.commit_and_push(
                f"Edit word: {current_word} -> {new_word} ({i+1}/{count})"
            )
            if ok:
                success_count += 1
                print(f"   [{i+1}/{count}] {current_word} -> {new_word}  ({msg})")
            else:
                print(f"   [{i+1}/{count}] Failed: {msg}")

            # Update position tracking for the next replacement
            target_end = target_start + len(new_word)
            current_word = new_word
            time.sleep(0.5)

        return True, f"One word was replaced {success_count} time(s)."

    # ---------- COMMAND PROCESS ----------
    def process_command(self, command):
        parts = command.strip().split()

        if len(parts) != 3 or parts[0].lower() != "edit":
            return False, "Invalid format. Use: edit <type> <count>"

        edit_type = parts[1].lower()
        try:
            count = int(parts[2])
        except ValueError:
            return False, "Count must be a number."

        if count <= 0 or count > 100:
            return False, "Count must be between 1 and 100."

        file_path = self.find_editable_file()
        if not file_path:
            return False, "No editable file found."

        if edit_type == "digit":
            return self.edit_digit(file_path, count)
        elif edit_type == "commentout":
            return self.edit_commentout(file_path, count)
        elif edit_type == "line":
            return self.edit_line(file_path, count)
        elif edit_type == "word":
            return self.edit_word(file_path, count)
        else:
            return False, f"Unknown edit type: {edit_type}"


# ============ MAIN ============
def main():
    # ⚠️ PUT YOUR REPOSITORY URL HERE
    REPO_URL = "https://github.com/yourusername/your-repo.git"

    if "yourusername" in REPO_URL:
        print("Please update REPO_URL in the script with your actual repository URL.")
        return

    editor = GitHubRepoEditor(REPO_URL)

    print("=" * 55)
    print(" GitHub Repository Editor (per-edit commit mode)")
    print("=" * 55)
    print("\nAvailable commands:")
    print("  edit digit <N>       - change one digit N times")
    print("  edit commentout <N>  - edit a random comment line N times")
    print("  edit line <N>        - change one line N times")
    print("  edit word <N>        - replace one word N times")
    print("  quit / exit          - exit the program")
    print("=" * 55)

    if not editor.check_network_connection():
        print("\nNo network connection... Please connect!")
        return

    print("\nNetwork connection established.")

    if not editor.ensure_repo_cloned():
        print("Failed to clone the repository.")
        return

    print(f"Repository ready at: {editor.local_path}")
    print("\nReady for commands!\n")

    while True:
        try:
            command = input("github-editor> ").strip()
            if not command:
                continue
            if command.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not editor.check_network_connection():
                print("No network connection... Please connect!")
                continue

            success, message = editor.process_command(command)
            print(f"\n{'[OK]' if success else '[FAIL]'} {message}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
