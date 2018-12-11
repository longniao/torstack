
jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var getWebsocketUrl = function () {
    var ishttps = 'https:' == document.location.protocol ? true: false;
    var url = window.location.host;
    if(ishttps){
        url = 'wss://' + url + "/ws";
    }else{
        url = 'ws://' + url + "/ws";
    }
    return url;
}

var renderItem = function (data) {
    if (data.type == "system") {
        tpl = ""
    } else if (data.type == "normal") {
        if (data.from_user == current_user) {
            style = "author";
        } else {
            style = "";
        }
        tpl = "<p class='message normal " + style + "'>" + data.message + "</p>"
    }
    return tpl;
}

function sendMessage(form) {
    var message = form.formToDict();
    console.log(message)
    listener.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

var handle = false;
var try_time = 0;
var ws_url = getWebsocketUrl();
var chat_box = $("#chat-box")

var listener = {

    socket: null,

    start: function() {
        if(listener.socket == null) {
            listener.socket = new WebSocket(ws_url);
        }
        listener.socket.onopen = function(event) {
            listener.open(event);
        }
        listener.socket.onmessage = function(event) {
            listener.message(event);
        }
        listener.socket.onclose = function(event) {
            listener.close(event);
        }
    },

    open: function (event) {
        console.log('Hello WebSocket!');
        // reset try time
        try_time = 0;
    },

    close: function (event) {
        console.log('Bye WebSocket!');
        // retry

        if (try_time < 10 && !handle) {
            setTimeout(function () {
                listener.start();
                try_time++;
            }, 3000);
        } else {
            console.log('WebSocket Error!');
        }
    },

    message: function (event) {
        var data = JSON.parse(event.data);
        listener.updateChatBox(data);
    },

    updateChatBox: function(data) {
        // console.log(data)
        content = renderItem(data);
        chat_box.append(content);
    }

};

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").on("submit", function() {
        sendMessage($(this));
        return false;
    });

    $("#messageform").on("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();

    listener.start();
});

