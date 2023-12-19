const socket = new WebSocket('ws://127.0.0.1:8000/ws');

socket.onopen = function(e) {
  console.log("Tried to connect to server");
  socket.send(JSON.stringify({
    message: 'Hello from Js client'
  }));
};

socket.onmessage = function(event) {
  try {
    console.log(event);
    console.log("Connected to server");
  } catch (e) {
    console.log('Error:', e.message);
  }
};
