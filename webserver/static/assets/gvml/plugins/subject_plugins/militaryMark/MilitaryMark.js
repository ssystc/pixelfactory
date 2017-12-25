/**
 * 项目：gvml
 * 文件：DyntargetTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */

class MilitaryMark extends GV.Tool {

    get alias() {
        return '静目标信息';
    }

    init() {
        this.css('./militaryMarkInfo.css');
        this.html('./militaryMarkInfo.html');
        var that = this;

   	    this.militaryMark = this.earth.getMapTool('MilitaryMark').select();
   
      for(var i=0;i<document.querySelectorAll('.yxms-content ul li img').length;i++){
          	document.querySelectorAll('.yxms-content ul li img')[i].onclick = function(){
          
          		
          		that.militaryMark.postMessage('changedMark', this.attributes[1].value,this.attributes[2].value);
          	}
          	
    	}	
    }

  	remove() {
  		this.earth.clearMapTool();
  	}

}

//# sourceURL=MilitaryMark.js 
