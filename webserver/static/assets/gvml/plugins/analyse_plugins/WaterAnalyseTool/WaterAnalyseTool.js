/**
 * 项目：gvml
 * 文件：DistanceTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-05 19:37:20.
 * 用途：类
 */
class WaterAnalyseTool extends GV.Tool {

// get alias() {
//  return '淹没分析工具';
// }
//
    init() {
    	console.log('water tool');
    	this.html('./wateranalyse.html');
    	this.css('./wateranalyse.css');
		this.watertool = this.earth.getMapTool('WaterAnalyseTool').select(); 
		this.watertool.on('analyse_watertool', this.areaParas);
		const that = this;
		//按钮功能(分析)
		document.querySelector('.yanmo_analyze').onclick = function(){
			this.style.background = "linear-gradient(#026075 10%,#01254f)";
			this.style.borderWidth = "0px";
			document.querySelector('.yanmo_remove').style.background = "none";
			document.querySelector('.yanmo_remove').style.borderWidth = "1px";
			alert('1----'+window.$('.yanmo_inData p:nth-child(2) input').val());
			alert('2----'+window.$('.yanmo_inData p:nth-child(3) input').val());
			alert('3----'+window.$('.yanmo_inData p:nth-child(5) input').val());
			alert('4----'+window.$('.yanmo_inData p:nth-child(6) input').val());
			var para=window.$('.yanmo_inData p:nth-child(2) input').val()+";"+window.$('.yanmo_inData p:nth-child(3) input').val()+";"
					+window.$('.yanmo_inData p:nth-child(5) input').val()+";"+window.$('.yanmo_inData p:nth-child(6) input').val()
			that.watertool.postMessage('create_wateranalse',para);
		}
		//清除
		document.querySelector('.yanmo_remove').onclick = function(){
			this.style.background = "linear-gradient(#026075 10%,#01254f)";
			this.style.borderWidth = "0px";
			document.querySelector('.yanmo_analyze').style.background = "none";
			document.querySelector('.yanmo_analyze').style.borderWidth = "1px";
			that.watertool.postMessage('clear_wateranalse',para);
		}
    }
    
    remove() {
    	this.earth.clearMapTool();
    }
    areaParas(v)
    {
    	alert(v);	
		window.$('.yanmo_inData p:nth-child(2) input').val(v.split(';')[0]);	
		window.$('.yanmo_inData p:nth-child(3) input').val(v.split(';')[1]);	
		window.$('.yanmo_inData p:nth-child(5) input').val(v.split(';')[2]);	
		window.$('.yanmo_inData p:nth-child(6) input').val(v.split(';')[3]);	
    }
}
