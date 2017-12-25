/**
 * 项目：gvml
 * 文件：ElectroMagneticTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */
class ElectroMagneticTool extends GV.Widget {


    get alias() {
    	return '电磁信息';
    }

    init() {
    	 this.css('./ElectroMagneticTool.css');
        this.html('./ElectroMagneticTool.html');
		this.electricwidget = this.earth.getMapWidget('Electric').open();
//     
		const that = this;
		document.getElementById("leida").onchange = function(){
		    //alert(this.checked)
		    var para = "typecontrol;leida;"+this.checked;
			that.electricwidget.postMessage("GeoVIS::GVElecPlugin::ElecPluginMessage",para)
		}
		document.getElementById("dataLink").onchange = function(){
		    //alert(this.checked)
		    var para = "typecontrol;dataLink;"+this.checked;
			that.electricwidget.postMessage("GeoVIS::GVElecPlugin::ElecPluginMessage",para)
		}
		document.getElementById("pinpu").onchange = function(){
		    //alert(this.checked)
		    var para = "typecontrol;pinpu;"+this.checked;
			that.electricwidget.postMessage("GeoVIS::GVElecPlugin::ElecPluginMessage",para)
		}
    }
//  dynTargetSelection(info)
//  {
//
//  }
//  dynTargetCountInfo(info)
//  {
//  	
//  }
    
    remove() {
    	this.electricwidget.close();
    }
    
}

//# sourceURL=ElectroMagneticTool.js 
