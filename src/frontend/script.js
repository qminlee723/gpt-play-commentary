document.addEventListener("DOMContentLoaded", () => {
  const logBox = document.getElementById("logOutput");
  const loadBtn = document.getElementById("loadBtn");
  const summarizeBtn = document.getElementById("summarizeBtn");
  const downloadDiv = document.getElementById("downloadLinks");

  // 초기화 메시지
  logBox.textContent =
    "[공연 데이터 수집] 버튼을 클릭 후 ⭐️작업이 완료되면⭐️ 그 후에 GPT 요약 실행 버튼을 클릭 해 주세요\n";

  // 공연 데이터 수집 버튼
  loadBtn.addEventListener("click", async () => {
    let dotCount = 0;
    let anim;

    const startLoadingAnimation = () => {
      anim = setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        const dots = ".".repeat(dotCount);
        logBox.textContent = `📥 공연 데이터 수집 중${dots}`;
      }, 500);
    };

    const stopLoadingAnimation = () => {
      clearInterval(anim);
    };

    try {
      startLoadingAnimation();

      const start_date = document
        .getElementById("startDate")
        .value.replace(/-/g, "");
      const end_date = document
        .getElementById("endDate")
        .value.replace(/-/g, "");

      if (!start_date || !end_date) {
        alert("시작일과 종료일을 선택해주세요!");
        stopLoadingAnimation();
        return;
      }

      const res = await fetch("http://127.0.0.1:5050/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ start_date, end_date }),
      });

      const data = await res.json();

      const log = await fetch("http://127.0.0.1:5050/log").then((res) =>
        res.text()
      );

      stopLoadingAnimation();
      logBox.textContent = log;

      await updateFileList();
    } catch (err) {
      stopLoadingAnimation();
      logBox.textContent =
        "❌ 공연 호출 실패! Backend 서버가 켜졌는지 다시 한번 확인하세요. `python flask_server.py`\n";
      console.error(err);
    }
  });

  // GPT 요약 버튼
  summarizeBtn?.addEventListener("click", async () => {
    logBox.textContent += "\n[🧠 GPT 요약 요청 중...]\n";
    try {
      const res = await fetch("http://127.0.0.1:5050/summarize");
      const data = await res.json();
      logBox.textContent += `[✅ 응답] ${data.message}\n`;
      await updateFileList();
    } catch (err) {
      logBox.textContent += "❌ /summarize 호출 실패\n";
      console.error(err);
    }
  });

  // 파일 목록 업데이트 함수
  async function updateFileList() {
    downloadDiv.innerHTML = "<h2>📁 파일 목록</h2>";

    try {
      const res = await fetch("http://127.0.0.1:5050/list-downloads");
      const files = await res.json();

      if (files.length === 0) {
        downloadDiv.innerHTML += "<p>📂 다운로드 가능한 파일이 없습니다.</p>";
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
      downloadDiv.innerHTML += "<p>⚠️ 파일 목록을 불러오지 못했습니다.</p>";
    }
  }

  // 페이지 로딩될 때 파일 목록 업데이트
  updateFileList();
});
