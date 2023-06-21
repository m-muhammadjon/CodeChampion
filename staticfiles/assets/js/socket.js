const ws_url = `ws://${window.location.host}/ws/user-socket/${user_id}`;
const socket = new WebSocket(ws_url);

socket.onopen = function (e) {
    console.log("Socket connected.");
}

socket.onmessage = function (e) {
    console.log("Socket message received.");
    const data = JSON.parse(e.data);
    let attempt = `tr#attempt-${data["attempt_id"]}`;
    if (data["is_finished"] === true) {
        document.querySelector(`${attempt} td.attempt-verdict`).innerHTML = data["status"];
        document.querySelector(`${attempt} td.attempt-time`).innerHTML = `${data["time"]} ms`;
        $(`${attempt} td.attempt-verdict`).attr("class", data["status"] === "Accepted" ? "accepted" : "wrong");

    } else {
        document.querySelector(`${attempt} td.attempt-verdict`).innerHTML = data["status"];
    }
}

socket.onerror = function (e) {
    console.error("Socket error.");
    const data = JSON.parse(e.data);
    console.log(data);
}

socket.onclose = function (e) {
    console.error("Socket closed.");
    const data = JSON.parse(e.data);
    console.log(data);
}

