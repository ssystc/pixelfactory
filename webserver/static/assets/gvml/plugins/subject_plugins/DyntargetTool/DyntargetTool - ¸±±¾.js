/**
 * 项目：gvml
 * 文件：DyntargetTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */

class MyBubble {
    constructor( container ,params = {}) {
		this._container = container;
		this._isShow = true;

		this._initHTML();
		for(const key in params) {
			this[key] = params[key];
		}
    }

    _initHTML() {
        this._moveDiv = $('<div class="moveDiv">').appendTo(this._container);
        if (this._movedivCss) {
            this._moveDiv.css(this._movedivCss);
        } else {
            this._moveDiv.css({
                    position: 'absolute',
                });
        }


        this._smallShow = $('<div style="display: none">').appendTo(this._moveDiv);

        this._bigShow = $('<div style="display: none">').appendTo(this._moveDiv);
       
        this._showSign = 0;
        const that = this;

        this._moveDiv.dblclick(() => {
            that._showSign++;
            if (that._showSign === 2) {
                that._showSign = 0;
            }

            switch (that._showSign) {
                case 0:
                    this._bigShow.hide();
                    break;
                case 1:
                    this._bigShow.show();
                    break;
            }
        })

        this._moveDiv.mousedown((e) => {
            if (e.which == 3) {
                if (that && this._clickFun) {
                    that._clickFun(that.bindingObject);
                }
            }   
        });
    }

    set showRange(showRange) {
        if (this._showRange === showRange) return;
        this._showRange = showRange;
        this._show();

    }

    get showRange() {
        return this._showRange;
    }

    set movedivCss(movedivCss) {
        this._movedivCss = movedivCss;
    }

    set smallHtml(html) {
        this._smallHtml = html;
    }

    set bigHtml(html) {
        this._bigHtml = html;
    }

    set smallCss(css) {
        this._smallCss = css;
    }

    set bigCss(css) {
        this._bigCss = css;
    }

    set show(show) {
        if (show === undefined) return;
        if (show !== this._isShow) {
            this._isShow = show;
            this._show();
        }
    }

    get tag() {
        return TagsEnum.Bubble;
    }

    setMap(map) {
        super.setMap(map);
        //this.position = this.position;
        this.screenPosition = this.screenPosition;
    }

    _show() {
        if (this._visible === undefined || this._showRange === undefined) return;
        if (this._visible && this._showRange && this._isShow) {
           this._moveDiv.show();
           this._smallShow.show();
           this._bigShow.hide();

        } else {
            this._smallShow.hide();
            this._bigShow.hide();
            this._moveDiv.hide();
        }
    }

    /**
     * 是否可见
     * @property visible
     * @type Boolean
     * @default true
     */
    set visible(visible = true) {
        if (!this._moveDiv) return;
        if (this._visible === visible) return;
        this._visible = visible;
        this._show();
    }

    get visible() {
        return this._visible;
    }

    /**
     * 屏幕坐标位置
     * @method screenPosition
     */
    set screenPosition(screenPosition) {
        if (!screenPosition) return;

        if (!this._screenPosition) {
            this._screenPosition = {};
      
            if (this._smallHtml) this._smallShow.html(this._smallHtml);
            if (this._bigHtml) this._bigShow.html(this._bigHtml);
            if (this._smallCss) this._smallShow.css(this._smallCss);
            if (this._bigCss) this._bigShow.css(this._bigCss);
        } 
        this._screenPosition = screenPosition;
        if (this._moveDiv) {
            this._moveDiv.css({
                bottom: screenPosition.y,
                left: screenPosition.x
            });
        }
    }

    get screenPosition() {
        return this._screenPosition;
    }

    /**
     * 广告显示内容
     */
    set text(text) {
        this._text = text;
    }

    get text() {
        return this._text;
    }

    set bindingObject(id) {
        this._bindingObject = id; 
    }

    get bindingObject() {
        return this._bindingObject;
    }

    set clickFun(fun) {
        this._clickFun = fun;
    }

    /**
     * 清空数据
     */
    clear() {
	    if (this._smallShow) {
            this._smallShow.remove();
        }
        if (this._bigShow) {
            this._bigShow.remove();
        }
        if (this._moveDiv) {
            this._moveDiv.remove();
        }
    }

}

class DyntargetTool extends GV.Widget {

    get alias() {
        return '动目标信息';
    }

