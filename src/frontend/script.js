document.addEventListener("DOMContentLoaded", () => {
  const logBox = document.getElementById("logOutput");
  const loadBtn = document.getElementById("loadBtn");
  const summarizeBtn = document.getElementById("summarizeBtn");
  const downloadDiv = document.getElementById("downloadLinks");

  function getYesterdayDateString() {
    const today = new Date();
    today.setDate(today.getDate() - 1);
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  // 어제 날짜로 startDate와 endDate 초기값 세팅
  const yesterdayStr = getYesterdayDateString();
  document.getElementById("startDate").value = yesterdayStr;
  // document.getElementById("endDate").value = yesterdayStr;
  let previousLog = "";
  let loadingMessage = "";
  let logInterval;
  let anim;

  // 초기화 메시지
  logBox.textContent =
    "[공연 데이터 수집] 버튼을 클릭 후 ⭐️작업이 완료되면⭐️ 그 후에 GPT 요약 실행 버튼을 클릭 해 주세요\n";

  const startLoadingAnimation = () => {
    let dotCount = 0;
    // loadingMessage = "📥 공연 데이터 수집 중";

    anim = setInterval(() => {
      dotCount = (dotCount + 1) % 4;
      const dots = ".".repeat(dotCount);
      loadingMessage = `📥 공연 데이터 수집 중${dots}`;
      logBox.textContent = `${loadingMessage}\n\n${previousLog}`;
      logBox.scrollTop = logBox.scrollHeight;
    }, 500);
  };

  const startSummarizingAnimation = () => {
    let dotCount = 0;
    loadingMessage = "📥 공연 데이터 수집 중";

    anim = setInterval(() => {
      dotCount = (dotCount + 1) % 4;
      const dots = ".".repeat(dotCount);
      loadingMessage = `🤖 공연 데이터 요약 중${dots}`;
      logBox.textContent = `${loadingMessage}\n\n${previousLog}`;
      logBox.scrollTop = logBox.scrollHeight;
    }, 500);
  };

  const stopLoadingAnimation = () => {
    clearInterval(anim);
  };

  const startLogFetching = () => {
    logInterval = setInterval(async () => {
      try {
        const log = await fetch("http://127.0.0.1:5050/log").then((res) =>
          res.text()
        );

        if (log !== previousLog) {
          previousLog = log;
          logBox.textContent = `${loadingMessage}\n\n${previousLog}`;
          logBox.scrollTop = logBox.scrollHeight;
        }
      } catch (err) {
        console.error("로그 업데이트 실패:", err);
      }
    }, 1000);
  };

  const stopLogFetching = () => {
    clearInterval(logInterval);
  };

  // 공연 데이터 수집 버튼
  loadBtn.addEventListener("click", async () => {
    loadBtn.disabled = true;
    loadBtn.textContent = "⏳ 수집중...";

    try {
      startLoadingAnimation();
      startLogFetching();

      const start_date = document
        .getElementById("startDate")
        .value.replace(/-/g, "");
      const end_date = document
        .getElementById("endDate")
        .value.replace(/-/g, "");

      if (!start_date || !end_date) {
        alert("시작일과 종료일을 선택해주세요!");
        stopLoadingAnimation();
        stopLogFetching();
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

      stopLoadingAnimation();
      stopLogFetching();

      const finalLog = await fetch("http://127.0.0.1:5050/log").then((res) =>
        res.text()
      );
      previousLog = finalLog;
      logBox.textContent = `${loadingMessage}\n\n${previousLog}`;
      logBox.scrollTop = logBox.scrollHeight;

      await updateFileList();
    } catch (err) {
      stopLoadingAnimation();
      stopLogFetching();
      logBox.textContent =
        "❌ 공연 호출 실패! Backend 서버가 켜졌는지 다시 한번 확인하세요. `python flask_server.py`\n";
      console.error(err);
    } finally {
      loadBtn.disabled = false;
      loadBtn.textContent = "📥 공연 데이터 수집";
    }
  });

  // GPT 요약 버튼
  summarizeBtn?.addEventListener("click", async () => {
    // logBox.textContent += "\n[🧠 GPT 요약 요청 중...]\n";

    summarizeBtn.disabled = true;
    summarizeBtn.textContent = "⏳ 요약중...";

    try {
      startSummarizingAnimation();
      startLogFetching();

      const res = await fetch("http://127.0.0.1:5050/summarize");
      const data = await res.json();
      logBox.textContent += `[✅ 응답] ${data.message}\n`;
      await updateFileList();
    } catch (err) {
      logBox.textContent += "❌ /summarize 호출 실패\n";
      stopLogFetching();
      stopLoadingAnimation();

      console.error(err);
    }

    stopLogFetching();
    stopLoadingAnimation();
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
    } finally {
      summarizeBtn.disabled = false;
      summarizeBtn.textContent = "🤖 GPT 요약 실행";
    }
  }

  // 페이지 로딩될 때 파일 목록 업데이트
  updateFileList();
});
