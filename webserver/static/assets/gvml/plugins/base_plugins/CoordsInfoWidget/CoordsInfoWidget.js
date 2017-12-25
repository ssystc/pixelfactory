/**
 * 项目：gvml
 * 文件：CoordsInfoWidget.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-06 16:11:36.
 * 用途：经纬度信息工具
 */

let CoordsInfoWidget;
{
    const GV = window.GV;
    // const aaa = '123';
    CoordsInfoWidget = (
        class CoordsInfo extends GV.Widget {

            get alias() {
                return '经纬度信息';
            }

            init() {
                this.css('./CoordsInfo.css');
                this.html('./CoordsInfo.html');
                this.infobar = this.earth.getMapWidget('InfoBar').open();
                this.infobar.on('locationChange', this.updateInfo.bind(this));
                //  infobar.changeCamera('123213213');
                // infobar.postMessage('change',);

                // if (this._lon === undefined) {
                //     this._lon = 0;
                //     this._lat = 0;
                //     this._space = '';
                // }
                this._space = '';
                const that = this;
                // this._finding = false;
                // setInterval(() => {
                //     if (that._find === true || that._finding === false) {
                //         that._finding = true;
                //         setTimeout(() => {
                //             $.ajax({
                //                 type : 'get',
                //                 //url : `http://192.168.4.223:9001/api/v1/query/location?lon=${parseInt(this._lon)}&lat=${parseInt(this._lat)}`,
                //                 url : `http://192.168.16.1:9001/api/v1/query/location?lon=${parseInt(that._cameraLon)}&lat=${parseInt(this._cameraLat)}`,
                //                 dataType: "json",
                //                 async : true,
                //                 success : function(resonse) {
                //                     if(resonse && resonse.DMMC) {
                //                         that._space = resonse.DMMC;
                //                     }
                //                 },
                //                 fail : function(status){
                //                     console.log("服务器报错状态码为"+status);
                //                 }	
                //             })
                //             that._finding = false;
                //         }, 100);
                //         this._find = false;
                //     }
                // }, 10);
                
                // setInterval(() => {
                //     if (!that._find) return;
                //     that._find = false;
                //     $.ajax({
                //         type : 'get',
                //         //url : `http://192.168.4.223:9001/api/v1/query/location?lon=${parseInt(this._lon)}&lat=${parseInt(this._lat)}`,
                //         url : `http://192.168.16.1:9001/api/v1/query/location?lon=${parseInt(that._cameraLon)}&lat=${parseInt(this._cameraLat)}`,
                //         dataType: "json",
                //         async : true,
                //         success : function(resonse) {
                //             if(resonse && resonse.DMMC) {
                //                 that._space = resonse.DMMC;
                //             } else {
                //                 that._space = '';
                //             }
                //         },
                //         fail : function(status){
                //             console.log("服务器报错状态码为"+status);
                //         }	
                //     })
                // }, 1000);
            }

            parseNum(num) {
                num = Math.abs(num);
                let tmp;
                const d = parseInt(num);
                tmp = (num - d) * 60;
                const f = parseInt(tmp);
                tmp = (tmp - f) * 60;
                const m = parseInt(tmp);
                return `${d}° ${f}′ ${m}″`
            }

            // getSpace(lon, lat) {

            //     if (this._lon === undefined) {
            //         this._lon = 0;
            //         this._lat = 0;
            //         this._space = '';
            //     }
            //     if (Math.abs(this._lon - lon) < 10 && Math.abs(this._lat - lat) < 10) {
            //         return this._space;
            //     }
                
            //     const that = this;
            //     this._lon = lon;
            //     this._lat = lat;
            //     $.ajax({
            //         type : 'get',
            //         url : `http://192.168.4.223:9001/api/v1/query/location?lon=${parseInt(lon)}&lat=${parseInt(lat)}`,
            //         dataType: "json",
            //         async : true,
            //         success : function(resonse) {
            //             if(resonse && resonse.DMMC) {
            //                 that._space = resonse.DMMC;
            //             }
            //         },
            //         fail : function(status){
            //             console.log("服务器报错状态码为"+status);
            //         }	
            //     })
            //     return this._space;
            // }

            updateInfo(infoArray) {
                if (!(infoArray instanceof Array) || infoArray.length < 4) { return; }

                const vp = this.earth.camera.viewpoint;
                if (this._cameraLat === undefined) {
                    this._cameraLat = 0;
                    this._cameraLon = 0;
                }

                if (Math.abs(this._cameraLat - vp.lat) > 5 || Math.abs(this._cameraLon - vp.lat) > 5) {
                    this._cameraLon = vp.lon;
                    this._cameraLat = vp.lat;
                    this._find = true;
                }

                const scale = this.earth.camera.scale;
                GV.$('#scale').html(`比例尺:${parseInt(scale)}m`);

                const lon = infoArray[0];
                if (lon < 0) {
                    GV.$('#longtitude').html(`W:${this.parseNum(lon)}`);
                } else {
                    GV.$('#longtitude').html(`E:${this.parseNum(lon)}`);
                }

                const lat = infoArray[1];
                if (lat < 0) {
                    GV.$('#latitude').html(`S:${this.parseNum(lat)}`);
                } else {
                    GV.$('#latitude').html(`N:${this.parseNum(lat)}`);
                }
            
                let height = infoArray[2];
                height = height < 0 ? height.toPrecision(6) : height.toPrecision(6);
                GV.$('#height').html(`焦点高度:${height}m`);

                let eye = infoArray[3] / 1000;
                eye = eye < 0 ? eye.toPrecision(6) : eye.toPrecision(6);
                GV.$('#eye').html(`视高:${eye}km`);

                this._lat = lat;
                this._lon = lon;
                GV.$('#space').html(`地区:${this._space}`);
            }

            remove() {
                this.infobar.close();
            }

        }
    );
}

//# sourceURL=CoordsInfoWidget.js 
