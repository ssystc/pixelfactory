(function ($, window, document, undefined) {
    var SpatialAnalysis = function (ele, options) {
        var defaultOptions = {
            url: "http://127.0.0.1:8251/spatialanalysis/",
            slope: {
                legend: {
                    '#38a800': '< 30°',
                    '#5ebd00': '30°-45°',
                    '#8bd100': '45°-55°',
                    '#c1e800': '55°-65°',
                    '#ffff00': '65°-70°',
                    '#ffbf00': '70°-75°',
                    '#ff8000': '75°-80°',
                    '#ff4000': '80°-85°',
                    '#ff0000': '≥ 85°',
                }
            }
        };
        this.options = $.extend({}, defaultOptions, options);
        this.options['urls'] = {
            ts: this.options.url + 'ppv.json',
            section: this.options.url + 'section.json',
            slope: this.options.url + "slope.json",
            ts2: this.options.url + 'visibility2.json'
        };
        this.init();
    };
    SpatialAnalysis.prototype = {
        init: function () {
            this.initUI();
            this.initScene();
        }
        , initUI: function () {
            var parent = $(document.body);
            var height = parent.outerHeight();
            var left = parent.outerWidth();
            this.$element = $("<div style='position: absolute;'>").addClass("geovis-sp").appendTo(parent);
            this.$element.css({
                top: height - 480,
                left: left - 450
            });
            this.$element.draggable();
            this.$header = $("<div>").appendTo(this.$element);
            $("<div style='float: left;background-color: #23bbe8; width: 10px;height: 16px;margin-top: 11px'>").appendTo(this.$header);
            this.$title = $("<div style='float: left;margin: 0 10px'>").addClass("title").html("空间分析").appendTo(this.$header);
            this.$tabUl = $('<ul style="float: left">').addClass("nav nav-tabs").appendTo(this.$header);
            this.$tabContent = $('<div>').addClass('tab-content toggle_wrap').appendTo(this.$element);

            // 通视分析
            this.$ts = $(`<li><a class="ts" title="通视分析" href='#sp-ts' data-toggle="tab"></a></li>`).appendTo(this.$tabUl);
            this.$tsContent = $(`<div class="tab-pane" id="sp-ts">`).appendTo(this.$tabContent);
            var table = $("<table class='ts'>").appendTo(this.$tsContent);
            var tr = $("<tr>").appendTo(table);
            var td = $("<td width='100'>").appendTo(tr);
            $("<label>").text("可 见 区 域: ").appendTo(td);
            td = $("<td>").appendTo(tr);
            $("<div>").css({width: 50, height: 10, backgroundColor: "#0bc20b"}).appendTo(td);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("不可见区域: ").appendTo(td);
            td = $("<td>").appendTo(tr);
            $("<div>").css({width: 50, height: 10, backgroundColor: "#c00c0a"}).appendTo(td);


            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("观察点高度: ").appendTo(td);
            this.$tsStart = $("<td>").appendTo(tr);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("目标点高度: ").appendTo(td);
            this.$tsEnd = $("<td>").appendTo(tr);
            tr = $("<tr>").appendTo(table);
            this.$tsError = $("<td colspan='2'>").appendTo(tr);
            // 剖面分析
            this.$pm = $(`<li><a class="pm" title="剖面分析" href='#sp-pm' data-toggle="tab"></a></li>`).appendTo(this.$tabUl);
            this.$pmContent = $(`<div class="tab-pane" id="sp-pm">`).appendTo(this.$tabContent);
            this.$pmChart = $('<div style="width: 800px;height: 300px">').appendTo(this.$pmContent);


            // 缓冲区分析
            this.$buffer = $(`<li><a class="buffer" title="缓冲区分析" href='#sp-buffer' data-toggle="tab"></a></li>`).appendTo(this.$tabUl);
            this.$bufferContent = $(`<div class="tab-pane" id="sp-buffer">`).appendTo(this.$tabContent);

            // 路径分析
            this.$path = $(`<li><a class="path" title="路径分析" href='#sp-path' data-toggle="tab"></a></li>`).appendTo(this.$tabUl);
            this.$pathContent = $(`<div class="tab-pane" id="sp-path">`).appendTo(this.$tabContent);

            // 高度分析
            this.$height = $(`<li><a class="height" title="高度分析" href='#sp-height' data-toggle="tab"></a></li>`).appendTo(this.$tabUl);
            this.$heightContent = $(`<div class="tab-pane" id="sp-height">`).appendTo(this.$tabContent);

            // 坡度分析
            this.$slope = $(`<li><a class="slope" title="坡度分析" href='#sp-slope' data-toggle="tab"></a></li>`).appendTo(this.$tabUl);
            this.$slopeContent = $(`<div class="tab-pane" id="sp-slope">`).appendTo(this.$tabContent);
            //操作区域
            table = $("<table style='float: left'>").appendTo(this.$slopeContent);
            tr = $("<tr>").appendTo(table);
            td = $("<td colspan='2'>").appendTo(tr);

            var btnToolbar = $('<div class="btn-toolbar">').appendTo(td);
            $('<div class="btn-group rect">').click((e) => {
                this.drawSlopeRect();
            }).appendTo(btnToolbar);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("经度: ").appendTo(td);
            this.$slopeX = $("<td>").appendTo(tr);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("纬度: ").appendTo(td);
            this.$slopeY = $("<td>").appendTo(tr);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("高度: ").appendTo(td);
            this.$slopeZ = $("<td>").appendTo(tr);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("坡度: ").appendTo(td);
            this.$slopeS = $("<td>").appendTo(tr);

            tr = $("<tr>").appendTo(table);
            td = $("<td>").appendTo(tr);
            $("<label>").text("坡向: ").appendTo(td);
            this.$slopeA = $("<td>").appendTo(tr);

            table = $("<table>").appendTo($("<div class='slope-legend'>").appendTo(this.$slopeContent));

            tr = $("<tr>").appendTo(table);
            td = $("<td colspan='2'>").text("坡度分析图例").appendTo(tr);

            for (var color in this.options.slope.legend) {
                $(`<tr><td><span class="legend-img" style="background-color:${color} "></span></td><td class="legend-text">${this.options.slope.legend[color]}</td></tr>`).appendTo(table);
            }
            this.lastClickItem = null;
            this.$element.find('a[data-toggle="tab"]').on('shown.bs.tab', (e) => {
                this.lastClickItem = $(e.target);
                this.onTabShow(e.target);
            });
            this.$ts.find("a").tab('show');
        },
        showOrHide: function () {
            if (this.$element.css('display') == 'none') {
                this.$element.show();
                this.onTabShow(this.lastClickItem);
            } else {
                this.hide();
                this.scene.clear()

            }
        },
        hide: function () {
            this.offAllEvents();
            this.$element.hide();
        },
        onTabShow: function (tabElement) {
            tabElement = $(tabElement);
            this.offAllEvents();
            //通视分析
            if (tabElement.hasClass('ts')) {
                this.tsModle.count = 0;
                this.getEarth().on('mouseClick', this.onTSClick, this);
            } else if (tabElement.hasClass('pm')) {
                this.getEarth().on('mouseClick', this.onPMClick, this);
            } else if (tabElement.hasClass('slope')) {
                this.onSlopeMove();
            }
        },
        offAllEvents: function () {
            this.getEarth().off('mouseClick', this.onTSClick, this);
            this.getEarth().off('mouseClick', this.onPMClick, this);
            if(this.scene){
                this.scene.clear();
            }
            this.slopeData = [];
        },
        pmModle: {
            count: 0,
            start: null,
            end: null,
        },
        onPMClick: function (info) {
            if (info) {
                this.pmModle.count++;
                if (this.pmModle.count % 2 == 1) {
                    this.pmModle.start = info;
                } else {
                    this.pmModle.end = info;
                    this.showPM(this.pmModle.start, this.pmModle.end);
                }
            }
        },
        analysis: function (url, data, successFun) {
            $.getJSON(url, data, successFun).fail(() => {
                alert("服务异常,请检查");
            })
        },
        //剖面显示操作
        showPM: function (start, end) {
            var data = {
                "p1.x": start.x,
                "p1.y": start.y,
                "p2.x": end.x,
                "p2.y": end.y
            }
            this.analysis(this.options.urls.section, data, (res) => {
                if (res) {
                    if (res.isSuccess) {
                        var myChart = echarts.init(this.$pmChart[0]);
                        var color = '#23bbe8';
                        // 指定图表的配置项和数据
                        var option = {
                            title: {
                                text: `最高海拔: ${res.maxH}米 最低海拔: ${res.minH}米 剖线长度: ${res.data[res.data.length - 1][0]}千米`,
                                x: 'center',
                                textStyle: {
                                    color: color,
                                    fontSize: 12
                                }
                            },
                            tooltip: {
                                formatter: function (params) {
                                    return '距离: ' + params.data[0].toFixed(2) + '千米<br>海拔: ' + params.data[1].toFixed(2) + '米';
                                }
                            },
                            grid: {
                                containLabel: true,
                                show: true
                            },
                            xAxis: {
                                name: "距离: 千米",
                                axisLine: {
                                    lineStyle: {
                                        color: color
                                    }
                                },
                                interval: (res.data[res.data.length - 1][0] - res.data[0][0]) / 10,
                                axisLabel: {
                                    formatter: function (value) {
                                        return value.toFixed(0);
                                    }
                                }

                            },
                            yAxis: {
                                name: "海拔: 米",
                                axisLine: {
                                    lineStyle: {
                                        color: color
                                    }
                                }
                            },
                            series: [{
                                type: 'line',
                                smooth: true,
                                data: res.data,
                                lineStyle: {
                                    normal: {
                                        color: color
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        color: color
                                    }
                                }
                            }]
                        };

                        // 使用刚指定的配置项和数据显示图表。
                        myChart.setOption(option);
                    } else {
                        alert(res.msg);
                    }
                } else {
                    alert("服务异常");
                }
            })
        },
        slopeData: [],
        onSlopeMove: function () {
            this.getEarth().on('mousemove', (info) => {
                var data = null;
                //搜索需要的信息
                for (var i = this.slopeData.length - 1; i >= 0; i--) {
                    data = this.slopeData[i];
                    if (info.x >= data.min_x && info.x < data.max_x && info.y >= data.min_y && info.y <= data.max_y) {
                        break;
                    } else {
                        data = null;
                    }
                }
                if (data != null) {
                    var cell_x = (data.max_x - data.min_x) / data.cols,
                        cell_y = (data.max_y - data.min_y) / data.rows;
                    var dcol = Math.floor((info.x - data.min_x) / cell_x);
                    if (dcol >= data.cols) {
                        dcol = data.cols - 1;
                    }
                    var drow = Math.floor((info.y - data.min_y) / cell_y);
                    if (drow >= data.rows) {
                        drow = data.rows - 1;
                    }
                    //求出格网偏移位置
                    var off = drow * data.cols + dcol;
                    this.$slopeX.text(info.x.toFixed(2));
                    this.$slopeY.text(info.y.toFixed(2));
                    this.$slopeZ.text(data.data[drow][dcol].toFixed(2));
                    this.$slopeS.text(data.slope[off].toFixed(2));
                    this.$slopeA.text(this.formatAspet(data.aspet[off]));
                }
            });
        },
        formatAspet: function (value) {
            if (value < 22.5) {
                return "北";
            } else if (value < 67.5) {
                return "东北";
            } else if (value < 112.5) {
                return "东";
            } else if (value < 157.5) {
                return "东南";
            } else if (value < 202.5) {
                return "南";
            } else if (value < 247.5) {
                return "西南";
            } else if (value < 292.5) {
                return "西";
            } else if (value < 337.5) {
                return "西北";
            } else {
                return "北";
            }

        },
        drawSlopeRect: function () {
            this.drawRect((coordinates) => {
                if (coordinates && coordinates.length > 0) {
                    var last = coordinates[coordinates.length - 1],
                        first = coordinates[0];
                    var isClosed = true;//是否封闭
                    for (var i = 0; i < last.length; i++) {
                        if (last[i] != first[i]) {
                            isClosed = false;
                            break;
                        }
                    }
                    if (!isClosed) {
                        coordinates.push(coordinates[0]);
                    }
                    var data = {
                        geometry: JSON.stringify({type: "Polygon", coordinates: coordinates})
                    }
                    this.analysis(this.options.urls.slope, data, (res) => {
                        this.slopeData.push(res);
                        /* '#38a800': '< 30°',
                         '#5ebd00': '30°-45°',
                         '#8bd100': '45°-55°',
                         '#c1e800': '55°-65°',
                         '#ffff00': '65°-70°',
                         '#ffbf00': '70°-75°',
                         '#ff8000': '75°-80°',
                         '#ff4000': '80°-85°',
                         '#ff0000': '≥ 85°',,*/
                        var colors = res.slope.map(function (value) {
                            if (value < 30) {
                                return "#38a800";
                            } else if (value < 45) {
                                return "#5ebd00";
                            } else if (value < 55) {
                                return "#8bd100";
                            } else if (value < 65) {
                                return "#c1e800";
                            } else if (value < 70) {
                                return "#ffff00";
                            } else if (value < 75) {
                                return "#ffbf00";
                            } else if (value < 80) {
                                return "#ff8000";
                            } else if (value < 85) {
                                return "#ff4000";
                            } else {
                                return "#ff0000";
                            }
                        });
                        var fieldData = new GV.FieldData({
                            elecData: {
                                lon_min: res.min_x,
                                lat_min: res.min_y,
                                lon_max: res.max_x,
                                lat_max: res.max_y,
                                colors: colors,
                                rows: res.rows,
                                cols: res.cols
                            }
                        });
                        this.scene.addNode(fieldData);
                    })
                }


            })
        },
        drawRect: function (fun) {
            var mouseClick = (info) => {
                this.getEarth().off('mouseClick', mouseClick, this);
                var polygon = new GV.Polygon({
                    style: {
                        'stroke-width': 3,
                        'stroke': '#FF0000'
                    }
                });
                this.scene.addNode(polygon);
                var mousemove = (mousemove) => {
                    polygon.vertices = [[info.x, info.y], [info.x, mousemove.y], [mousemove.x, mousemove.y], [mousemove.x, info.y]];
                }
                var mouseEndClick = () => {
                    this.getEarth().off('mouseClick', mouseEndClick, this);
                    this.getEarth().off('mousemove', mousemove, this);
                    fun(polygon.vertices.getPoints());
                    this.scene.removeNode(polygon);
                };

                this.getEarth().on('mouseClick', mouseEndClick, this);
                this.getEarth().on('mousemove', mousemove, this);
            };
            this.getEarth().on('mouseClick', mouseClick, this);
        },
        tsModle: {
            count: 0,
            start: null,
            end: null,
        },
        onTSClick: function (info) {
            if (info) {
                this.tsModle.count++;
                if (this.tsModle.count % 2 == 1) {
                    this.tsModle.start = info;
                } else {
                    this.tsModle.end = info;
                    this.TSAnalysis(this.tsModle.start, this.tsModle.end);
                }
            }
        },
        scene: null,
        initScene: function () {
            this.scene = new GV.GraphicScene();
            this.getEarth().addScene(this.scene);
        },
        addLine: function (start, end, color) {
            var node = new GV.Polyline({
                vertices: [[start.x, start.y, start.z], [end.x, end.y, end.z]],
                style: {
                    'stroke-width': 3,
                    'stroke': color,
                    'altitude-clamping': 'terrain-drape',
                }
            });
            this.scene.addNode(node);
        },
        TSAnalysis: function (start, end) {
            var data = {
                "p1.x": start.x,
                "p1.y": start.y,
                "p2.x": end.x,
                "p2.y": end.y
            }
            this.analysis(this.options.urls.ts, data, (res) => {
                if (res) {
                    this.$tsError.text(res.msg);
                    if (res.isSuccess) {
                        start.z = res.startH;
                        end.z = res.endH;
                        this.$tsStart.text(start.z.toFixed(2) + "米");
                        this.$tsEnd.text(end.z.toFixed(2) + "米");
                        if (res.point) {
                            this.addLine(start, res.point, "#0bc20b");
                            this.addLine(res.point, end, "#c00c0a");
                        } else {
                            this.addLine(start, end, "#0bc20b");
                        }
                    }
                }
            })
           /* this.analysis(this.options.urls.ts2, {x: end.x, y: end.y, radius: 10}, (vres) => {
                var colors = vres.vm.map(function (item) {
                    return item == 1 ? "#00FF00" : "#FF0000";
                });
                var fieldData = new GV.FieldData({
                    elecData: {
                        lon_min: vres.gisExtent.xMin,
                        lat_min: vres.gisExtent.yMin,
                        lon_max: vres.gisExtent.xMax,
                        lat_max: vres.gisExtent.yMax,
                        colors: colors,
                        rows: vres.rows,
                        cols: vres.cols
                    }
                });
                this.scene.addNode(fieldData);
            })*/
        },
        getEarth: function () {
            return this.options.earth;
        }

    }
    $.fn.GEOVISSP = function (options) {
        var geovisSP = new SpatialAnalysis(this, options);
        return geovisSP;
    }
})(jQuery, window, document);
