function set_md5()
{
    if ($("#id_password").val()!="")
    {
        $("#id_password_md5").val($.md5($("#id_password").val()))
    }
}
function change_img(){
    $.ajax({
        type : "POST", //提交方式 
        url : "/imgvalid",//路径 
        cache:false,
        data : { 
            "_xsrf":$("input[name='_xsrf']").val(),
            "refresh" : "1",
            "time":new Date().getMilliseconds()
        },//数据，这里使用的是Json格式进行传输 
        success : function(result) {//返回数据根据结果进行相应的处理 
            $("#valid_img").attr("src",jQuery.parseJSON(result).path);
        } 
    })
}
function check(index){
    name = $(index).attr("name")
    id = $(index).attr("id")
    val = $(index).val()
    if (name=="account"){
        var namePattern = /^[a-zA-Z0-9_-]+$/;
        if (val!="")
        {
            if (!namePattern.test(val)){
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('用户名仅可包含字母，数字，下划线，减号', '#'+id);
                });
                $(index).focus()
            }
            else{
                $.ajax({
                    type : "POST", //提交方式 
                    url : "/register",//路径 
                    cache:false,
                    data : { 
                        "_xsrf":$("input[name='_xsrf']").val(),
                        "Check":true,
                        "field":"name",
                        "val":val,
                    },//数据，这里使用的是Json格式进行传输 
                    success : function(result) {//返回数据根据结果进行相应的处理 
                        if(jQuery.parseJSON(result).exist){
                            layui.use('layer', function(){
                                var layer = layui.layer;
                                layer.tips('用户名已存在', '#'+id);
                            });
                            $(index).val("")
                        }
                    } 
                })
            }
        }
    }
    else if (name=="email")
    {
        var emailPattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        if (val!="")
        {
            if (!emailPattern.test(val)){
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('邮箱地址不合理，请重新输入', '#'+id);
                });
                $(index).focus()
            }
            else{
                $.ajax({
                    type : "POST", //提交方式 
                    url : "/register",//路径 
                    cache:false,
                    data : { 
                        "_xsrf":$("input[name='_xsrf']").val(),
                        "Check":true,
                        "field":"email",
                        "val":val,
                    },//数据，这里使用的是Json格式进行传输 
                    success : function(result) {//返回数据根据结果进行相应的处理 
                        if(jQuery.parseJSON(result).exist){
                            layui.use('layer', function(){
                                var layer = layui.layer;
                                layer.tips('该邮箱已注册', '#'+id);
                            });
                            $(index).val("")
                        }
                    } 
                })
            }
            
        }
        
    }
    else if (name=="valid")
    {
        if (val!="")
        {
            $.ajax({
                type : "POST", //提交方式 
                url : "/register",//路径 
                cache:false,
                data : { 
                    "_xsrf":$("input[name='_xsrf']").val(),
                    "ValidCheck":true,
                    "val":val,
                },//数据，这里使用的是Json格式进行传输 
                success : function(result) {//返回数据根据结果进行相应的处理 
                    if(jQuery.parseJSON(result).wrong){
                        layui.use('layer', function(){
                            var layer = layui.layer;
                            layer.tips('验证码输入错误', '#'+id);
                        });
                        $(index).val("")
                        change_img()
                    }
                } 
            })
        }
        
    }
}