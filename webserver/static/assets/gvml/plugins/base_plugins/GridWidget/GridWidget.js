/**
 * 项目：gvml
 * 文件：SceneModeWidget.js
 * 作者：巩志远
 * 部门：产品研发中心
 * 邮箱：gongzy@geovis.com
 * 日期：2017-03-03 23:23:38.
 * 用途：类
 */

class GridWidget extends GV.Widget {

  init() {
  	this.registerName = 'GeoVIS::BasePlugin::GridWidget';
	this.grid = this.earth.getMapWidget('Gridwidget').open();
	
  }

}

