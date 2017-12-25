class MyBubble {
    constructor( container ,params = {}) {
		console.log('New MyBubble: ', params.id);
        this._id = `bubble_of_${params.id}`;
        this._bindObject = params.id;
        this._visible = params.visible;
        this._showRange = true;     // 相机变化导致Bubble的显隐变化
        this._position = params.position;
        this._container = container;
        this._info = params.info;
        this._name = params.name;
        this._num = params.num;
        this._pluginUrl = params.baseurl;
        this.clickFn = []; // 存放各个面板单击触发事件
        this.closeFn = []; // 存放各个面板单击关闭事件
        // this._initHTML(params.info);
        this.isMouseDown = false;
		this.downX = 0;
		this.downY = 0;
		this.bottomX = 0;
		this.bottomY = 0;
        this._isPositionChanged = false; // 判断是否位置发生变化
    }

    /**
     * 是否可见
     * @property visible
     * @type Boolean
     * @default false
     */
    set visible(visible = false) {
        this._visible = visible;
        if (this._visible === true) {
            this.render();
        } else {
            this.unrender();
        }
    }

    get visible() {
        return this._visible;
    }

    /**
     * 屏幕坐标位置
     * @method screenPosition
     */
    set position(screenPosition) {
        this._position = screenPosition;
        this._updatePosition();
    }

    get position() {
        return this._position;
    }

    set bindObject(id) {
        this._bindObject = id; 
    }

    get bindObject() {
        return this._bindObject;
    }

    set showRange(range = true) {
        this._showRange = range;
        if (this._moveDiv) {
            if (this._showRange === true) {
                this._moveDiv.css({ display: 'block' });
                this._line.css({ display: 'block' });
            } else {
                this._moveDiv.css({ display: 'none' });
                this._line.css({ display: 'none' });
            }
        }
    }

    get showRange() {
        return this._showRange;
    }

    /**
     * 更新Bubble
     * 参数为c++传过来的visible和position
     */
    updateBubble(nextProps) {
        // console.log(nextProps);
        if (this.visible !== nextProps.visible) this.visible = nextProps.visible;
        if (this.visible === true && this.showRange === true) {
            if (this.position.x !== nextProps.x || this.position.y !== nextProps.y) {
                // console.log('update_bubble: ', nextProps);
                this.position = {
                    x: nextProps.x,
                    y: nextProps.y
                };
            }
        }
    }

    /**
     * 标牌渲染函数
     * 说明：（以下为我写的代码逻辑说明，如果不符合需求，可在对应代码处自己修改）
     * 1. 名称： 先判断c++给了目标名称没，再看EP_targetInfo是否传了名称来，如果都没有则显示ID。
     * 2. geovis_tag_moveDiv： moveDiv目前固定大小514*320，要改的话在MyTag.css
     * 3. clickFn代表点击触发事件，closeFn代表点击关闭事件，index是一一对应的
     *      但都不是必须的，具体定义全在DyntargetTool里面new MyBubble的时候定义，这边别随便改了
     * 4. 点击关闭按钮暂时不要，如果一定要要自己得添加visible：false的消息发给c++，否则关不了
     */
    render() {
        this._moveDiv = $('<div id="'+this._id+'" class="geovis_tag_moveDiv">').appendTo(this._container);
		this._line = $('<div class="geovis_tag_line"></div>').appendTo(this._container);
        this._moveDiv.css({
            position: 'absolute',
            left: `${this.position.x}px`,
            top: `${this.position.y}px`
        });
        if (this._info) { // 如果有info消息的话
            let content = '';
            this._info.showAttr.forEach((item, key) => {
                // console.log(item, key);
                if (item.type === 'full') {
                    content += `
                        <div class="geovis_tag_content_full${key === 0 ? ' geovis_tag_content_top' : ''}">
                            <span data-prop="${item.attr}">${item.name}</span>
                            <span>${item.value}</span>
                        </div>
                    `;
                } else if (item.type === 'half') {
                    content += `
                        <div class="geovis_tag_content_half">
                            <span data-prop="${item.attr[0]}">${item.name[0]}</span>
                            <span>${item.value[0]}</span>
                            <span data-prop="${item.attr[1]}">${item.name[1]}</span>
                            <span>${item.value[1]}</span>
                        </div>
                    `;
                } else if (item.type === 'func') {
                	let btnSpan = '';
                    item.attr.forEach((vl, id) => {
                        btnSpan += `
                        <span id="${vl}" class="geovis_tag_content_func_span" style="background-color: #3E3E3E;">
                            ${item.name[id]}
                        </span>`;
                    });
                    content += `
                        <div class="geovis_tag_content_func">${btnSpan}</div>
                    `;
                }
            });
            const innerhtml = `
                <div class="geovis_tag_container">
                    <div class="geovis_tag_title">
                        <span class="geovis_tag_title_span">
                            ${this._name ? this._name : this._info.name ? this._info.name : `目标ID: ${this._bindObject}`}
                        </span>
                        <!--div class="geovis_tag_title_cancel"></div-->
                    </div>
                    <div class="geovis_tag_content">
                        ${content}
                    </div>
                </div>`;
            $(this._moveDiv).html(innerhtml);
            // 定义拖拽部分和事件
            // 定义关闭事件  ----- 目前这个不要了，要的话，得自己添加消息给c++，让c++发的消息的visible为false
            // $(`#${this._id} .geovis_tag_title_cancel`).css({
            //     backgroundImage: `url(${GV.Util.formatURL('./img/close.png', this._pluginUrl)})`
            // });
            // $(`#${this._id} .geovis_tag_title_cancel`).click(() => {
            //     // this.unrender();
            // });
            // 定义面板按钮点击事件
            const funcInfo = this._info.showAttr[this._info.showAttr.length - 1];
            funcInfo.attr.forEach((val, ind) => {
                $(`#${this._id} #${val}`).click((e) => {
                    if (this.rgb2hex(e.target.style.backgroundColor) === '#3E3E3E') {
                        e.target.style.backgroundColor = '#247994';
                        if (this.clickFn[ind]) this.clickFn[ind](this._bindObject, this._info);
                    } else {
                        e.target.style.backgroundColor = '#3E3E3E';
                        if (this.closeFn[ind]) this.closeFn[ind](this._bindObject, this._info);
                    }
                });
            });
            // 定义拖拽事件部分
            this._moveDiv.mousedown((e) => {
                if (e.which === 1) {
                    this.isMouseDown = true;
                    // this._line.hide();
                    this.downX = e.clientX - this._moveDiv[0].offsetLeft;
                    this.downY = e.clientY - this._moveDiv[0].offsetTop;
                    this.bottomX = this._moveDiv[0].offsetWidth - this.downX;
                    this.bottomY = this._moveDiv[0].offsetHeight - this.downY;
                }
            });

            this._moveDiv.mousemove((e) => {
                if (this.isMouseDown === true) {
                    if (this._isPositionChanged === false) this._isPositionChanged = true;
                    if (e.clientX >= 0 && e.clientY >= 0 && e.clientX + this.bottomX <= document.body.clientWidth
                        && e.clientY + this.bottomY <= document.body.clientHeight) {
                            this._moveDiv.css({
                                left: (e.clientX-this.downX) + 'px',
                                top: (e.clientY-this.downY) + 'px'
                            });
                        //	this._changeScreenPoint();
                        this._rotateLine({
                            x: this.position.x,
                            y: document.body.clientHeight - this.position.y
                        }, this._moveDiv[0]);
                    }
                }
            });

            this._moveDiv.mouseup(() => {
                this.isMouseDown = false;
                this.downX = 0;
                this.downY = 0;
                this.bottomX = 0;
                this.bottomY = 0;
            });
        }
    }

    // rgb(r,g,b) to #RRGGBB
    rgb2hex(str) {
        const str2rgb = (str) => {
            const sub = str.substring(4, str.length - 1);
            const rgbArr = sub.split(',');
            for (let i = 0; i < rgbArr.length; i++) {
                rgbArr[i] = parseInt(rgbArr[i], 0);
            }
            return { r: rgbArr[0], g: rgbArr[1], b: rgbArr[2] };
        }
        const dec2hex = (dec) => {
            const arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
            const divider = Math.floor(dec / 16);
            const remainder = dec % 16;
            if (dec > 255 || divider > 15) return `${arr[15]}${arr[15]}`;
            return `${arr[divider]}${arr[remainder]}`;
        }
        const rgb = str2rgb(str);
        return `#${dec2hex(rgb.r)}${dec2hex(rgb.g)}${dec2hex(rgb.b)}`;
    }

    _rotateLine(object, bindNode) {
		var start = object;
		var offsetWidth = bindNode.offsetWidth;
		var offsetHeight = bindNode.offsetHeight;
		var node =  {
			x: bindNode.offsetLeft + offsetWidth / 2,
			y: bindNode.offsetTop + offsetHeight / 2
		};
		var end = {x:0, y: 0};
		var deltaX = node.x - start.x;
		var deltaY = node.y - start.y;
		var tan_alpha = 0;
		/**
		 *    t = tan(a) = deltaY / deltaX;  
		 *     \  t > 1   |  t < -1  /
		 *      \         |         /
		 *  0<t<1\   二   |  一    / 0>t>-1
		 *        \       |       /
		 * ----------------------------------
		 *         /      |       \
		 *  -1<t<0/  三   |    四  \ 0<t<1
		 *       /        |         \
		 *      /  t < -1 |   t > 1  \    
		 */
		// 正上方 // JS 支持 无穷 +/- Infinity
		// console.log(deltaX, deltaY);
		if (deltaX > 0 && deltaY > 0) { // 四
			end.x = bindNode.offsetLeft;
			end.y = bindNode.offsetTop;
		} else if (deltaX > 0 && deltaY < 0) { // 一
			end.x = bindNode.offsetLeft;
			end.y = bindNode.offsetTop + offsetHeight;
		} else if (deltaX < 0 && deltaY < 0) { // 二
			end.x = bindNode.offsetLeft + offsetWidth;
			end.y = bindNode.offsetTop + offsetHeight;
		} else if (deltaX < 0 && deltaY > 0) { // 三
			end.x = bindNode.offsetLeft + offsetWidth;
			end.y = bindNode.offsetTop;
		}
		deltaX = end.x - start.x;
		deltaY = end.y - start.y;
		// console.log(bindNode.offsetLeft, offsetWidth, end.x);
		// console.log(bindNode.offsetTop, offsetHeight, end.y);
		// console.log('---------------------------------------');
		// 计算start 和 end 的 长度以及偏角
		var lineLength = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
		var radius = lineLength / 2;
		// 算出来角度
		var du = Math.acos(deltaX / lineLength) * (deltaY < 0 ? -1 : 1);
		var deg = du / Math.PI * 180;

		var dy_ = radius * Math.sin(du);
		var dx_ = radius * Math.cos(du) - radius;
		// DOM
		var line = this._line[0];
		line.style.width = lineLength + 'px';
		line.style.transform = `translate(${dx_}px,${dy_}px) rotate(${deg}deg)`;
		line.style.left = (start.x) +'px';
		line.style.top = (start.y) +'px';
	}

    // 标牌位置更新函数
    _updatePosition() {
        if (this._moveDiv) {
            if (this._isPositionChanged === false) {  // 如果没有发生过拖拽，则更新标牌位置
				this._moveDiv.css({
                    position: 'absolute',
                    left: `${this.position.x}px`,
                    top: `${document.body.clientHeight - this.position.y}px`
                });
			} else { // 如果位置被拖拽过，则更新线段
				this._rotateLine({
					x: this.position.x,
					y: document.body.clientHeight - this.position.y
				}, this._moveDiv[0]);
			}
            
        }
    }

    unrender() {
        if (this._moveDiv) $(this._moveDiv).remove();
        if (this._line) $(this._line).remove();
        // if (this.clickFn) this.clickFn = undefined;
        this._moveDiv = undefined;
        this._line = undefined;
        this._visible = false;
        this._isPositionChanged = false;
    }

    // 危险操作，彻底摧毁MyBubble
    destroy() {
        this.unrender();
        this.clickFn = [];
        this.closeFn = [];
        this._bindObject = undefined;
        this._container = undefined;
        this._info = undefined;
    }
}