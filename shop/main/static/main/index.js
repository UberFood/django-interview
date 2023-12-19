var SERVER_ADDRESS = location.origin.replace(/^http/, 'ws') + "/ws";
console.log(SERVER_ADDRESS)
const socket = new WebSocket(SERVER_ADDRESS);

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
