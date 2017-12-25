/**
 * 项目：gvml
 * 文件：DistanceTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-05 19:37:20.
 * 用途：类
 */
class InterVisibleTool extends GV.Tool {

// get alias() {
//  return '通视分析工具';
// }
//
    init() {
    	console.log('inter visible tool');
    	this.html('./InterVisible.html');
    	this.css('./InterVisible.css');
		this.intervisibletool = this.earth.getMapTool('InterVisibleTool').select(); 
		this.intervisibletool.on("analyse_intervisible",this.getParas);
		const that = this;
		//按钮功能（分析）
		document.querySelector('.tslv_analyze').onclick = function(){
			this.style.background = "linear-gradient(#026075 10%,#01254f)";
			this.style.borderWidth = "0px";
			document.querySelector('.tslv_remove').style.background = "none";
			document.querySelector('.tslv_remove').style.borderWidth = "1px";
			//alert('1----'+window.$('.tslv_inData p:nth-child(1) input').val());
			//alert('2----'+window.$('.tslv_inData p:nth-child(2) input').val());
			//alert('3----'+window.$('.tslv_inData p:nth-child(3) input').val());		
			//alert('4----'+window.$('.tslv_inData p:nth-child(4) input').val());	
			var para =window.$('.tslv_inData p:nth-child(1) input').val()+";"+window.$('.tslv_inData p:nth-child(2) input').val()+";"+window.$('.tslv_inData p:nth-child(3) input').val()
			//alert(para);
			that.intervisibletool.postMessage('create_intervisible',para);
		}
		//清除
		document.querySelector('.tslv_remove').onclick = function(){
			this.style.background = "linear-gradient(#026075 10%,#01254f)";
			this.style.borderWidth = "0px";
			document.querySelector('.tslv_analyze').style.background = "none";
			document.querySelector('.tslv_analyze').style.borderWidth = "1px";
		}
    }
    
    remove() {
    	this.earth.clearMapTool();
    }
    getParas(v)
    {
    	//alert(v);	
		window.$('.tslv_inData p:nth-child(1) input').val(v.split(';')[0]);	
		window.$('.tslv_inData p:nth-child(2) input').val(v.split(';')[1]);		
    }
}
