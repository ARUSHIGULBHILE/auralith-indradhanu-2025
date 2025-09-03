# Frontend (Dashboard)

Choose your stack (e.g., React + Vite). Suggested commands:

```bash
npm create vite@latest dashboard -- --template react
cd dashboard
npm install
npm run dev
```

Connect to the backend:
- REST: `GET http://localhost:8000/state/<device_id>`
- WebSocket: `ws://localhost:8000/ws`

Example WebSocket JS:
```js
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (evt) => {
  const msg = JSON.parse(evt.data);
  if (msg.type === 'update') {
    console.log('Twin update:', msg.data);
  }
};
// Keep alive:
setInterval(() => ws.send('ping'), 15000);
```
