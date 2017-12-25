/**
 * 项目：gvml
 * 文件：CompassZoom.js
 * 作者：钱晶
 * 部门：产品研发中心
 * 邮箱：jqian@mail.ie.ac.cn
 * 日期：2017-03-08 13:22:28.
 * 用途：类
 */

class Skyandcloud extends GV.Widget {

  	init() {
  		//alert('sky')
		//this.css('./Skyandcloud.css');
		//this.html('./Skyandcloud.html');
	    this.registerName = 'GeoVIS::SkyAndCloudPlugin::SkyAndCloudWidget';	
	    this.sky = this.earth.getMapWidget('SkyAndCloud').open();
//	    const slider = document.getElementById('btn_scaleSkyAndCloud');
//	    const sliderSnow = document.getElementById('btn_snow');
//	    const switcher =document.getElementsByClassName("setting-control")[0];
//	    console.log('aa');
//      const that = this;        
//     
//	    slider.oninput = () => {
//	      this.sky.postMessage('time', slider.value.toString());
//	    }; 
//	    sliderSnow.oninput = () => {
//	      this.sky.postMessage('isSnow', sliderSnow.value.toString());
//	    }; 
//		switcher.onclick =function() {
//			if(this.childNodes[1].style.left == "0px"){
//				this.childNodes[1].style.left = "25px";
//				this.nextSibling.nextSibling.innerHTML = "开";
//				this.setAttribute('data', 'true');
//			}else{
//				this.childNodes[1].style.left = "0px";
//				this.nextSibling.nextSibling.innerHTML = "关";
//				this.setAttribute('data', 'false');
//			}
//			that.sky.postMessage('isLight', this.getAttribute('data'));   
//		}
    

	}
  	    remove() {
        this.sky.close();
    }
}

//# sourceURL=Skyandcloud.js 
