/**
 * 项目：gvml
 * 文件：DistanceTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-05 19:37:20.
 * 用途：类
 */
class RouteEditTool extends GV.Tool {

// get alias() {
//  return '量测工具';
// }
//
    init() {
    	console.log('route edit');
		this.distance = this.earth.getMapTool('RouteEdit').select(); 
    }
    
    remove() {
    	this.earth.clearMapTool();
    }
}
