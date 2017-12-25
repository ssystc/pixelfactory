;(function ($, window, document, undefined) {

    //注册插件
    $.fn.GEOVISDituLayer = function (options) {
      
       if (!options.earth) {
            console.info('参数必须包含需操作的earth对象');
            return;
        }
      var layer_ditu =gvml.addImageLayer({
                 	name:'imagelayer',
                 	source:new GV.GeneralLayerSource({
                 		driver:'tms',
                 		title:'DEM',
                 		profile:'local',
                 		url:'http://192.168.4.236:19090/geowebcache/service/tms/1.0.0/MAP@EPSG%3A4326_MAP@png/',
                 		srs:'EPSG:4326',
                 	})
                 });
        return layer_ditu;
    }
})(jQuery, window, document);

