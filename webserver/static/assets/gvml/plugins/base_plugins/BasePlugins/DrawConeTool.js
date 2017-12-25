/**
 * 项目：gvml
 * 文件：DrawIconTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-18 13:49:28.
 * 用途：类
 */

class DrawConeTool extends GV.Tool {

  init() {
    this.drawConeTool = this.earth.getMapTool('DrawConeTool').select();
  }
  
  remove() {
  	this.earth.clearMapTool();
  }

}
