/**
 * 项目：gvml
 * 文件：Bluetooth.js
 * 作者：lihaidong
 * 部门：产品研发中心
 * 邮箱：lihd@geovis.com
 * 日期：2017-03-03 23:23:38.
 * 用途：类
 */

class Bluetooth extends GV.Widget {
	StrToJson(str0){
		//前半字符串
		var str1 = str0.substring(0,str0.lastIndexOf("Data\":")+6)
		//后半截字符串
		var str2 = str0.substring(str0.lastIndexOf("Data\":")+6); 
		if (str2.indexOf("{") == 1) {
			//双引号变单引号
			str2 = str2.replace(/\"/,"");
			str2 = str1 + str2;
			//最后一个单引号变回双引号
			str1 = str2.substring(0,str2.lastIndexOf("\""));
			var str2 = str2.substring(str2.lastIndexOf("\""));
			str2 = str1 + str2.replace(/\"/,"");
		} 
		else{
			str2 = str0;
		}
		return JSON.parse(str2);
	}
	StrToJson1(str0){
		var str1 = str0.substring(str0.indexOf("(")+1,str0.lastIndexOf(")"));
		str1 = str1.split(" ")
		return str1
	}
	fun(angle) {
      return angle/180*3.1415926;
    }
	
  	init() {
  		//打开蓝牙
	    window.OpenBlueTooth();
	    const this_ = this;
	    //得到相机对象
	    const camera = this.earth.camera; 
	    //const vp = camera.getViewPoint();//得到相机当前姿态
	    window.getText = function (temp)
		{
			//{"Command":"Voice","Data":"上海"}
//				camera.setViewPoint({"long":0,"lat":0,"range":6378137},2);.
			console.log("temp")
			console.log(temp)
//			alert("voice")
			var Type = this_.StrToJson(temp).Command;
			if (Type == "Voice") {
				$.ajax({
					type:"get",
//					url:"http://192.168.6.3:9004/api/v1/zsk/query="+this_.StrToJson(temp).Data,
					url:"http://192.168.110.222:9004/api/v1/zsk/query="+this_.StrToJson(temp).Data,
					async:false,
					success:function(msg){
//						alert("success")
						console.log("msg")
						console.log(msg)
						if( msg.type == "location_of_place"){
							camera.setViewPoint({"long":this_.StrToJson1(JSON.parse(msg.result)[0].WZ)[0],"lat":this_.StrToJson1(JSON.parse(msg.result)[0].WZ)[1],"range":300000},2);
						}else if(msg.type == "identify_graph_object"){
							//图上有什么
							//alert(msg.result)
							
							uploadShipPic();
						}
						else if( msg.type == "current_location")
						{
							//它在哪
						var widget = this_.earth.getPluginByName('dyntarget');
						if(widget === undefined){alert('dyntarget widget === undefined');}
						widget.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "createhangmu;" + "123");
						//camera.setViewPoint({"long":139,"lat":35,"range":300000},2);
						
						//////////////////////////////////////
						const vp = camera.getViewPoint();
                      	vp.long = 127.500;
                      	vp.lat = 31.4536;
                      	vp.heading = -0;
                      	vp.pitch = -20;
                      	vp.range = 180000;
                      	camera.setViewPoint(vp,2);
                      	///////////////////////////////////

						
						//widget.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "createHMTrack;" + msg.info);
						
						}
						else if(msg.type == "d_distance_to_me")
						{
							//距离我多远
							var widget2 = this_.earth.getPluginByName('dyntarget');
							widget2.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "createHAX;" + msg.result);
							
							
													//////////////////////////////////////
						const vp = camera.getViewPoint();
                      	vp.long = 126.347;
                      	vp.lat = 34.000;
                      	vp.heading = -0;
                      	vp.pitch = -20;
                      	vp.range = 1058330;
                      	camera.setViewPoint(vp,2);
                      	///////////////////////////////////
						}
						else if(msg.type == "d_subship")
						{
							//所属舰支有哪些msg.result
							//init3DForce(msg.result);
//							alert("获取网页连接给three.js拿数据" + getDataUrl)

							getSubShip();
							
						}
						else if(msg.type == "d_task")
						{
							//执行什么任务
//							alert("发送2张图热力图/*给G5")
							var widget2 = this_.earth.getPluginByName('dyntarget');
							widget2.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "createImage;" + msg.result);
							
													
							const vp = camera.getViewPoint();
	                      	vp.long = 137.539;
	                      	vp.lat = 25.423;
	                      	vp.heading = 0;
	                      	vp.pitch = -90;
	                      	vp.range = 7555910;
	                      	camera.setViewPoint(vp,2);
						}
						else if(msg.type == "d_rel_graph")
						{
							//船员情况
							//init3DForce(msg.result);
//							alert("获取地址给three")

							getCaptainRelation();
							
							
						}
						else if(msg.type == "d_threaten")
						{
							//有什么威胁
//							alert("返回四个威胁范围G5")
							var widget2 = this_.earth.getPluginByName('dyntarget');
							widget2.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "showDangerous;" +"");
						
							const vp = camera.getViewPoint();
	                      	vp.long = 123.678;
	                      	vp.lat = 35.265;
	                      	vp.heading = 0;
	                      	vp.pitch = -30;
	                      	vp.range = 6378137;
	                      	camera.setViewPoint(vp,2);
						}
//						else{
//							console.log(JSON.parse(msg.result).h)
////							alert(JSON.parse(msg.result).h + "米")
//						}
						
					}
				});
				
			}else if (Type == "SetCamera") {
				var tex = this_.StrToJson(temp);
				//俯仰角前后俯仰
//				if (tex.Data.PitchValue != undefined) {
//					camera.rotate(0,-this_.fun(tex.Data.PitchValue))
//				}
//				//经度
//				if(tex.Data.LonValue != undefined){
////					vp.long = tex.Data.LonValue + vp.long;
//					camera.pan(this_.fun(tex.Data.LonValue)*(-0.5),0);
//				}
//				//纬度
//				if(tex.Data.LatValue != undefined){
////					vp.lat = tex.Data.LatValue + vp.lat;
//					camera.pan(0,this_.fun(tex.Data.LatValue)*(-0.5));
//				}
//				//改变高度---放松
//				if (tex.Data.ScaleValue != undefined) {
//				    const vp = camera.getViewPoint();//得到相机当前姿态
//				    console.log(vp.range)
//				    console.log(tex.Data.ScaleValue)
//					if ( vp.range >10000 || vp.range < 2000000 ) {
//						camera.setRange( vp.range - tex.Data.ScaleValue*100000)
//					}
//				}
////				camera.setViewPoint(vp,0); //设置相机姿态,与飞到指定位置的时间
//			}else if(Type == "ResetCamera"){
//			    camera.setViewPoint(VpHome,1); //设置相机姿态,与飞到指定位置的时间
//			}else if(Type == "ResetHeading"){
//			    camera.setViewPoint(VpHome,1); //设置相机姿态,与飞到指定位置的时间

				camera.postMessage('set_camera', tex);
			}
			else if(Type == "ResetCamera")
			{
				camera.postMessage('set_camera', temp);
			}
			else if(Type == "ResetHeading")
			{
				camera.postMessage('set_camera', temp);
			}
			
		}
	    
  	}

}

