/**
 * 项目：gvml
 * 文件：CompassZoom.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-08 13:22:28.
 * 用途：类
 */

class Ocean extends GV.Widget {

  	init() {
		this.css('./Ocean.css');
		this.html('./Ocean.html');
	    this.registerName = 'GeoVIS::SkyAndCloudPlugin::OceanWidget';
	    const Windslider = document.getElementById('btn_scaleWind');
	    const Waveslider = document.getElementById('btn_scaleWave');
	    const WindValue = document.getElementById('windValue');
	    const WaveValue = document.getElementById('waveValue');
	    console.log('aa');
        const that = this;        
       
	    Windslider.oninput = () => {
	    	WindValue.value=parseInt(Windslider.value/8.3);
//	    	WaveValue.value=parseInt(Waveslider.value/33.3);
	      that.postMessage('wind', WindValue.value);
//	      that.postMessage('wave', WaveValue.value);
	    }; 
	    Waveslider.oninput = () => {
//	    	WindValue.value=parseInt(Windslider.value/8.3);
	    	WaveValue.value=parseInt(Waveslider.value/33.3);
//	      that.postMessage('wind', WindValue.value);
	      that.postMessage('wave', WaveValue.value);
	    };       	
	}
}

//# sourceURL=Ocean.js 
