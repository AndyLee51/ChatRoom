his = new Array()

var ws = new WebSocket("ws://10.1.20.71:9000/wschat");
ws.onmessage = function(e) {
    message = JSON.parse(e.data)
    room_name=message[0]
    user_name=message[1]
    msg=message[2]
    console.log(message)
    // $("#contents").append("<p>" + e.data + "</p>");
    content = "<div style='display: flex;'><div class='imgdiv_rec'><img src='static/pic/group.png' class='send_img'>"+user_name+"</div><div class='msg_rec left' id='msg'>"+ msg+"</div></div><br/>"
    if ($("[nowsel='true']").attr("id")==room_name)
    {
        console.log(content)
        $("#msgshow").append(content)
    }
    else{
        if (his[room_name] == undefined){
            his[room_name] = content
        }
        else{
            his[room_name] += content
        }
        num = Number($("#"+room_name+" .msg_tip").html())
        $("#"+room_name+" .msg_tip").html(num+1)
        $("#"+room_name+" .msg_tip").css({"display":""})
    }
    
}
$(function() { 
    bkLib.onDomLoaded(function() {
        var myNicEditor = new nicEditor({maxHeight:100,iconsPath : 'static/pic/nicEditorIcons.gif'});
        myNicEditor.setPanel('Editor');
        myNicEditor.addInstance('input_area');

        $("#Editor").next().addClass("nui-scroll")
        $("#Editor").next().css({"border-width":"","border-top-style":"","border-right-style":"",
            "border-bottom-style":"","border-left-style":""})
        // $("body").css("background-color","burlywood")
    });

    $(this).keydown(function(e) {
        var keyCode = e.keyCode || e.which || e.charCode;
        var ctrlKey = e.ctrlKey || e.metaKey;
        if(ctrlKey && keyCode == 13) {
        }
        else if (keyCode == 13)
        {
            msgSend()
            e.preventDefault();
            return false;
        }
    })

    $(".user_info").mouseover(function(){
        $(this).css({"background-color":"darkcyan"})
    })
    $(".user_info").mouseout(function(){
        if($(this).attr("nowsel")!="true")
        {
            $(this).css({"background-color":""})
        }
    })
    $(".user_info").click(function(){
        // 保存现在的消息
        his[$("[nowsel='true']").attr("id")]=$("#msgshow").html()
        $("#now_info").html($("[nowsel='true']").attr("id"))
        ///更换选中
        $(this).attr("nowsel","true")
        $(this).siblings().css({"background-color":""})
        $(this).siblings().attr("nowsel","false")
        $("#now_info").html($("[nowsel='true']").attr("id"))
        $("#"+$("[nowsel='true']").attr("id")+" .msg_tip").html("")
        $("#"+$("[nowsel='true']").attr("id")+" .msg_tip").css({"display":"none"})
        content = his[$("[nowsel='true']").attr("id")]
        if (content==undefined){
            $("#msgshow").html("")
        }
        else{
            $("#msgshow").html(content)
        }
    })


    $(".nin_room").mouseover(function(){
        $(this).css({"background-color":"darkcyan"})
    })
    $(".nin_room").mouseout(function(){
        if($(this).attr("ninsel")!="true")
        {
            $(this).css({"background-color":""})
        }
    })
    $(".nin_room").click(function(){
        $(this).attr("ninsel","true")
        $(this).siblings().css({"background-color":"azure"})
        $(this).siblings().attr("ninsel","false")
    })

    $("#now_info").html($("[nowsel='true']").attr("id"))

    layui.config({base: '/static/js/'})
	layui.use(['mouseRightMenu','layer','jquery'],function(){
		var mouseRightMenu = layui.mouseRightMenu,layer = layui.layer,$=layui.jquery;
         //右键监听
         $('.nin_room').bind("contextmenu",function(e){
			var data = $(this).attr("id")
 			var menu_data=[
				{'data':data,'type':1,'title':'加入'},
			]
 			mouseRightMenu.open(menu_data,false,function(d){
                layer.confirm('确认加入'+d.data+'?', {icon: 3, title:'提示'}, function(index){
                    $.ajax({
                        type : "POST", //提交方式 
                        url : "/group",//路径 
                        cache:false,
                        data : { 
                            "_xsrf":$("input[name='_xsrf']").val(),
                            "action":"join",
                            "val":d.data,
                        },//数据，这里使用的是Json格式进行传输 
                        success : function(result) {//返回数据根据结果进行相应的处理 
                            location.reload(function(){
                                layer.alert('您已成功退出'+selected_room);
                            });
                        } 
                    })
                    layer.close(index);
                },function(index){
                    layer.close(index);
                });
            });
			return false;
		}); 

 		$('.user_info').bind("contextmenu",function(e){
			var data = $(this).attr("id")
 			var menu_data=[
				{'data':data,'type':1,'title':'退出'},
			]
 			mouseRightMenu.open(menu_data,false,function(d){
                layer.confirm('确认退出'+d.data+'?', {icon: 3, title:'提示'}, function(index){
                    $.ajax({
                        type : "POST", //提交方式 
                        url : "/group",//路径 
                        cache:false,
                        data : { 
                            "_xsrf":$("input[name='_xsrf']").val(),
                            "action":"quit",
                            "val":d.data,
                        },//数据，这里使用的是Json格式进行传输 
                        success : function(result) {//返回数据根据结果进行相应的处理 
                            location.reload(function(){
                                
                            });
                        } 
                    })
                    layer.close(index);
                },function(index){
                    layer.close(index);
                });
            });
			return false;
		});
			
	})

})
function msgSend()
{
    myEditor = nicEditors.findEditor("input_area")
    div = document.getElementById("msgshow")
    content = myEditor.getContent()
    if (content!="")
    {
        msg = nicEditors.findEditor("input_area").getContent()
        room_name=$("[nowsel='true']").attr("id")
        ws.send(JSON.stringify([room_name,msg]));

        // <div class='imgdiv'><img src='static/pic/user.png'></div>
        content = "<div style='display: flex;'><div class='msg_send right' id='msg'>"+ myEditor.getContent()+"</div><div class='imgdiv'><img src='static/pic/Me.png' class='send_img'></div></div><br/>"
        $("#msgshow").append(content)
        myEditor.setContent("")
        $(".nicEdit-main")[0].focus()
        div.scrollTop = div.scrollHeight
    }
}
function hide()
{
    width = $("#nonin").outerWidth()
    $("#nonin").hide("10",function(){
        $("#showBtn").css({"display":""})
        // $("#massage").width("100%")
        $(".nicEdit-main").parent().width("100%")
        $(".nicEdit-main :first").width("100%")
        
    });
}
function show()
{
    $("#showBtn").css({"display":"none"})
    $("#nonin").show("0",function(){
        
        $("#massage").width("100%")
        // $(".nicEdit-main").parent().width("70%")
        // $(".nicEdit-main :first").width("70%")
    });
}
function join_room()
{
    selected_room = $("[ninsel='true']").attr("id")
    layui.use('layer', function(){
        var layer = layui.layer;
        layer.confirm(' 确认加入'+selected_room+'?', {icon: 3, title:'提示'}, function(index){
            $.ajax({
                type : "POST", //提交方式 
                url : "/group",//路径 
                cache:false,
                data : { 
                    "_xsrf":$("input[name='_xsrf']").val(),
                    "action":"join",
                    "val":selected_room,
                },//数据，这里使用的是Json格式进行传输 
                success : function(result) {//返回数据根据结果进行相应的处理 
                    location.reload(function(){
                        layer.alert('您已加入'+selected_room);
                    });
                } 
            })
            layer.close(index);
        },function(index){
            layer.close(index);
        });
    });
}

function create()
{
    layer.prompt({
        formType: 0,
        title: '请输入聊天室名称',
        // area: ['800px', '350px'] //自定义文本域宽高
      }, function(value, index, elem){
        $.ajax({
            type : "POST", //提交方式 
            url : "/group",//路径 
            cache:false,
            data : { 
                "_xsrf":$("input[name='_xsrf']").val(),
                "action":"create",
                "val":value,
            },//数据，这里使用的是Json格式进行传输 
            success : function(result) {//返回数据根据结果进行相应的处理 
                if (result=="0"){
                    layer.alert("该聊天室已存在！");
                }else{
                    layer.alert("创建成功");
                    setTimeout(function(){
                        location.reload()
                    },1000)
                    
                }
                
            } 
        })  
        // layer.close(index);
      });
}
function out(){
    $.ajax({
        type : "POST", //提交方式 
        url : "/group",//路径 
        cache:false,
        data : { 
            "_xsrf":$("input[name='_xsrf']").val(),
            "action":"out",
            "val":$("[nowsel='true']").attr("id"),
        },//数据，这里使用的是Json格式进行传输 
        success : function(result) {//返回数据根据结果进行相应的处理 
            location.replace("/login")
        } 
    }) 
}