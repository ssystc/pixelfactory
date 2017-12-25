/**
 * 项目：gvml
 * 文件：DyntargetTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:27:20.
 * 用途：类
 */
const GV = window.GV;
class MarkPlugin extends GV.Tool {

    get alias() {
        return '全新标绘面板';
    }

    init() {
        this.script('./build/PlotPanel.js');
        // const pluginContainer = document.createElement('div');
        this._marking = true;
        GV.$(this.container).css({
            width: '404px',
            height: '924px',
            position: 'absolute',
            top: '64px',
            right: '100px'
        });
        this._pickTool = this.earth.getMapTool('targetSelect');
        this._initMarkView();
    }

    _initMarkView() {
        const that = this;
        const plotTool = new PlotPanel.PlottingView(this.container.id, {
            library: [
                {id: 'basic_mark', name: '基本标绘库', json: GV.Util.formatURL('./mark/basicMarkConfig/basic_mark.json', this.url)},
                {id: 'military_mark', name: '军事标绘库', json: GV.Util.formatURL('./mark/militaryMarkConfig/mil_mark.json', this.url)},
                {id: 'model_mark', name: '三维模型库'}
            ]
        });
        plotTool.propFunc = (prop, value) => {
            if (that._current_node) that._current_node[prop] = value;
        };
        plotTool.render();
        const hand = GV.$('<div className="mark_hand"></div>').appendTo(this.container);
        // console.log(GV.Util.formatURL('./assets/hand.png', this.url));
        hand.css({
            position: 'absolute',
            top: '9px',
            right: '13px',
            width: '32px',
            height: '32px',
            border: '1px solid #00a0e9',
            cursor: 'pointer',
            backgroundImage: `url(${GV.Util.formatURL('./assets/pen.png', this.url)})`,
            backgroundPosition: 'center',
            backgroundSize: '24px 24px',
            backgroundRepeat: 'no-repeat'
        });
        hand.click(() => {
            this._marking = !this._marking;
            if (this._marking === true) {
                hand.css({ backgroundImage: `url(${GV.Util.formatURL('./assets/pen.png', this.url)})`});
                this.earth.clearMapTool();
                this._current_node = undefined;
            } else {
                hand.css({ backgroundImage: `url(${GV.Util.formatURL('./assets/hand.png', this.url)})`});
                if (this._pickTool) this._pickTool.select();
            }
        });

        this._initMark(plotTool);

        if (this._pickTool) {
            this._pickTool.on('pick_obj', (uuid) => {
                that._current_node = this.earth.getNodeById(uuid);
                plotTool.renewPropPanel({
                    className: `GV.${that._current_node.constructor.name}`,
                    properties: that._current_node.toJson()[that._current_node.tag],
                });
            });
        }

    }

    _initMark(plotTool) {
        this.scene = new GV.GraphicScene();
        this.earth.addScene(this.scene);

        this.jbScene = new GV.JBScene();
        this.earth.addScene(this.jbScene);

        //监听鼠标位置变化
        let info;
        this.infobar = this.earth.getMapWidget('InfoBar').open();
        this.infobar.on('locationChange', (newInfo) => {
            if (!(newInfo instanceof Array) || newInfo.length < 4) { return; }
            if (!info) info = {};
            info.lon = newInfo[0];
            info.lat = newInfo[1];
            info.alt = newInfo[2] + 10000.0;
        });
        let node = {pos: [], node: undefined}
        this.earth.container.mouseup((event) => {
            if (event.button === 0 && this._marking === true && event.target.nodeName === 'EMBED') {
                if (this.scene && this.jbScene) {
                    const mark = plotTool.getMark();
					if (!mark) return;
                    if (mark.className === 'GV.JBLine' || mark.className === 'GV.Polygon' || mark.className === 'GV.Polyline') {
                        if (!node.node) this._addLine(info, mark, node);
                        else this._updateLine(info, node);
                    } else {
                        this._addMark(info, mark);
                    }
                }
            } else if (event.button === 2 && this._marking === true && event.target.nodeName === 'EMBED') {
                // this._marking = false;
                node = {pos: [], node: undefined};
            }
        });
    }

