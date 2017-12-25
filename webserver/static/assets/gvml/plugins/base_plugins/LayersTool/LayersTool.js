/**
 * 项目：gvml
 * 文件：LayersTool.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-05 19:37:20.
 * 用途：类
 */
// const GV = window.GV;
let LayersTool;
{
    const GV = window.GV;
    LayersTool = (
        class Layers extends GV.Tool {

            get alias() {
                return '图层管理工具';
            }

            init() {
                console.debug(this.container.id);
                const layers = this.earth.getLayers();
                this.initDOM(layers);
            }

            initDOM(initLayers) {
                const inits = [];
                initLayers.layers.forEach((value) => {
                    inits.push({
                        id: value.name ? value.name : `image_${Math.floor(Math.random() * 10000)}`,
                        name: '未命名图层',
                        type: value.constructor.name === 'ImageLayer' ? 'image' : 'undefined',
                    });
                });
                if (!this.dom) {
                    this.layerToolDom = new GV.LayerManagerView({
                        container: this.container.id,
                        url: GV.Util.formatURL('./layers.json', this.url),
                        layers: {
                            images: inits,
                            baseImage: { id: initLayers.baseLayer.id, name: '基础图层', type: 'base_image' },
                        },
                        onAddClick: (item) => {
                        // undefined 说明取消添加基础图层，不做操作，还是原来的，暂且不做变白球的操作
                            if (item === undefined) {
                                console.log('您取消了基础图层');
                                return;
                            }
                            switch (item.type) {
                                case 'base_image': this.updateBaseImage(item); break;
                                case 'image': this.addImage(item); break;
                                case 'elevation': this.addElevation(item); break;
                                default: break;
                            }
                        },
                        onSort: (id, from, to) => { console.log(id, from, to); },
                        onDeleteClick: (id) => { this.removeLayer(id); },
                    });
                    this.layerToolDom.render();
                    this.dom = true;
                }
            }

            addImage(item) {
                let source;
                if (item.type === 'image') {
                    switch (item.source.driver) {
                        case 'tms':
                            source = new GV.TileMapServiceSource({
                                url: item.source.url,
                                format: item.source.format,
                            });
                            break;
                        case 'gdal':
                            source = new GV.GdalLayerSource({
                                url: item.source.url,
                                extensitions: 'tif',
                            });
                            break;
                        case 'xyz':
                            source = new GV.XYZLayerSource({
                                url: item.source.url,
                            });
                            break;
                        case 'grst':
                            source = new GV.GeneralLayerSource({
                                driver: 'grst',
                                url: item.source.url,
                            });
                            break;
                        default: break;
                    }
                    this.earth.addImageLayer({
                        name: item.id,
                        source,
                    });
                }
                // console.log(layer.name, layer.driver);
            }

            addElevation(item) {
                let source;
                if (item.type === 'elevation') {
                    switch (item.source.driver) {
                        case 'gdal':
                            source = new GV.GdalLayerSource({
                                url: item.source.url,
                                extensitions: 'tif',
                            });
                            break;
                        case 'tms':
                            source = new GV.TileMapServiceSource({
                                url: item.source.url,
                                format: item.source.format,
                            });
                            break;
                        default: break;
                    }
                    this.earth.addTerrainLayer({
                        name: item.id,
                        source,
                    });
                }
            }

            removeLayer(id) {
                const layerset = this.earth.getLayers();
                // console.log(layerset);
                layerset.layers.forEach((value) => {
                    if (value.name === id) {
                        console.log(this, value.name, id);
                        this.earth.removeLayer(value);
                    }
                });
            }

            updateBaseImage(item) {
                let source;
                const sources = [];
                for (const index in item.source) {
                    if (item.source[index]) {
                        switch (item.source[index].driver) {
                            case 'tms':
                                source = new GV.TileMapServiceSource({
                                    url: item.source[index].url,
                                    format: item.source[index].format,
                                });
                                sources.push(source);
                                break;
                            case 'gdal':
                                source = new GV.GdalLayerSource({
                                    url: item.source[index].url,
                                });
                                sources.push(source);
                                break;
                            case 'xyz':
                                source = new GV.XYZLayerSource({
                                    url: item.source[index].url,
                                });
                                sources.push(source);
                                break;
                            default: break;
                        }
                    }
                }
                const base = this.earth.getBaseLayer();
                if (base) {
                    base.name = item.name;
                    base.updateDataSource(sources);
                }
            }

            remove() {
                console.log('remove: ', this.dom);
                this.removeUI();
                this.dom = false;
            }
        }
    );
}


//# sourceURL=LayersTool.js 
