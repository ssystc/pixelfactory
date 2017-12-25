/**
 * 项目：gvml
 * 文件：DyntargetTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */

class DyntargetTool extends GV.Widget {

    get alias() {
        return '动目标信息';
    }

    init() {
		this.css('./ami.css');
		this.css('./MyTag.css');
		this.script('./MyBubble.js');
    	this._showRange = true;
		//this._readFile();
		this.dynTarget = this.earth.getMapWidget('DynTarget').open();
		// this.dynTarget.on("dyntarget_selectioninfor",this.dynTargetSelection);
		// this.dynTarget.on("dyntarget_countInfo",this.dynTargetCountInfo);

        /**
		 * to 晓琳： 这里改一下，改成监听你的EP_targetInfo
		 */
		//this.dynTarget.on('EP_TargetInfo', this._updataInfo.bind(this));
        this._updataInfo();
        this.dynTarget.on('add_bubble', this._addBubble.bind(this));
        this.dynTarget.on('update_bubble', this._updataBubble.bind(this));
        this.dynTarget.on('remove_bubble', this._removeBubble.bind(this));
		
        this.dynTarget.on('dyntarget_FreqOccuDegreeStatistics', this.FreqOccu);
        this.dynTarget.on('dyntarget_SpaceOccuDegreeStatistics', this.SpaceOccu);
        this.dynTarget.on('dyntarget_SignalDensityStatistics', this.SignalDensity);
        this.dynTarget.on('dyntarget_ComplexDegreeChangeWithTime', this.Complex);
        this.dynTarget.on('dyntarget_ComplexPieStatistics', this.ComplexPie);

		//监听相机高度
		this.earth.camera.onCameraChange(this._rangeChange.bind(this));

		// this.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "startrealdyntarget;");
        
    }
    //频谱占用度 统计数据生成
    FreqOccu(data) { console.log("FreqOccu  数据" + data); }
    //空间覆盖率统计数据生成
    SpaceOccu(data) { console.log("SpaceOccu  数据" + data); }
    //信号密度统计生成
    SignalDensity(data) { console.log("SignalDensity  数据" + data); }
 	//复杂度变化 曲线生成
    Complex(data) { console.log(data); console.log("上面数组是  Complex  数据"); }
    //复杂度统计饼图数据生成
    ComplexPie(data) { console.log(data); console.log("上面数组是  ComplexPie  数据"); }
	SaveCurrentArea(areaName) { alert(areaName); this.dynTarget.postMessage('SaveCurrentArea',areaName); }
	RequestCurrentArea(areaName) { alert(areaName); this.dynTarget.postMessage('RequestCurrentArea',areaName); }
	LookatTarget(id) { alert(id); this.dynTarget.postMessage('LookatTarget',id); }
	startStaticTarget(v) { this.dynTarget.postMessage('start_statictarget',v); }
	startNBHKData(v) { this.dynTarget.postMessage('start_NBHKData',v); }
	startNBWXData(v) { this.dynTarget.postMessage('start_NBWXData',v); }
	startServerHKData(v) { this.dynTarget.postMessage('start_ServerHKData',v); }
	setViewPort(v) { this.dynTarget.postMessage('set_ViewPort',v); }
	FreqOccuDegreeStatistics() { this.dynTarget.postMessage('FreqOccuDegreeStatistics'); }
	SpaceOccuDegreeStatistics() { this.dynTarget.postMessage('SpaceOccuDegreeStatistics'); }
	SignalDensityStatistics() { this.dynTarget.postMessage('SignalDensityStatistics'); }
	ComplexDegreeChangeWithTime() { this.dynTarget.postMessage('ComplexDegreeChangeWithTime'); }
	ComplexPieStatistics() { this.dynTarget.postMessage('ComplexPieStatistics'); }
	StartRadar() { this.dynTarget.postMessage('StartRadar'); }
	CreateTargetType(v) { this.dynTarget.postMessage('CreateTargetType',v);	}//v:targetType  radar or air 
	RadarLayerChanged(rdjson) { this.dynTarget.postMessage('RadarLayerChanged',rdjson); }
	RadarModelChanged(rdmodel) { this.dynTarget.postMessage('RadarModelChanged',rdmodel); }
	RadarSingleVisible(id, isVisible)
	{
		this.dynTarget.postMessage('RadarSingleVisible',id , isVisible);
	}
	ShowForceArea(id)
	{
		this.dynTarget.postMessage('ShowForceArea',id);
	}
	ViewChange23D()
	{
		this.dynTarget.postMessage('ViewChange23D');
	}
	RadarUnionHeight(heiList)
	{
		this.dynTarget.postMessage('RadarUnionHeight',heiList);
	}
	
