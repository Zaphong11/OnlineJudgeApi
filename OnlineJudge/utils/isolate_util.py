import subprocess
import os
from typing import Dict
from models.language import Language
from sqlalchemy.orm import Session


class CompilationError(Exception):
    pass


class UnsupportedLanguageError(Exception):
    pass


class IsolateUtil:
    def __init__(self, box_id: int = 0):
        self.box_id = box_id
        self.box_path = f"/var/local/lib/isolate/{self.box_id}/box/"

    def init_sandbox(self):
        """Initialize the sandbox environment"""
        cmd = f"isolate --box-id={self.box_id} --init"
        try:
            return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to initialize sandbox: {str(e)}")

    def cleanup(self):
        """Clean up the sandbox environment"""
        cmd = f"isolate --box-id={self.box_id} --cleanup"
        try:
            return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to cleanup sandbox: {str(e)}")

    def _get_run_command(self, language_id: int, db_session: Session) -> str:
        """Get the appropriate run command based on language configuration"""
        lang_config = db_session.query(Language).filter(Language.id == language_id).first()
        if not lang_config:
            raise UnsupportedLanguageError(f"Language ID {language_id} not found in database")

        file_name = f"code{lang_config.file_ext}"
        file_path = f"{self.box_path}/{file_name}"

        # Handle compiled languages
        if lang_config.judge_key in ["g++", "gcc", "javac"]:
            if lang_config.judge_key in ["g++", "gcc"]:
                compile_cmd = [
                    lang_config.judge_key,
                    file_path,
                    "-o",
                    f"{self.box_path}/program"
                ]
                try:
                    subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
                    return "./program"
                except subprocess.CalledProcessError as e:
                    raise CompilationError(f"Compilation failed: {e.stderr}")

            elif lang_config.judge_key == "javac":
                compile_cmd = [
                    "javac",
                    file_path
                ]
                try:
                    subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
                    return "java Main"
                except subprocess.CalledProcessError as e:
                    raise CompilationError(f"Java compilation failed: {e.stderr}")

        # Handle interpreted languages
        return f"{lang_config.judge_key} {file_name}"

    def run_code(self,
                 language_id: int,
                 source_code: str,
                 input_data: str,
                 time_limit: float,
                 memory_limit: int,
                 db_session: Session) -> Dict:
        """Execute code in the sandbox environment"""
        try:
            # Get language configuration and prepare file
            lang_config = db_session.query(Language).filter(Language.id == language_id).first()
            if not lang_config:
                return {"status": "error", "error": f"Language ID {language_id} not found"}

            file_name = f"code{lang_config.file_ext}"

            # Write source code
            with open(f"{self.box_path}/{file_name}", "w") as f:
                f.write(source_code)

            # Write input data if provided
            if input_data:
                with open(f"{self.box_path}/input.txt", "w") as f:
                    f.write(input_data)

            # Prepare execution command
            try:
                run_cmd = self._get_run_command(language_id, db_session)
            except CompilationError as e:
                return {"status": "compilation_error", "error": str(e)}

            # Execute in sandbox
            cmd = [
                "isolate",
                f"--box-id={self.box_id}",
                f"--time={time_limit}",
                f"--wall-time={time_limit * 2}",
                f"--memory={memory_limit * 1024}",
                "--stdin=input.txt",
                "--stdout=output.txt",
                "--stderr=error.txt",
                "--run",
                run_cmd
            ]

            # Run the command
            process = subprocess.run(cmd, capture_output=True, text=True)

            # Read output and error if available
            try:
                with open(f"{self.box_path}/output.txt", "r") as f:
                    output = f.read()
            except FileNotFoundError:
                output = ""

            try:
                with open(f"{self.box_path}/error.txt", "r") as f:
                    error = f.read()
            except FileNotFoundError:
                error = ""

            # Check execution result
            if process.returncode == 0:
                return {
                    "status": "success",
                    "output": output,
                    "error": error
                }
            else:
                return {
                    "status": "runtime_error",
                    "output": output,
                    "error": error
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }