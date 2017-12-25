/**
 * 项目：gvml
 * 文件：DyntargetBubble.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */
class DyntargetBubble extends GV.Widget {

    get alias() {
        return '动目标信息标牌';
    }

    init() {
		// this.html('./MyTag.html');
    	// this.css('./css/MyTag.css');
        this.dynTargetBubble = this.earth.getMapWidget('DynTargetBubble').open();
        this.dynTargetBubble.on('add_bubble', this._addBubble.bind(this));
        this.dynTargetBubble.on('update_bubble', this._updataBubble.bind(this));
        this.dynTargetBubble.on('remove_bubble', this._removeBubble.bind(this));
    }

    _addBubble(bubble) {
        if (!this._bubbles) {
			this._bubbles = new Map();
			this._scene = new GV.GraphicScene(); 
			this.earth.addScene(this._scene);
		}

		if(bubble !== undefined && (bubble instanceof Array)) {
			bubble.forEach((value) => {
				if(value === undefined) return;
				const newbubble = new GV.Bubble({
					//position: {lon: value.lon, lat: value.lat, alt: value.alt},
					screenPosition: {x: value.x, y: value.y},
					text: value.data,
					visible: value.visible,
					bindingObject: value.id
				});
				this._bubbles.set(value.id, newbubble);
				this._scene.addNode(newbubble);
			});
		}
    }

	_updataBubble(bubbles) {
		if (!this._bubbles || !(bubbles instanceof Array)) return;

		bubbles.forEach((value) => {
			const tempBubble = this._bubbles.get(value.id);
			if(!tempBubble) return;
			//tempBubble.position = {lon: value.lon, lat: value.lat, alt: value.alt}
			tempBubble.screenPosition = {x: value.x, y: value.y};
			tempBubble.visible = value.visible; 
		});
	}

	_removeBubble(bubbles) {
		if (!this._bubbles || !(bubbles instanceof Array)) return;

		bubbles.forEach((value) => {
			if(value === undefined) return;
			value = value.toString();
			const tempBubble = this._bubbles.get(value);
			if(!tempBubble) return;
			this._bubbles.delete(value);
			this._scene.remove(tempBubble);
			tempBubble.clear();
		});

	}

	remove() {
		if(this.dynTargetBubble) {
			this.dynTargetBubble.close();
		}
	}

	
}

//# sourceURL=DyntargetTool.js 