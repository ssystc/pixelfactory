/**
 * 项目：gvml
 * 文件：SceneModeWidget.js
 * 作者：巩志远
 * 部门：产品研发中心
 * 邮箱：gongzy@geovis.com
 * 日期：2017-03-03 23:23:38.
 * 用途：类
 */

class SceneModeWidget extends GV.Widget {

  	init() {

	    this.css('./SceneMode.css');
	    this.html('./SceneMode.html');
	    let viewMode = '3D';
	    var this_ = this; 
		//左侧面板添加二三维切换
		$(".minig-nav").append($(".wrap_2_3"));
	    $('.wrap_2_3').click(() => {
	      if(viewMode === '3D') {
	      	viewMode = '2D'
	      } else {
	      	viewMode = '3D'
	      }
	      this.earth.viewMode = viewMode;
	    });
 
  	}

}

//# sourceURL=SceneModeWidget.js 
