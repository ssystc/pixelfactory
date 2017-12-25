;(function ($, window, document, undefined) {

    //注册插件
    $.fn.GEOVISYingxiangLayer = function (options) {
       //alert('yingxiang')
       if (!options.earth) {
            console.info('参数必须包含需操作的earth对象');
            return;
        }
      
       
       var layer_yingxiang =options.earth.addImageLayer({
                 	name:'imagelayer',
                 	source:new GV.GeneralLayerSource({
                 		driver:'tms',
                 		title:'DEM',
                 		profile:'local',
                 		url:'http://192.168.4.236:19090/geowebcache/service/tms/1.0.0/IMG@EPSG%3A4326_IMG@jpeg/',
                 		srs:'EPSG:4326',
                 	})
                 });
        return layer_yingxiang
    }
})(jQuery, window, document);

