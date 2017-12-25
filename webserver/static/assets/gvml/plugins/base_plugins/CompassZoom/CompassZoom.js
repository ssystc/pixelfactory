/**
 * 项目：gvml
 * 文件：CompassZoom.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-08 13:22:28.
 * 用途：类
 */
let CompassZoom;
{
    const $ = window.$;
    const GV = window.GV;
    CompassZoom = class Compass extends GV.Widget {

        fun(angle) {
            return angle / 180 * 3.1415926;
        }

        init() {
            this.css('./zoom.css');
            this.html('./zoom.html');

            const slider = document.getElementById('btn_scale');

            const camera = this.earth.camera; // 得到相机对象

            camera.onCameraChange((cameraChange) => { //监听相机的左右偏转角。heading为相机的左右偏转角度单位是弧度角
                let heading = cameraChange.viewpoint.heading;
                heading = -heading;
                window.$('.ck-ratation').css({
                    transform: `rotate(${heading}deg)`,
                });
            });

            $('.wan-back , .wans-back').css({
                background: `url(${GV.Util.formatURL('./image/wan.png', this.url)})`
            });
            $('#home > img').attr('src', GV.Util.formatURL('./image/ageage.png', this.url));
            $('#mapViewHome > img').attr('src', GV.Util.formatURL('./image/sstop.png', this.url));
            $('#home').click(() => {
                camera.flyToHome(2);   // 相机回复到home位置
            });

            $('#rotateUp > img').attr('src', GV.Util.formatURL('./image/tttt.png', this.url));
            $('#rotateUp').click(() => {
                camera.rotate(0, this.fun(10));
                $('.wan-back').css({
                    transform: 'rotate(0deg)',
                    top: '-1px',
                    left: '3px'        
                });       
            });

            $('#rotateDown > img').attr('src', GV.Util.formatURL('./image/bbbb.png', this.url));
            $('#rotateDown').click(() => {
                camera.rotate(0, -this.fun(10));
                $('.wan-back').css({
                    transform: 'rotate(180deg)',
                    top: '47px',
                    left: '8px'        
                });         
            });

            $('#rotateLeft > img').attr('src', GV.Util.formatURL('./image/llll.png', this.url));
            $('#rotateLeft').click(() => {
                camera.rotate(-this.fun(10), 0);
                $('.wan-back').css({
                    transform: 'rotate(270deg)',
                    top: '25px',
                    left: '-19px'        
                });        
            });

            $('#rotateRight > img').attr('src', GV.Util.formatURL('./image/rrrr.png', this.url));
            $('#rotateRight').click(() => {
                camera.rotate(this.fun(10), 0);//相机旋转：第一个参数为左右偏转，第二个参数为俯仰。单位是弧度角范围是（-3.14到3.14）
                $('.wan-back').css({
                    transform: 'rotate(90deg)',
                    top: '21px',
                    left: '30px'        
                });        
            });

            $('#mapviewUp > img').attr('src', GV.Util.formatURL('./image/tttt.png', this.url));
            $('#mapviewUp').click(() => {
                camera.pan(0, -this.fun(10));
                $('.wans-back').css({
                    transform: 'rotate(0deg)',
                    top: '-1px',
                    left: '3px'        
                });      
            });

            $('#mapviewDown > img').attr('src', GV.Util.formatURL('./image/bbbb.png', this.url));
            $('#mapviewDown').click(() => {
                camera.pan(0, this.fun(10));
                $('.wans-back').css({
                    transform: 'rotate(180deg)',
                    top: '47px',
                    left: '8px'        
                });       
            });

            $('#mapviewLeft > img').attr('src', GV.Util.formatURL('./image/llll.png', this.url));
            $('#mapviewLeft').click(() => {
                camera.pan(this.fun(10), 0);
                $('.wans-back').css({
                    transform: 'rotate(270deg)',
                    top: '25px',
                    left: '-19px'        
                });        
            });

            $('#mapviewRight > img').attr('src', GV.Util.formatURL('./image/rrrr.png', this.url));
            $('#mapviewRight').click(() => {
                // 平移球体：第一个参数为左右平移，第二个参数为前后平移。单位是弧度角（精度和纬度范围是-3.14到3.14，一般设置为0.2）
                camera.pan(-this.fun(10), 0);
                $('.wans-back').css({
                    transform: 'rotate(90deg)',
                    top: '21px',
                    left: '30px'        
                });       
            });
            
            slider.oninput = () => {
                camera.setViewpoint({range: slider.value * 704919}); // 设置高度数值为相机与球体的距离单位是米
            };

        // camera.zoom(value);//缩放相机运算规则：最新距离 = (1 + value) * 当前距离（所以参数为-1到1之间）
        }

    };
}

//# sourceURL=CompassZoom.js 
