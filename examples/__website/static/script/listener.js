$(function(){

    //#################### 消息提醒模块
    (function(){

        $(window).on('message', function(event, data){

            if(data.from_user==current_user){

                //自己的消息不提醒
                return;

            }else{

                //显示未读消息的条数
                var $target = $(".chatContainer[data-main='"+data.from_email+"']");
                if((data.to_email==current_user) && ($target.is(":visible")==false)){

                    var $list_target = $(".chatListColumn[data-target='"+data.from_email+"']");
                    var $info = $list_target.find('.label-info');
                    var num =parseInt( $info.html())+1;
                    $info.show().html(num);

                }

                if((data.to_email=='groups') && ($("#all").is(':visible')==false)){

                   var $info = $("#chat-all").find('.label-info');
                   var num =parseInt( $info.html())+1;
                   $info.show().html(num);

                }

                 //调用webkitNotifications
                 if(window.webkitNotifications){
                     //浏览器功能检测
                     //console.log("Notifications are supported!");
                     if (window.webkitNotifications.checkPermission() == 0) {

                         var notification = window.webkitNotifications.createNotification(
                                data.avatar, data.nickname+ '发来了新消息', data.message);
                         notification.show();
                         notification.onclick=function(){

                             //页面显示聊天面板
                             var $target = $target = $(".chatListColumn[data-target='"+data.from_email+"']");
                             if(data.to_email=='groups'){
                                 $target = $(".chatListColumn[data-target='groups']");
                             }
                             $target.click();
                             //聚焦浏览器
                             $(window).focus();

                         };
                         window.setTimeout(function(){

                            notification.cancel();

                         }, 5000);

                     }else{
                         window.webkitNotifications.requestPermission();
                     }

                 }

                $(window).trigger('voice.message');

            }

        });

    })();

    // ####################### 系统通知模块
    (function(){
        $(window).on('system.error', function(event, data){

            var tpl_alert = $("#tpl_alert").html();
            var template = tpl_alert.replace("{0}","")
                .replace("{1}", data.message)
            $("body").prepend(template);

        })
        $(window).on('add', function(event, data){

            //console.log(data);
            if(data.email!=current_user){
                 $(window).trigger('voice.system',null);
            }


        });
        $(window).on('voice.system', function(event, data){

             //调用html5 audio播放提示音
             var hasVideo = !!(document.createElement('video').canPlayType);
             if(hasVideo==true){
                 //播放提示音
                 var snd = new Audio("/static/mp3/system.wav"); // buffers automatically when created
                 snd.play();

             }

        });
        $(window).on('voice.message', function(event, data){

             //调用html5 audio播放提示音
             var hasVideo = !!(document.createElement('video').canPlayType);
             if(hasVideo==true){
                 //播放提示音
                 var snd = new Audio("/static/mp3/tweet.wav"); // buffers automatically when created
                 snd.play();

             }

        });

    })();

    // websocket
    (function(){

         if ("WebSocket" in window) {

            //Template
            var tpl_chatItem = $("#tpl_chatItem").html();
            var curWwwPath=window.document.location.href;
            var pathName=window.document.location.pathname;
            var pos=curWwwPath.indexOf(pathName);
            var localhostPaht=curWwwPath.substring(7,pos);

            var ws = new WebSocket('ws://'+localhostPaht+'/ws')

            ws.onmessage = function(event){

                var obj = eval("("+event.data+")")

                if(obj.type=="normal"){

                    $(window).trigger("message", obj);

                    var tpl = tpl_chatItem.replace("{0}", obj.message)
                            .replace("{1}", obj.avatar)
                            .replace("{3}", obj.nickname)

                    var from_email = obj.from_email;
                    var to_email = obj.to_email;

                    if(from_email==current_user){
                        tpl = tpl.replace("{2}", "me")
                    }else{
                        tpl = tpl.replace("{2}", "you")
                    }
                    var $container = null;

                    if( to_email != 'groups' ){

                        $container = $(".chatContainer[data-main='"+from_email+"']");
                        if(from_email == current_user){
                            $container = $(".chatContainer[data-main='"+to_email+"']");
                        }

                    }else{
                        $container = $("#all")
                    }

                    var $scroll = $container.find(".chatScorll");
                    $scroll.append(tpl);
                    $scroll.scrollTop($scroll[0].scrollHeight);

                    emojify.run();

                }else if(obj.type=="add"){
                    /**
                     * bugs:
                     * 当其他用户刷新页面后 会出现多个聊天面板  data-main='email'相同[修改判断参数为聊天面板email]
                     *
                     * */
                    for(var i=0;i<obj.clients.length;i++){

                        //更新用户列表项
                        //有新成员加入
                        var client = obj.clients[i]
                        var length = $("#"+client.id).length
                        if(length==0){
                            var tpl_chatmember = $("#tpl_chatmember").html()
                                .replace("{0}", client.avatar)
                                .replace("{1}", client.nickname)
                                .replace("{2}", "")
                                .replace("{3}", client.id)
                                .replace("{4}", client.id)
                                .replace("{5}", client.email);

                            $(window).trigger(obj.type, client);
                            $("#chatMember").append(tpl_chatmember)
                        }

                        //更新聊天面板项
                        //var length = $("#chat-"+client.id).length
                        var length = $(".chatContainer[data-main='"+client.email+"']").length;
                        if(length==0){

                            var tpl_chatcontainer = $("#tpl_chatcontainer").html()
                                    .replace("{0}", "chat-"+client.id)
                                    .replace("{1}", "与"+client.nickname+"聊天中...")
                                    .replace("{2}", client.id)
                                    .replace("{3}", client.email);
                            $("#chat_containers").append(tpl_chatcontainer)

                        }

                    }

                }else if(obj.type=='out'){

                    $(window).trigger(obj.type, obj);
                    var select = "#"+obj.id;
                    $(select).fadeOut(1000).remove();

                }else{

                    $(window).trigger(obj.type, obj);

                }

            }

        } else {

            alert("WebSocket not supported");

        }

    })();

});