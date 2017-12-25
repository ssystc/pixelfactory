//封装ajax请求
function GAjax(options){
	options.type = (options.type || "POST").toUpperCase();
	options.dataType = options.dataType || "json";
	var params = formatParams(options.data);

	var oXhr = new XMLHttpRequest();
	oXhr.onreadystatechange = function (){
		if(oXhr.readyState == 4){ 	 
			if(oXhr.status == 200){   
				options.success(oXhr.responseText)		
			}else{
				options.fail(oXhr.status)
			}
		}else{
			// console.log(oXhr.readyState)
		}
	};
	if(options.type == 'GET'){
		oXhr.open('GET',options.url + "?" + params,options.async);
		oXhr.send(null);
	}else if(options.type == 'POST'){
		oXhr.open("POST", options.url,options.async);
		//设置表单提交时的内容类型
        oXhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        oXhr.send(params);
	}			
};
//格式化参数
function formatParams(data) {
    var arr = [];
    for (var name in data) {
        arr.push(encodeURIComponent(name) + "=" + encodeURIComponent(data[name]));
    }
    // arr.push(("v=" + Math.random()).replace(".",""));
    return arr.join("&");
};
//示例
// GAjax({
// 	type : 'POST',
// 	url : 'json/index.json',
// 	data : {params1:'one',params2:"two"},
// 	dataType: "json",
// 	async : true,
// 	success : function(resonse){
// 		console.log(JSON.parse(resonse))
// 	},
// 	fail : function(status){
// 		alert("服务器报错状态码为"+status)
// 	}
// });



