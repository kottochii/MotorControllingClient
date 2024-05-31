var socket = io();
socket.on('connect', function() {
    console.log("Connected to the backend successfully.");
    socket.emit("backend_cnxn")
});
socket.on('message', (msg) => {
    console.log(msg);
    if(msg.signout)
        handleState('signout')
    else if(msg.signin)
        handleState('signin', msg.signin);

    if(msg.login_error)
    {
        $(".keypad_key").each((i, x) => {
            x.disabled = false;
        });
        $('#login_error')[0].innerText = msg.login_error;
    }
    
    if(msg.motors)
    {
        // motors is an array
        handleDevices(msg.motors);
    }

    if(msg.whoami)
    {
        $('#control_panel_user_id')[0].innerText = `${msg.whoami.response.name} [ID: ${msg.whoami.response.id}]`;
    }

    //handleState(msg);
});
socket.on('backend_error', (msg) => {
    console.error('Backend error', msg)
})
socket.on('disconnect', () => {
    console.error("Disconnected from the backend. Will refresh, state will not be lost")
    document.location = "";
});
socket.on('server_is_not_discoverable', (data) => {
    $("#emergency_floating_msg")[0].innerText = "Cannot establish connection with server " + data.server_address + ".\nCheck the connection and make sure to update the client's settings if required.";
})
socket.on('register_card_result', (data) => {
    $("#register_card_btn")[0].disabled = false;
    let text = $("#register_card_status")[0];
    if(data != true)
    {
        text.innerText = data.problem ?? "Unknown error occured. Card could not be registered.";
    }
    else text.innerText = "Successfully registered your card."
})