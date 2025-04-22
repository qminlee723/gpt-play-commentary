document.addEventListener("DOMContentLoaded", () => {
  const logBox = document.getElementById("logOutput");
  const loadBtn = document.getElementById("loadBtn");
  const summarizeBtn = document.getElementById("summarizeBtn");

  // 초기화 메시지
  logBox.textContent =
    "[공연 데이터 수집] 버튼을 클릭 후 ⭐️작업이 완료되면⭐️ 그 후에 GPT 요약 실행 버튼을 클릭 해 주세요\n";

  loadBtn.addEventListener("click", async (e) => {
    try {
      logBox.textContent = "📥 공연 데이터 수집 요청 중...\n";

      const res = await fetch("http://127.0.0.1:5050/run");
      const data = await res.json();

      // 수집 완료 후 로그를 다시 가져옴
      const log = await fetch("http://127.0.0.1:5050/log").then((res) =>
        res.text()
      );
      logBox.textContent = log;
    } catch (err) {
      logBox.textContent =
        "❌ 공연 호출 실패! Backend 서버가 켜졌는지 다시 한번 확인하세요. `python flask_server.py`\n";
      console.error(err);
    }
  });

  summarizeBtn?.addEventListener("click", async () => {
    logBox.textContent += "\n[🧠 GPT 요약 요청 중...]\n";
    try {
      const res = await fetch("http://127.0.0.1:5050/summarize");
      const data = await res.json();
      logBox.textContent += `[✅ 응답] ${data.message}\n`;
    } catch (err) {
      logBox.textContent += "❌ /summarize 호출 실패\n";
      console.error(err);
    }
  });
});

document.addEventListener("DOMContentLoaded", async () => {
  const downloadDiv = document.getElementById("downloadLinks");

  try {
    const res = await fetch("http://127.0.0.1:5050/list-downloads");
    const files = await res.json();

    if (files.length === 0) {
      downloadDiv.innerHTML = "<p>📂 다운로드 가능한 파일이 없습니다.</p>";
      return;
    }

    const ul = document.createElement("ul");
    files.forEach((file) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `http://127.0.0.1:5050/download/${file}`;
      a.download = file;
      a.textContent = `💾 ${file}`;
      li.appendChild(a);
      ul.appendChild(li);
    });

    downloadDiv.appendChild(ul);
  } catch (err) {
    console.error("파일 목록 로드 실패:", err);
    downloadDiv.innerHTML = "<p>⚠️ 파일 목록을 불러오지 못했습니다.</p>";
  }
});
