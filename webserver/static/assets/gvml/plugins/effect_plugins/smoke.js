/**
 * 项目：gvml
 * 文件：CompassZoom.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-08 13:22:28.
 * 用途：类
 */

class smoke extends GV.Widget {

  init() {

	  this.smoke = this.earth.getMapWidget('Smoke').open();
	}
    remove() {
  	this.smoke.close();
  }
}