    _addLine(pos, mark, node) {
        if (!mark || !pos) return node;
        if (!pos.alt || pos.alt <= 10000.0) pos.alt = 10000.0;
        const options = mark.props;
        options.vertices = [];
        options.vertices.push([pos.lon, pos.lat, pos.alt]);
        switch (mark.className) {
            case 'GV.JBLine':
                options.code = mark.config.id;
                node.pos = options.vertices;
                node.node = new GV.JBLine(options);
                this.jbScene.addNode(node.node);
                break;
            case 'GV.Polygon':
                node.pos = options.vertices;
                node.node = new GV.Polygon(options);
                this.scene.addNode(node.node);
                break;
            case 'GV.Polyline':
                node.pos = options.vertices;
                node.node = new GV.Polyline(options);
                this.scene.addNode(node.node);
                break;
            default: break;
        }
        return node;
    }

    _updateLine(pos, node) {
        if (!pos) return node;
        if (!pos.alt || pos.alt <= 10000.0) pos.alt = 10000.0;
        node.pos.push([pos.lon, pos.lat, pos.alt]);
        node.node.addPoints([pos.lon, pos.lat, pos.alt]);
        return node;
    }

    _addMark(pos, mark) {
        if (!mark || !pos) return;
        if (pos.alt <= 10000.0) pos.alt = 10000.0;
        // console.log(pos);
        // console.log(mark);
        const options = mark.props;
        options.position = pos;
        switch (mark.className) {
            case 'GV.JBPoint':
                options.code = mark.config.id;
                options.textColor = mark.props.textColor.substring(0, 7);
                const jbpoint = new GV.JBPoint(options);
                this.jbScene.addNode(jbpoint);
                break;
            case 'GV.Label':
                const label = new GV.Label(options);
                this.scene.addNode(label);
                break;
            case 'GV.Place':
				options.icon = mark.props.icon === './assets/pin.png' ? GV.Util.formatURL(mark.props.icon, this.url) : mark.props.icon;
                const place = new GV.Place(options);
                this.scene.addNode(place);
                break;
            case 'GV.ImageOverLay':
                const ImageOverLay = new GV.ImageOverLay(options);
                this.scene.addNode(ImageOverLay);
                break;

            case 'GV.Model':
                const Model = new GV.Model(options);
                this.scene.addNode(Model);
                break;

            case 'GV.Circle':
                options.height = 0;
                options.arcStart = 0;
                options.arcEnd = 360;
                const Circle = new GV.Circle(options);
                this.scene.addNode(Circle);
                break;
            case 'GV.Cylinder':
                options.arcStart = 0;
                options.arcEnd = 360;
                const Cylinder = new GV.Circle(options);
                this.scene.addNode(Cylinder);
                break;

            case 'GV.Sector':
                options.height = 0;
                const Sector = new GV.Circle(options);
                this.scene.addNode(Sector);
                break;

            case 'GV.Semicylinder':
                const Semicylinder = new GV.Circle(options);
                this.scene.addNode(Semicylinder);
                break;

            case 'GV.Ellipse':
                options.height = 0;
                const Ellipse = new GV.Ellipse(options);
                this.scene.addNode(Ellipse);
                break;

            case 'GV.Cylindroid':
                const Cylindroid = new GV.Ellipse(options);
                this.scene.addNode(Cylindroid);
                break;

            case 'GV.Ellipsoid':
                const Ellipsoid = new GV.Ellipsoid(options);
                this.scene.addNode(Ellipsoid);
                break;

            case 'GV.Sphere':
                const Sphere = new GV.Sphere(options);
                this.scene.addNode(Sphere);
                break;

            case 'GV.Cone':
                const Cone = new GV.Cone(options);
                this.scene.addNode(Cone);
                break;
            
            default: break;
        }
    }

    remove() {
        super.remove();
        this.container.innerHTML = '';
        window.store['store-Mark'] = undefined;
        window.store['store-Prop'] = undefined;
    }

}

//# sourceURL=MarkPlugin.js