    init() {
		this.css('./ami.css');
		this.css('./MyTag.css');
    	var that = this;
		//this._readFile();
		this.dynTarget = this.earth.getMapWidget('DynTarget').open();
//      this.dynTarget.on("dyntarget_selectioninfor",this.dynTargetSelection);
//      this.dynTarget.on("dyntarget_countInfo",this.dynTargetCountInfo);

        //this.dynTargetBubble = this.earth.getMapWidget('DynTargetBubble').open();
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
			
            //this.dynTarget.postMessage("GeoVIS::GVDynTargetPlugin::DynTargetMessage", "startrealdyntarget;");

        
    }
    //频谱占用度 统计数据生成
    FreqOccu(data)
    {
    	console.log("FreqOccu  数据" + data);
    	
    }
    //空间覆盖率统计数据生成
    SpaceOccu(data)
    {
    	console.log("SpaceOccu  数据" + data);
    }
    //信号密度统计生成
    SignalDensity(data)
    {
    	console.log("SignalDensity  数据" + data);
    }
 	//复杂度变化 曲线生成
    Complex(data)
    {
    	console.log(data);
    	console.log("上面数组是  Complex  数据");
    }
    //复杂度统计饼图数据生成
    ComplexPie(data)
    {
    	console.log(data);
    	console.log("上面数组是  ComplexPie  数据");
    }

	setData(data) {
		if(data instanceof Array) {
			this._data = data;
			const that = this;
			if (!this._bubbles) return;
			this._bubbles.forEach((value) => {
				if(that._isHave(value.num)) {
					value.show = true;
				} else {
					value.show = false;
				}
			});
		}
	}

	_isHave(id) {
		if(!this._data) return false;

		for(let i = 0; i < this._data.length; i++) {
			if(this._data[i] == id)
				return true;
		}
		return false;
	}

	showBubble() {
		this.dynTarget.postMessage('show_bubble');
	}

	hideBubble() {
		this.dynTarget.postMessage('hide_bubble');

		//因为接受到的删除bubble的数据有问题临时这么清理
		if(this._bubbles === undefined) return;

		this._bubbles.forEach((bubble) => {
			if(!bubble) return;
			this._scene.remove(bubble);
			bubble.clear();

		});
		this._bubbles.clear();
	}
	startStaticTarget(v)
	{
		this.dynTarget.postMessage('start_statictarget',v);
	}
	startNBHKData(v)
	{
		this.dynTarget.postMessage('start_NBHKData',v);
	}
	startNBWXData(v)
	{
		this.dynTarget.postMessage('start_NBWXData',v);
	}
	startServerHKData(v)
	{
		this.dynTarget.postMessage('start_ServerHKData',v);
	}
	setViewPort(v)
	{
		this.dynTarget.postMessage('set_ViewPort',v);
	}
	
	FreqOccuDegreeStatistics()
	{
		this.dynTarget.postMessage('FreqOccuDegreeStatistics');
	}
	SpaceOccuDegreeStatistics()
	{
		this.dynTarget.postMessage('SpaceOccuDegreeStatistics');
	}
	SignalDensityStatistics()
	{
		this.dynTarget.postMessage('SignalDensityStatistics');
	}
	ComplexDegreeChangeWithTime()
	{
		this.dynTarget.postMessage('ComplexDegreeChangeWithTime');
	}
	ComplexPieStatistics()
	{
		this.dynTarget.postMessage('ComplexPieStatistics');
	}
	StartRadar()
	{
		this.dynTarget.postMessage('StartRadar');		
	}
	CreateTargetType(v)
	{
		this.dynTarget.postMessage('CreateTargetType',v);	//v:targetType  radar or air 
	}
	RadarLayerChanged(rdjson)
	{
		this.dynTarget.postMessage('RadarLayerChanged',rdjson);//
	}
	
	RadarModelChanged(rdmodel)
	{
		this.dynTarget.postMessage('RadarModelChanged',rdmodel);
	}
	
	SaveCurrentArea(areaName)
	{
		alert(areaName)
		this.dynTarget.postMessage('SaveCurrentArea',areaName);
	}
	RequestCurrentArea(areaName)
	{
		alert(areaName)
		this.dynTarget.postMessage('RequestCurrentArea',areaName);
	}
	LookatTarget(id)
	{
		alert(id)
		this.dynTarget.postMessage('LookatTarget',id);
	}

//  dynTargetSelection(info)
//  {
//
//  }
//  dynTargetCountInfo(info)
//  {
//
//  }

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

	_rangeChange(data) {
		const range = data.viewpoint.range;
		if(this._bubbles) {
			let showRange;
			if(range > 10000000) {
				showRange = false;
			}else{
				showRange = true;
			}
			this._bubbles.forEach((bubble) => {
				bubble.showRange = showRange;
			});
		}
	}

	_readFile() {
		const that = this;
		$.ajax({
			type:"get",
			url:"yanshi/test2.json",
			async:true,
			success:function(res) {
				that._data = res;
			}
		});
	}