	RadarUnionName(nameList)
	{
		this.dynTarget.postMessage('RadarUnionName',nameList);
	}
	
	/**
	 * to 晓琳： 这个函数改成你获取targetinfo并且赋给this._info
	 * this._info数据结构： 
	 * {
	 * 		id: 'suoyin', // 索引
	 * 		name: '', // 中文名称，没有则不用管，默认为undefined
	 * 		showAttr: [
	 * 			{ type: 'full', name: '中文名称（没有直接用Attr名）', attr: 'attr_name(可以自定义)', value: 'attr_value'},
	 * 			{ type: 'half', name: ['中文名称1', '中文名称2'], attr: ['attr1', 'attr2'], value: ['value1', 'value2']}, // 数组长度必须为2
	 * 			{ type: 'func', name: ['按钮名称1', '...', '...', '...'], attr: ['btn_id_1','','','']} // 数组长度根据所需改变, 最好不超过8个
	 * 		],
	 * 		otherAttr: { / 存放其它乱七八糟的Attr /}
	 * }
	 */
	_updataInfo() {
		const test_data = {
			row__array__: [
				{id: '1', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'A部队', dwsx: '敌', mmlb: 'kz目标'},
				{id: '2', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', szbd: 'B部队', dwsx: '敌'},
				{id: '3', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'C部队', dwsx: '我'},
				{id: '4', longitude: 100.2, latitude: 20.0, altitude: 0, asdc: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'D部队', dwsx: '我'},
				{id: '5', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'E部队', dwsx: '敌'},
				{code: '6', longitude: 100.2, latitude: 20.0, altitude: 0, bgdg: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'F部队', dwsx: '我'},
				{id: '7', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'G部队', dwsx: '我'},
				{id: '8', longitude: 100.2, latitude: 20.0, altitude: 0, sstt: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'B部队', dwsx: '敌'},
				{id: '9', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'D部队', dwsx: '敌'},
				{id: '10', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'C部队', dwsx: '我'},
				{id: '59', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'A部队', dwsx: '敌', mmlb: 'kz目标'},
				{id: '60', longitude: 100.2, latitude: 20.0, altitude: 0, mmmm: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'A部队', dwsx: '敌'},
				{code: '61', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', szbd: 'D部队', dwsx: '我'},
				{id: '62', longitude: 100.2, latitude: 20.0, altitude: 0, lkst: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'C部队', dwsx: '我'},
				{id: '63', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'B部队', dwsx: '敌'},
				{id: '64', longitude: 100.2, latitude: 20.0, altitude: 0, kyst: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'F部队', dwsx: '我'},
				{id: '65', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', szbd: 'E部队', dwsx: '敌'},
				{id: '66', longitude: 100.2, latitude: 20.0, altitude: 0, zdmb: '布吉岛', time: '2017-06-14 08:56:12', szbd: 'E部队', dwsx: '敌'}, // 目标不存在的情况, 也不会影响代码执行
				{id: '67', longitude: 100.2, latitude: 20.0, altitude: 0, bjdm: '布吉岛', time: '2017-06-14 08:56:12', ssbd: 'A部队', dwsx: '敌', mmlb: 'kz目标'},
				{id: '68', name: '辽宁号', longitude: 100.2, latitude: 20.0, altitude: 0, bjdm: '布吉岛', time: '2017-06-15 09:56:12', ssbd: 'B部队', dwsx: '敌', mmlb: 'dm目标'},
				{id: '69', longitude: 100.2, latitude: 20.0, altitude: 0, bjdm: '布吉岛', time: '2017-06-15 08:56:12', ssbd: 'A部队', dwsx: '敌', mmlb: 'dm目标'},
				{id: '30', name: '卡尔文森号', longitude: 100.2, latitude: 20.0, altitude: 0, bjdm: '布吉岛', time: '2017-06-15 09:56:12', ssbd: 'B部队', dwsx: '敌', mmlb: 'dm目标'},
				{id: '34', name: '夏普伦湖号',longitude: 100.2, latitude: 20.0, altitude: 0, bjdm: '布吉岛', time: '2017-06-15 08:56:12', ssbd: 'A部队', dwsx: '敌', mmlb: 'dm目标'}
			]
		};
		this._info = new Map();
		const mubiao_list = test_data.row__array__;
		for (let i = 0; i < mubiao_list.length; i++) {
			const id = mubiao_list[i].id ? mubiao_list[i].id : mubiao_list[i].code;
			const position_i = `经度：${mubiao_list[i].longitude} 纬度：${mubiao_list[i].latitude} 高度：${mubiao_list[i].altitude}`;
			const ssbd_i = mubiao_list[i].ssbd ? mubiao_list[i].ssbd : mubiao_list[i].szbd;
			const info = {
				id,
				name: mubiao_list[i].name, // 若果没有name不用管，如果别的属性是名称，则把mubiao_list[i].name替换成mubiao_list[i].(你的attr名称)
				showAttr: [
					{type: 'full', name: '坐标', attr: 'postion', value: position_i},
					{type: 'full', name: '时间', attr: 'time', value: mubiao_list[i].time},
					{type: 'half', name: ['部队', '敌我'], attr: ['ssbd', 'dwsx'], value: [ssbd_i, mubiao_list[i].dwsx]},
					{
						type: 'func',
					    name: ['知识库', '重点目标', '雷达范围', '打击范围'],
					    attr: [`zslib_func_${id}`, `yxtx_func_${id}`, `ldfw_func_${id}`, `djfw_func_${id}`]
					}
				],
				otherAttr: mubiao_list[i]
			};
			this._info.set(id, info);
		}
	}
	//画圆
	//createCircle   创建圆的命令
	//ciricle1        名称
	//115.0;35.0;100.0 圆的位置
	//10000.0          圆半径
	//1.0;0.0;0.0;1.0  圆颜色
	//var para = "createCircle;ciricle1;115.0;35.0;100.0;10000.0;1.0;0.0;0.0;1.0";
	//widget.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", para);

	//画矩形
	//createRectangle   创建矩形的命令
	//testrecangle        名称
	//120.0;35.0;100.0;120.0;40.0;100.0;125.0;40.0;100.0;125.0;35.0;100.0; 四个点坐标，顺时针
	//1.0;0.0;0.0;1.0  矩形颜色
	//var para = "createRectangle;testrecangle;120.0;35.0;100.0;120.0;40.0;100.0;125.0;40.0;100.0;125.0;35.0;100.0;1.0;0.0;0.0;1.0";
	//widget.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", para);

	//画文字
	//createText   创建矩形的命令
	//testtext        名称
	//118.0;35.0;100.0 文字位置
	//this is just for test  文字显示内容
	//1.0;0.0;0.0;1.0 文字颜色
	//32  文字大小
	//var para = "createText;testtext;118.0;35.0;100.0;this is just for test;1.0;0.0;0.0;1.0;32";
	//widget.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", para);
	/**
	 * ===============================================================================================================================
	 * 标牌相关函数
	 * 
	 */

	showBubble() {
		console.log('show_bubble');
		this.dynTarget.postMessage('show_bubble');
	}

	hideBubble() {
		console.log('hide_bubble');
		this.dynTarget.postMessage('hide_bubble');
	}

	_rangeChange(data) {
		if(!data || !data.viewpoint) return;
		const range = data.viewpoint.range;
		if(this._bubbles) {
			let showRange;
			if (range > 10000000) {
				showRange = false;
			} else {
				showRange = true;
			}
			if (this._showRange !== showRange) {
				// console.log(showRange);
				this._showRange = showRange;
				this._bubbles.forEach((bubble) => {
					bubble.showRange = showRange;
				});
			}
			
		}
	}
	// 接收消息添加bubble
    _addBubble(bubble) {
        // console.log(bubble[0].id);
		if (!this._bubbles) this._bubbles = new Map();
		if(bubble !== undefined && (bubble instanceof Array)) {
			bubble.forEach((value) => {
				if(value === undefined) return;
				if (!this._info.get(value.id)) this._info.set(value.id, {
					id: value.id,
					name: value.name,
					showAttr: [
						{type: 'full', name: '坐标', attr: 'postion', value: "暂无"},
						{type: 'full', name: '时间', attr: 'time', value: "暂无"},
						{type: 'half', name: ['部队', '敌我'], attr: ['ssbd', 'dwsx'], value: ["暂无", "暂无"]},
						{
							type: 'func',
							name: ['知识库', '重点目标', '雷达范围', '打击范围'],
							attr: [`zslib_func_${value.id}`, `yxtx_func_${value.id}`, `ldfw_func_${value.id}`, `djfw_func_${value.id}`]
						}
					],
					otherAttr: {}
				});
				const tempBubble = this._mountBubble(value);
				// console.log(tempBubble);
				this._bubbles.set(value.id, tempBubble);
				// console.log(this._bubbles.get(value.id));
			});
		}
    }
	// 实例化bubble
	_mountBubble(msg) {
		const info = this._info.get(msg.id);
		const bubble = new MyBubble(this.container, {
			id: msg.id,
			visible: msg.visible,
			name: msg.name,
			num: msg.num,
			position: {x: msg.x, y: msg.y},
			baseurl: this.url,
			info: info
		});
		// 下面是自定义标牌面板的按钮点击事件（clickFn）和关闭事件（closeFn）
		if (info) {
			info.showAttr[info.showAttr.length - 1].attr.forEach((value, index) => {
				if (index === 3) { // 定义clickFn 和 closeFn的情况
					bubble.clickFn[index] = (id, info) => {
						this.ShowForceArea(id);
					};
					bubble.closeFn[index] = (id, info) => { this.ShowForceArea(id); };
				} else if (index === 2) {
					bubble.clickFn[index] = (id, info) => {
						this.RadarSingleVisible(id, true);
					};
					bubble.closeFn[index] = (id, info) => { this.RadarSingleVisible(id, false); };
				} else if (index === 0) {
					bubble.clickFn[index] = (id, info) => {
						// this.添加知识库方法(id, info);
					};
				} else if (value === 'jdzl_func_1_6016') { // 只定义clickFn的情况
					bubble.clickFn[index] = (id, info) => { alert(info.otherAttr.ssbd); };
				}
			});
		}
		// console.log(bubble);
		return bubble;
	}

	_updataBubble(bubbles) {
		// console.log('update_bubble: ', bubbles);
		if(bubbles !== undefined && (bubbles instanceof Array)) {
			bubbles.forEach((value) => {
				if(value === undefined) return;
				const tempBubble = this._bubbles.get(value.id);
				if (tempBubble && tempBubble.isMouseDown === false)
					tempBubble.updateBubble(value);
					// tempBubble._info = new_info; //如果需要info变更的话
			});
		}
	}

	// 所有的bubble均删除
	_removeBubble(bubbles) {
		console.log('remove_bubble: ', bubbles);
		if(bubbles !== undefined && (bubbles instanceof Array)) {
			bubbles.forEach((value) => {
				if(value === undefined) return;
				const tempBubble = this._bubbles.get(value.id);
				tempBubble.destroy();
			});
		}
		this._bubbles = undefined;
	}

    remove() {
		super.remove();
		if(this.dynTarget) {
			this.dynTarget.close();
		}
    }
}

//# sourceURL=DyntargetTool.js 
