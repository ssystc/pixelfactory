/**
 * 项目：gvml
 * 文件：DistanceTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-05 19:37:20.
 * 用途：类
 */
class MoveObjectTool extends GV.Tool {

// get alias() {
//  return '量测工具';
// }
//
    init() {
    	console.log('move edit');
		this.distance = this.earth.getMapTool('MoveEdit').select(); 
    }
    
    remove() {
    	this.earth.clearMapTool();
    }
}
