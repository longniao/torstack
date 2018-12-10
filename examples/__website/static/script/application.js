$(function(){

    //##############################页面初始化
    (function(){

        //emoji c表情配置
        emojify.setConfig({
            emojify_tag_type: 'img',
            emoticons_enabled: true,
            people_enabled: true,
            nature_enabled: true,
            objects_enabled: true,
            places_enabled: true,
            symbols_enabled: true
        });

        //初始化emoji表情
        emojify.run();

        $.ajax({

            url: "/background",
            type: 'get',
            success: function(result){
                 $("#fullscreen_post_bg").hide().css('background-image','url('+result+')').fadeIn(500);
                 $("#fullscreen_bg_load").hide();
            }

        });

        var tpl_chatcontainer = $("#tpl_chatcontainer").html()
            .replace("{0}", "all")
            .replace("{1}", "群聊中")
            .replace("{3}", 'groups');
        $("#chat_containers").empty().append(tpl_chatcontainer)
        $("#all").fadeIn(500);

    })();

    //###################页面事件监听
    (function(){

        //页面刷新或者管理事件
        $(window).bind('beforeunload', function(e){
            console.log(e);
            return false;
        });

        //用户列表点击处理
        $("#chatMember").delegate(".chatListColumn","click", function(){

            $(".chatListColumn").removeClass('active');
            $(this).addClass('active');
            var target = $(this).attr("data-target");
            if(target!=undefined){

                var $target = $(".chatContainer[data-main='"+target+"']");
                var _class = $target.attr("class")
                $("."+_class).hide();//隐藏其他面板
                $target.fadeIn(500);

                //清理消息提示数
                var $info =$(this).find('.label-info');
                var num =0;
                $info.hide().html(num);
                
            }

        });

        //点击显示emoji表情列表
        $("body").on('click', '.btn_face', function(e){

            var xx = (e.pageX || e.clientX + document.body.scrollLeft)-290;
            var yy = (e.pageY || e.clientY + document.boyd.scrollTop)-155;
            $("#emoji_face").css("top",yy).css("left",xx).toggle();

        });

        //点击表情，添加到输入框
        $("#emoji_face").delegate("li", "click", function(e){

            var emoji = $($(this).find('img')[0]).attr('title');
            $(".chatContainer").each(function(){
                if($(this).css('display')=='block'){
                    var $textarea =  $(this).find('textarea');
                    var tmp =$textarea.val()+emoji;
                    $textarea.val(tmp);
                }
            });
            emojify.run();

        });

        //点击发送按钮 发送信息
        $("body").on('click', '.chatSend', function(){

            var $from = $(this).parent('form')
            $from.submit()
            return false

        });

        //ctrl+Enter发送信息
        $("body").delegate('.chatInput', 'keyup', function(e){

            if(e.ctrlKey && e.which == 13 || e.which == 10) { // Ctrl+Enrer(回车)
                $(this).prev().click();
            }

        });

        //表单提交事件处理
        $("body").delegate('.sendForm', 'submit', function(){

            var $textarea = $(this).find('textarea')
            var $input = $(this).find('input')
            var message = $textarea.val()
            var to = $input.val();
            var to_email = $(this).parents('.chatContainer').attr('data-main');
            to = to=='{2}'?'':to;
            to_email = to_email=='{3}'?'':to_email;
            $.post("./chat", { data: message, to: to ,to_mail: to_email}, function(data){
                $("#data").val('');
            });
            $textarea.val("");
            return false;

        });

    })();

});