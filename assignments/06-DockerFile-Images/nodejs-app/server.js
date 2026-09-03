const http = require('http');

const PORT = 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Node.js App - Assignment 06</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #0f172a; color: #f8fafc; }
    .card { background: #1e293b; padding: 2.5rem 3.5rem; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; }
    h1 { color: #38bdf8; margin-bottom: 0.5rem; }
    p { color: #94a3b8; font-size: 1.1rem; }
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; background: #0369a1; color: #e0f2fe; font-size: 0.875rem; font-weight: 600; margin-top: 1rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Node.js Application Deployed</h1>
    <p>Running inside Docker container on port 3000</p>
    <span class="badge">Task 3: Docker Application Deployment</span>
  </div>
</body>
</html>`);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Node.js web server running on port ${PORT}`);
});
