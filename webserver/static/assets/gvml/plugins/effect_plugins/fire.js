/**
 * 项目：gvml
 * 文件：CompassZoom.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-08 13:22:28.
 * 用途：类
 */

class fire extends GV.Widget {

  init() {
		console.log('fire');
	  this.fire = this.earth.getMapWidget('Fire').open();
	}
  
    remove() {
    	
  	this.fire.close();
  }
}
