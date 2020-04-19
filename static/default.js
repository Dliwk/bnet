let current_chat_id = location.href.split('/')[location.href.split('/').length - 1];

function open_chat(chat_id) {
    location.href = '/chat/' + chat_id;
    current_chat_id = chat_id;
}

function show_error(text) {
    let error = document.createElement('div');
    error.className = "alert alert-dismissible alert-danger";
    let btn = document.createElement("button");
    btn.className = "close";
    btn.innerText = "×";
    let attr = document.createAttribute("data-dismiss");
    attr.value = "alert";
    btn.attributes.setNamedItem(attr);
    error.innerText = text;
    $("div#errors").append(error);
    error.append(btn);
}

function send_message(chat_id) {
    if (chat_id === undefined) {
        chat_id = current_chat_id;
    }
    let textbox = $("#msg-textbox");
    let text = textbox.text();
    $.ajax("/chat/" + chat_id, {
        accept: "application/json",
        type: "POST",
        data: {
            text: text,
        },
        success: function (data) {
            let msg = document.createElement("div");
            msg.className = "message";
            let userinfo = document.createElement("div");
            userinfo.className = "message-user-info";
            let user = document.createElement('a');
            user.className = "message-user";
            user.href = '/yourself';
            user.innerText = 'Вы';
            let msg_text = document.createElement('div');
            msg_text.className = "message-text";
            msg_text.innerText = text;
            userinfo.append(user);
            msg.append(userinfo);
            msg.append(msg_text);
            $("#messages").append(msg);
            textbox.text('');
        },
        error: function (data) {
            show_error("Какая-то ошибка, попробуйте позже");
        },
    });
}

$(document).ready(function () {
    $("#msg-textbox").keypress(function (e) {
        if (e.ctrlKey && e.key === "Enter") {
            send_message();
        }
    })
});