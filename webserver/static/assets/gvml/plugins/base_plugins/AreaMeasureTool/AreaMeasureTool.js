/**
 * 项目：gvml
 * 文件：DistanceTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-05 19:37:20.
 * 用途：类
 */
class AreaMeasureTool extends GV.Tool {

  init() {

    this.areaMeasureTool = this.earth.getMapTool('AreaMeasure').select();
    this.areaMeasureTool.on('area_sendtojs', this._getInfo);
  }
    _getInfo(info) {
    	console.log(info);
    }
  remove() {
    this.earth.clearMapTool();
  }
  HistoryRecord(para)
  {
  	this.areaMeasureTool.postMessage('HistoryRecord',para);
  }
  
}
