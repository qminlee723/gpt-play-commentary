document.addEventListener("DOMContentLoaded", () => {
  const logBox = document.getElementById("logOutput");
  const loadBtn = document.getElementById("loadBtn");

  logBox.textContent = "[📡 로그 스트리밍 시작됨...]\n";

  const eventSource = new EventSource("http://127.0.0.1:5050/stream-log");

  eventSource.onmessage = function (event) {
    console.log("📥 로그 수신:", event.data);
    logBox.textContent += event.data + "\n";
    logBox.scrollTop = logBox.scrollHeight;
  };

  eventSource.onerror = function (err) {
    console.error("❌ SSE 연결 실패", err);
    logBox.textContent += "\n❌ SSE 연결 실패!\n";
  };

  loadBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      logBox.textContent = "🚀 수집 시작 요청 전송 중...\n";

      const res = await fetch("http://127.0.0.1:5050/run");
      const data = await res.json();

      const log = await fetch("http://127.0.0.1:5050/log").then((res) =>
        res.text()
      );
      logBox.textContent = log;
    } catch (err) {
      logBox.textContent = "❌ 서버 호출 실패!\n";
      console.error(err);
    }
  });
});
