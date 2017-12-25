;(function ($, window, document, undefined) {

    //注册插件
    $.fn.GEOVISShiliangLayer = function (options) {
      // alert('shiliang')
       if (!options.earth) {
            console.info('参数必须包含需操作的earth对象');
            return;
        }
       gvml.addVectorLayer({
				                name:'modelLayer',
				                layout: {
				                    level: [
				                        {name: 'far', style: 'large', min_range:1e7, max_range:1e10},
				                    ]
				                },
				                styles: {
			                        'large': {
			                        'stroke':                       '#888888',
			                        'stroke-width':                 '2px',
			                        'altitude-clamping':            'terrain-drape',
			                        }
			                	},
				                source: new GV.GeneralModelSource({
				                    driver: 'ogr',
				                    url: './shp/world/world.shp'
				                })
				            });
				            	layer1 = gvml.addVectorLayer({
				                name:'modelLayer',
				                 layout: {
				                    level: [
				                        {name: 'near', style: 'small', min_range:10000, max_range:3e7}
				                    ]
				                },
				                styles: {
				                    'small': {
				                        'stroke':            '#666666',
				                        'stroke-width':      '2px',
				                        'altitude-clamping':  'terrain-drape',
				                    }
				                },
				                source: new GV.GeneralModelSource({
				                    driver: 'ogr',
				                    url: './shp/china/shengjiel.shp'
				                })
				            });

    }
})(jQuery, window, document);

