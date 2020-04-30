function longpoll_listener(chat_id) {
    $.ajax('/chat/' + chat_id + '/updates', {
        accept: "application/json",
        method: "GET",
        // async: false,
        success: function (data) {
            if (!data.ok) {
                // show_error('Какая-то ошибка, попробуйте позже');
                return;
            }
            for (let i = 0; i < data.values.length; i++) {
                let event = data.values[i];
                if (event.type === 'new_message') {
                    if (!event.is_system) {
                        let msg = document.createElement("div");
                        msg.className = "message";
                        let userinfo = document.createElement("div");
                        userinfo.className = "message-user-info";
                        let user = document.createElement('a');
                        user.className = "message-user";
                        user.href = '/user/' + event.username;
                        user.innerText = event.username;
                        let msg_text = document.createElement('div');
                        msg_text.className = "message-text";
                        msg_text.innerText = event.text;
                        userinfo.append(user);
                        msg.append(userinfo);
                        msg.append(msg_text);
                        $("#messages").append(msg);
                    } else {
                        let msgbox = document.createElement("div");
                        msgbox.className = "message-system-box";
                        let msg = document.createElement("div");
                        msg.className = "message-system";
                        let username = document.createElement('a');
                        username.className = "message-user-system";
                        username.href = '/user/' + event.username;
                        username.innerText = event.username;
                        let msg_text = document.createElement('span');
                        msg_text.className = "message-text-system";
                        msg_text.innerText = ' ' + event.text;
                        msg.append(username);
                        msg.append(msg_text);
                        msgbox.append(msg);
                        $("#messages").append(msgbox);
                    }
                }
            }
        },
        error: function (data) {
            // show_error('Какая-то ошибка, попробуйте позже');
        },
        complete: function (data) {
            longpoll_listener(chat_id);
        }
    });
}