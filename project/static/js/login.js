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
function check(self){
    name = $(self).attr("name")
    id = $(self).attr("id")
    val = $(self).val()

    if (name=="valid")
    {
        if (val!="")
        {
            $.ajax({
                type : "POST", //提交方式 
                url : "/login",//路径 
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
                        $(self).val("")
                        change_img()
                    }
                } 
            })
        }
    }
}