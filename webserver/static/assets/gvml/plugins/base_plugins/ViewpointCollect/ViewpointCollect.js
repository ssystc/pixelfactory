/**
 * 项目：gvml
 * 文件：ViewpointCollect.js
 * 作者：董波
 * 部门：产品研发中心
 * 邮箱：dongb@mail.ie.ac.cn
 * 日期：2017-04-13 16:11:36.
 * 用途：视点收藏挂件
 */
class ViewpointCollect extends GV.Widget {

    get alias() {
        return '视点收藏';
    }

    init() {
        console.log('...viewPoint');

        this.viewpointList = [];
        this.camera = this.earth.camera;
//      this.fun = function (info) { console.log(info); }
		this.count = -1;
    }

    /**
     * 读取文件得到视点数据
     * @param fileUrl{String} 文件路径
     */
    openFile(fileUrl) {
        if (fileUrl) {
            this.fileUrl = fileUrl;
        }

        const jsonUrl = GV.Util.formatURL('./viewpoints/temp.json', GV.config.WindowLocation);
        const json = GV.Util.jsonSyncPromise(jsonUrl).responseJSON;
        if (json) {
            this.viewpointList = json;
            if (this.fun) { this.fun(this.viewpointList); }
        } 
    }

    /**
     * 保存视点数据文件
     * @param fileUrl{String} 文件保存路径
     */
    saveFile() {
        
        let fileUrl = this.fileUrl;
        
        if (fileUrl) {
            fileUrl = `${fileUrl}temp.json`;
            window.saveFile(JSON.stringify(this.viewpointList), fileUrl);
        }

    }

    /**
     * 添加视点数据
     * 一条视点数据示例{id：1123213，imageUrl: 1123213.png, vp: vp(从相机获取的对象)}
     */
    addViewpoint() {
        const vpData = {};
        vpData.id = GV.Util.createGuid();
        vpData.imageUrl = `${vpData.id}.png`;
        vpData.vp = this.camera.getViewPoint();
        if (vpData.vp) {
            this.earth.saveFramImage({url: `${this.fileUrl}/${vpData.imageUrl}`, wide: 200, high: 200});
            this.viewpointList.push(vpData);
			this.saveFile();
            // 延迟执行确保图片已经保存
            const that = this;
            
            if(this.fun) {
            	window.setTimeout(() => {
                	that.fun(that.viewpointList);
            	}, 3000);
            }

        }
    }

    /**
     * 删除视点数据
     * @param id{String} 视点id
     */
    removeViewpoint(id) {
        if (this.viewpointList && this.viewpointList.length > 0) {
            let count = 0;
            for (; count < this.viewpointList.length; count++) {
                if(this.viewpointList[count].id === id) break;
            }

            if(count !== this.viewpointList.length) {
                this.viewpointList.splice(count, 1);
                this.saveFile();
                // 应该删除对应图片后续加上
            }
        }

		if(this.fun) {
			this.fun(this.viewpointList);
		}
   
    }

    /**
     *清空视点数据
     */
    clearViewpoint() {
        this.viewpointList.clear();
        if(this.fun) {
        	this.fun(this.viewpointList);
        }
        
    }

    /**
     * 得到数据列表
     */
    getViewpointList() {
        return this.viewpointList;
    }

    /**
     * 飞到指定视点下
     */
    flyTo(id, time) {
        let i = 0
        for (; i < this.viewpointList.length; i++) {
            if (this.viewpointList[i].id === id) {break;}
        }
        if (i !== this.viewpointList.length) {
            const data = this.viewpointList[i];
            if(!time) time = 2;
            this.camera.setViewPoint(data.vp, time);
        }

    }
    
    getVp(i) {
    	if(this.viewpointList.length ===0) return undefined;
		this.count += i;
		if(this.count <0) this.count = 0;
		if(this.count >=this.viewpointList.length ) this.count = this.viewpointList.length - 1;
		
		const data = this.viewpointList[this.count];
		if(data && data.vp) return data.vp;
		return undefined;
    }

    onUpdataList(fun) {
        this.fun = fun;
    }

}

//# sourceURL=ViewpointCollect.js 
