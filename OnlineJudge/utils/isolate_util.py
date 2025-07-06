import subprocess
import os
from models.language import Language
from sqlalchemy.orm import Session

class CompilationError(Exception):
    pass

class UnsupportedLanguageError(Exception):
    pass

class RuntimeExecutionError(Exception):
    pass

class IsolateUtil:
    def __init__(self, box_id: int = 0):
        self.box_id = box_id
        self.box_path = f"/var/local/lib/isolate/{self.box_id}/box"

    def init_sandbox(self):
        cmd = f"isolate --box-id={self.box_id} --init"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)

    def cleanup(self):
        cmd = f"isolate --box-id={self.box_id} --cleanup"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)

    def run_code(self, language_id: int, source_code: str, input_data: str, time_limit: int, memory_limit: int, db_session: Session):
        # 1. Lấy thông tin ngôn ngữ
        lang: Language = db_session.query(Language).filter(Language.id == language_id).first()
        if not lang:
            raise UnsupportedLanguageError("Language not found")

        file_name = f"Main{lang.file_ext}"
        file_path = os.path.join(self.box_path, file_name)

        # 2. Ghi code vào file trong sandbox
        with open(file_path, "w") as f:
            f.write(source_code)

        # 3. Ghi input vào file nếu có
        input_file = os.path.join(self.box_path, "input.txt")
        with open(input_file, "w") as f:
            f.write(input_data if input_data is not None else "")
        # 4. Biên dịch nếu cần
        if lang.judge_key in ["/usr/bin/g++", "/usr/bin/gcc"]:
            compile_cmd = (
                f"isolate --box-id={self.box_id} --mem=1048576 --processes=50 "
                f"--dir=/usr/bin --dir=/bin "
                f"--dir=/lib --dir=/lib64 --dir=/usr/lib "
                f"--dir=/usr/libexec --dir=/usr/lib/gcc --dir=/usr/lib/x86_64-linux-gnu "
                f"--dir=/usr/libexec/gcc/x86_64-linux-gnu/13 "
                f"--dir=/usr/lib/gcc/x86_64-linux-gnu/13 "
                f"--env=PATH=/usr/bin:/bin --env=LD_LIBRARY_PATH=/lib:/lib64:/usr/lib "
                f"--run -- {lang.judge_key} {file_name} -o program"
            )       
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise CompilationError(result.stderr)
            exec_cmd = f"./program"
        elif lang.judge_key == "javac":
            compile_cmd = f"isolate --box-id={self.box_id} --run -- javac {file_name}"
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise CompilationError(result.stderr)
            exec_cmd = f"java Main"
        elif lang.judge_key in ["/usr/bin/python3", "/usr/bin/node"]:
            exec_cmd = f"{lang.judge_key} {file_name}"
        else:
            raise UnsupportedLanguageError("Judge key not supported")

        # 5. Thực thi code trong isolate
        mem_limit = max(memory_limit * 1024, 524288)  # ít nhất 512MB
        run_cmd = (
            f"isolate --box-id={self.box_id} "
            f"--time={time_limit} --mem={mem_limit} "
            f"--processes=10 "
            f"--stdin=input.txt --stdout=output.txt --run -- {exec_cmd}"
        )
        result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeExecutionError(result.stderr)

        # 6. Đọc output
        output_file = os.path.join(self.box_path, "output.txt")
        output = ""
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                output = f.read()

        return {
            "status": "Accepted",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output": output
        }