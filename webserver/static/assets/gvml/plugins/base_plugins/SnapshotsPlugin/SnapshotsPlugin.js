
// 创建插件
class SnapshotsPlugin extends GV.Tool {

// 初始化插件
  init() {
  	// 引用基础库
	console.log('fdsafdsa');
  	this.script('../UtilTools/GAjax.js');
  	this.script('../UtilTools/echarts3.js');
  	this.script('../UtilTools/createChars.js');
  	const that = this;
  	// 激活插件
	this.distance = this.earth.getMapTool('RectAngleTool').select(); 

	// 接收框选操作
	this.distance.on('ts_rectangle', this.ontsrectangle.bind(this));
	
	document.getElementById('container').addEventListener('mouseup', (event)=>{
			this.shift = event.shiftKey;
		}, false);

	this.distance.on('ts_rectangle_close', this.oncloseiamge);
	
  }
   
   oncloseiamge(msg){
	   //右键关闭
		document.getElementById("imgDiv").style.display = "none";
   }
   
   // 连接服务并绘制统计信息
	ontsrectangle(msg){	
		
		
		var pointerstr = msg.replace(/;/g, ',');
		var dataUrl; 
		
		if(this.shift)
		{
			dataUrl = "http://192.168.6.2:19007/api/v1/create/IMAGE?format=jpeg&BoundingBox=" + pointerstr; 
		}
		else
		{
			dataUrl = "http://192.168.6.2:19006/api/v1/create/IMAGE?format=jpeg&BoundingBox=" + pointerstr; 
		}
		
		var pointarr = msg.split(";");		
		if(document.getElementById("imgDiv").style.display == "none"){
			document.getElementById("imgDiv").style.display = "block";
		}
		document.body.removeChild(document.getElementById("imgDiv"));
		var img = new Image();
		img.src = dataUrl;
		console.log(dataUrl)
		img.style.maxWidth = '512';
		img.style.maxHeight = "512px";
		var wrap = document.createElement("div");
		wrap.setAttribute("id","imgDiv");
		wrap.style.width = "512px";
		wrap.style.height = "512px";
		wrap.style.border = "solid #1111 10px";
		wrap.style.backgroundClip = "padding-box,border-box";
		wrap.style.backgroundOrigin = "padding-box,border-box";
		wrap.style.backgroundImage = "linear-gradient(white,white),linear-gradient(#395e73,#1d334b)";
		wrap.style.position = "absolute";
		wrap.style.top = "0px";
		wrap.style.right = "0px";
		document.body.appendChild(wrap);
		wrap.appendChild(img);


		// var b = document.createElement("bu");
		// b.setAttribute("id","imgDiv");
		// b.setAttribute("id","imgDiv");
		// b.textContent="打印";
		// b.style.width = "80px";
		// b.style.height = "40px";
		// b.style.border = "solid #1111 10px";
		// b.style.backgroundClip = "padding-box,border-box";
		// b.style.backgroundOrigin = "padding-box,border-box";
		// b.style.backgroundImage = "linear-gradient(white,white),linear-gradient(#395e73,#1d334b)";
		// b.style.position = "absolute";
		// b.style.top = "600px";
		// b.style.right = "0px";
		// document.body.appendChild(b);
		
	}

		remove() {
		this.distance.off('ts_rectangle', this.ontsrectangle.bind(this));
		this.earth.clearMapTool();
	}
}

