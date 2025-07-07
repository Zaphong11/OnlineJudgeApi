require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
let editor;
require(['vs/editor/editor.main'], function () {
    editor = monaco.editor.create(document.getElementById('editor'), {
        value: '',
        language: 'cpp',
        theme: 'vs-dark',
        automaticLayout: true,
        fontSize: 16,
    });
});

const langMap = {
    cpp: 2,
    c: 3,
    python: 1,
    javascript: 5
};
const monacoLangMap = {
    cpp: 'cpp',
    c: 'c',
    python: 'python',
    javascript: 'javascript'
};

document.getElementById('language').onchange = function () {
    const lang = document.getElementById('language').value;
    if (editor && monacoLangMap[lang]) {
        monaco.editor.setModelLanguage(editor.getModel(), monacoLangMap[lang]);
    }
};

document.getElementById('run-btn').onclick = async function () {
    const code = editor ? editor.getValue() : '';
    const input = document.getElementById('input').value;
    const output = document.getElementById('expected-output').value || "";
    const language = document.getElementById('language').value;
    const language_id = langMap[language];
    const time_limit = 1000;
    const memory_limit = 256;

    const payload = {
        language_id,
        code,
        input,
        output,
        time_limit,
        memory_limit
    };

    document.getElementById('result').value = "Đang chấm...";

    try {
        const res = await fetch('http://127.0.0.1:8000/api/submissions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        // Nếu backend trả về id/submission_id, tự động lấy kết quả chi tiết
        const submissionId = data.id || data.submission_id;
        if (submissionId) {
            // Gọi API lấy kết quả chi tiết chỉ với output
            const resultRes = await fetch(`http://127.0.0.1:8000/api/results/${submissionId}`);
            const resultData = await resultRes.json();
            let resultText = "";
            // Hiển thị status nếu có
            if (typeof resultData.status !== "undefined" && resultData.status !== null) {
                resultText += "Status: " + resultData.status + "\n";
            }
            resultText += "Output: " + (typeof resultData.output !== "undefined" ? resultData.output : "(no output)") + "\n";
            document.getElementById('result').value = resultText;
        }
        else {
            // Fallback: vẫn hiển thị kết quả từ /submissions nếu không có id
            let resultText = "";
            resultText += "Output: " + (typeof data.output !== "undefined" ? data.output : "(no output)") + "\n";
            if (typeof data.status !== "undefined" && data.status !== null) {
                resultText += "Status: " + data.status + "\n";
            }
            if (data.stderr) {
                resultText += "Error: " + data.stderr + "\n";
            }
            document.getElementById('result').value = resultText;
        }
    } catch (err) {
        document.getElementById('result').value = "Lỗi kết nối server!";
    }
};