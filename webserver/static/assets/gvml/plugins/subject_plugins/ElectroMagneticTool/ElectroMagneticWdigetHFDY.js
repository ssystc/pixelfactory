/**
 * 项目：gvml
 * 文件：ElectroMagneticTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */
class ElectroMagneticWdigetHFDY extends GV.Widget {


    get alias() {
    	return '电磁信息HFDY';
    }

    init() {    	
		this.electricwidget = this.earth.getMapWidget('WidgetHFDY').open();
    }
//  dynTargetSelection(info)
//  {
//
//  }
//  dynTargetCountInfo(info)
//  {
//  	
//  }

	clearElec(){
		console.log("clearElec")
		this.electricwidget.postMessage("clearElec")
	}
	
	setElecVisible(name, height, v){		
		var para = name.toLowerCase() + ";" + height + ";" + (v?"true":"false")
		console.log("setElecVisible", para)
		this.electricwidget.postMessage("setElecVisible",para)
	}
	
	showHeightsElec(name, heights){
		var hstr = ""
		for(var i = 0; i < heights.length; i++)
			hstr = hstr + " " + heights[i]
		var para = name.toLowerCase() + ";" + hstr + ";" + "true"
		console.log("showHeightsElec", para)
		this.electricwidget.postMessage("showHeightsElec",para)
	}
	
	hideAllElec(){
		console.log('hideAllElec')
		this.electricwidget.postMessage("hideAllElec")
	}
	    
    remove() {
    	this.electricwidget.close();
    }
    
}

//# sourceURL=ElectroMagneticTool.js 
