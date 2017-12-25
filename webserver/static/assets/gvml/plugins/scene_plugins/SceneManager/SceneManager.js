/**
 * 项目：gvml
 * 文件：SceneManager.js
 * 作者：董波
 * 部门：产品研发中心
 * 邮箱：dongb@mail.ie.ac.cn
 * 日期：2017-03-08 13:22:28.
 * 用途：类
 */

class SceneManager extends GV.Widget {

    init() {
        // this.css('./.css');
        // this.html('./.html');
        console.log('sceneManager');
        this.scene = new GV.GraphicScene();
        this.earth.addScene(this.scene);
 //       this.parseScene('forbidden_city.model');
        this.parseScene('cbd.model');
        
    }

    parseScene(url) {
      const that = this;
      const promise = GV.Util.xmlPromise(url);
      promise.done((xml) => {
          that.addScene(GV.Util.xmlToJson(xml));
      });

      promise.fail((text) => {
          if (text.readyState === 4 && text.status === 200) {
              alert('scene文件解析失败，请检查是否拼写错误。');
              console.error('scene文件解析失败，请检查是否拼写错误。');
          } else {
              alert('scene文件读取失败，请检查路径是否错误。');
              console.error('scene文件读取失败，请检查路径是否错误。');
          }
      });

    }

    addScene(json) {
        
        let models = json.Models.model || json.Models.Model;
      
        if (!models) return;

        if(!models.length) {
            const tempModel = models;
            models = [];
            models.push(tempModel);
        }

        for ( let i = 0; i < models.length; i++ ) {
            const modeldata = models[i];
            const place = new GV.Place({position: {lat: modeldata.Local.lat, lon: modeldata.Local.lon},
            icon: 'airport.png'});
            const model = new GV.Model({
                position: {lat: modeldata.Local.lat, lon: modeldata.Local.lon, alt: modeldata.Local.hig},
                style: {
                    model: modeldata.Path,
                }
            }
          );
            this.scene.addNode(model);
            //this.scene.addNode(place);
        }

    }

    remove() {
        this.scene.clear();
    }

}

//# sourceURL=SceneManager.js 