    _createHtml(value, data) {

		if(!value || !data || !data.data)
			return `<p>${value.num}</p>`;

		let type = value.num;
		type = parseInt(type);
		let targetInfo;
		data.data.forEach((info) => {
			if ( info && info.num !== undefined && info.num === type ) {
				targetInfo = info;
			}
		});

		if(targetInfo === undefined)
			return `<p>${value.id}</p>`;

		let content;
		if(value.attr === '1') {
			content = `<div class="LeftContent">
					<div class="LeftSureBtn">我方目标</div>
					<div class="SearchAll">
						<div class="title">目标</div>
						<p>${value.name}</p>
					</div>
					<div class="SearchSure">
						<div class="title">详细信息</div>
						<p>country:${targetInfo.country}</p>
						<p>platform:${targetInfo.platform}</p>
						<p>role:${targetInfo.role}</p>
					</div>
				</div>`;
		}else{
			content = `<div class="SeachedAim">
						<div class="SureBtn">目标型号确认</div>
						<div class="SearchAll">
							<div class="title">侦察到电子目标</div>
								<p>country:${targetInfo.country}</p>
								<p>platform:${targetInfo.platform}</p>
								<p>role:${targetInfo.role}</p>
						</div>
						<div class="SearchSure">
							<div class="title">确认目标</div>
							<p>${value.name}   100%</p>
							<p>目标管控等级   ${value.attr}</p>
						</div>
					</div>`;
		}
		return content;
	}

    _addBubble(bubble) {
        if (!this._bubbles) {
			this._bubbles = new Map();
		}
		const that = this;
		if(bubble !== undefined && (bubble instanceof Array)) {
			bubble.forEach((value) => {
				if(value === undefined) return;

				let smallHtml;
				
				if(value.attr === '1') {
					smallHtml = `<div class = "1232" style = "position: absolute; bottom: -111px; left: 51px"><div class="geovis_tag_container">
            <div class="geovis_tag_title">
                <span class="geovis_tag_title_span">辽宁号</span>
                <div class="geovis_tag_title_cancel"></div>
            </div>
            <div class="geovis_tag_content">
                <div class="geovis_tag_content_coord">
                    <span>坐标</span>
                    <span>东经：121°2545' &nbsp 北纬：121°2545'</span>
                </div>
                <div class="geovis_tag_content_time">
                    <span>时间</span>
                    <span>2017年6月6日11:30:19</span>
                </div>
                <div class="geovis_tag_content_forces">
                    <span>部队</span>
                    <span>第一部队</span>
                    <span>坐标</span>
                    <span>第一部队</span>
                </div>
                <div class="geovis_tag_content_func">
                    <span class="geovis_tag_content_func_span" style="background: #247994;">雷达知识库</span>
                    <span class="geovis_tag_content_func_span" style="background: #3E3E3E;">影响特征</span>
                    <span class="geovis_tag_content_func_span" style="background: #3E3E3E;">航路分析</span>
                    <span class="geovis_tag_content_func_span" style="background: #3E3E3E;">重点目标</span>
                </div>
            </div>
        </div></div>`;//`<div class="LeftDet">${value.name}</div>`;
				} else {
					smallHtml = `<div class="123213" style = "position: absolute; bottom: -111px; left: 51px"><div class="geovis_tag_container">
            <div class="geovis_tag_title">
                <span class="geovis_tag_title_span">辽宁号</span>
                <div class="geovis_tag_title_cancel"></div>
            </div>
            <div class="geovis_tag_content">
                <div class="geovis_tag_content_coord">
                    <span>坐标</span>
                    <span>东经：121°2545' &nbsp 北纬：121°2545'</span>
                </div>
                <div class="geovis_tag_content_time">
                    <span>时间</span>
                    <span>2017年6月6日11:30:19</span>
                </div>
                <div class="geovis_tag_content_forces">
                    <span>部队</span>
                    <span>第一部队</span>
                    <span>坐标</span>
                    <span>第一部队</span>
                </div>
                <div class="geovis_tag_content_func">
                    <span class="geovis_tag_content_func_span" style="background: #247994;">雷达知识库</span>
                    <span class="geovis_tag_content_func_span" style="background: #3E3E3E;">影响特征</span>
                    <span class="geovis_tag_content_func_span" style="background: #3E3E3E;">航路分析</span>
                    <span class="geovis_tag_content_func_span" style="background: #3E3E3E;">重点目标</span>
                </div>
            </div>
        </div></div>`;//`<div class="RightDet">${value.name}</div>`;
				}
				let bigHtml = this._createHtml(value, this._data);
				const newbubble = new MyBubble(that.earth.container,{
					
					text: value.data,
					visible: value.visible,
					bindingObject: value.id,
					smallHtml: smallHtml,
					bigHtml: bigHtml,
					movedivCss:{
								position: 'absolute',
								float: 'left',
								cursor: 'pointer'
							},
					screenPosition: {x: value.x, y: value.y}
				});
				newbubble.num = value.num;
				newbubble._moveDiv.data('data',value.id);
				newbubble.clickFun = function(id) {
					let that = this;
					console.log(id);
					console.log(this.bindingObject);
				}

				this._bubbles.set(value.id, newbubble);
			 	
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
			tempBubble.clear();
		});

	}

    remove() {
		if(this.dynTarget) {
			this.dynTarget.close();
		}
    }
}

//# sourceURL=DyntargetTool.js 
