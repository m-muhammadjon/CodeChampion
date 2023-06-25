let ws_url = "";
if (window.location.pathname.match(/\/problems\/(\d+)\/attempts/)) {
    ws_url = `ws://${window.location.host}/ws/user-socket/${user_id}`;

} else if (window.location.pathname === "/attempts") {
    ws_url = `ws://${window.location.host}/ws/attempt-socket`;
}
const socket = new WebSocket(ws_url);

socket.onopen = function (e) {
    console.log("Socket connected.");
}

socket.onmessage = function (e) {
    console.log("Socket message received.");
    const data = JSON.parse(e.data);
    let attempt = `tr#attempt-${data["attempt_id"]}`;
    if (data["created"] === true) {
        let element = $(`<tr id="attempt-${data['attempt_id']}">
            <td class="attempt-id">
                ${request_user_id === data['user_id'] ? `<a href="/attempts/${data['attempt_id']}" class="blue">${data["attempt_id"]}</a>` : data["attempt_id"]}
            </td>
            <td class="attempt-user">
                <a href="" class="blue-hover">${data['username']}</a>
            </td>
            <td class="attempt-problem">
                <a href="" class="blue-hover">${data['problem_title']}</a></td>
            <td class="attempt-language">${data['language']}</td>
            <td class="attempt-verdict text-dark">
                ${data['status']}
            </td>
            <td class="attempt-time">0 ms</td>
            <td class="attempt-memory">0 KB</td>
            <td class="attempt-created">${data['created_at']}</td>
        </tr>`);
        element.prependTo("tbody");

        // Remove the last item of tbody
        $("tbody tr").last().remove();

    }

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

