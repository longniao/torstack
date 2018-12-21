
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

var system_type = ["system:in", "system:out", "system:error"];
var renderItem = function (data) {
    if ($.inArray(data.type, system_type) >= 0) {
        tpl = "<p class='message normal text-center'>" + data.content + "</p>"
    } else {
        if (data.from_id == current_id) {
            tpl = "<p class='message normal text-right'><span class='label label-message'>" + data.content + "</span> <span class='label label-name'>: " + data.from_name + "</span></p>"
        } else {
            tpl = "<p class='message normal'><span class='label label-name'>" + data.from_name + " :</span> <span class='label label-message'>" + data.content + "</span></p>"
        }
    }
    return tpl;
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
        console.log($(".chat-container").offset().top);
        console.log(chat_box.get(0).scrollHeight);
        $(".chat-container").animate({
            scrollTop: chat_box.get(0).scrollHeight - $(".chat-container").offset().top
        }, 500);
    }
};

function sendMessage() {
    // console.log($('#message').val());
    $('#messageform').ajaxSubmit();
    $('#message').val("");
}

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").on("submit", function() {
        sendMessage();
        return false;
    });

    $("#messageform").on("keypress", function(e) {
        if (e.keyCode == 13) {
            sendMessage();
            return false;
        }
    });
    $("#message").select();

    listener.start();
});

