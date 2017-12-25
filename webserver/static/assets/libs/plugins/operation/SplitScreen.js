;(function ($, window, document, undefined) {
  var SplitScreen = function (ele, options) {
    /* console.log(options);
     if (!options.earth) {
     console.info('地球初始化未完成');
     return;
     }*/
    //����Ĭ�ϲ���
    this.default = {
      type: 'H',//'H'ˮ水平,'V'-垂直
      linkage: true //�Ƿ�����
    };
    this.options = $.extend({}, this.default, options);
    this.$earthElement = this.options.earth.container;
    this.init();
  }
  SplitScreen.prototype = {
    init: function () {
      this.initUI();
    }
    , toggleUI: function () {
      const isHidden = this.$otherEarthElement.css('visibility') == 'hidden';
      this.$otherEarthElement.css('visibility', isHidden ? 'visible' : 'hidden');
      this.$earthElement.parent().css('display', isHidden ? 'grid' : 'block');
    }
    , initUI: function () {
      const isH = this.options.type === 'H';
      const parentStyle = {
        display: 'grid',
        height: '100%',
        'gridAutoFlow': isH ? 'column' : 'row'
      }
      if (isH) {
        parentStyle['gridAutoColumns'] = '50%';
      } else {
        parentStyle['gridAutoRows'] = '50%';
      }
      this.$earthElement.parent().css(parentStyle);
      this.$otherEarthElement = $('<div>').appendTo(this.$earthElement.parent());
      this.initOtherEarth();
    }
    , lastView: {}
    //��������
    , earthReady: function (selfEarth) {
      //ͬ���ӽ�
      if (this.options.linkage) {
        var _this = this;
        var toOtherLinkFun = function (ev) {
          if (ev.viewpoint != _this.lastView) {
            _this.lastView = ev.viewpoint;
            selfEarth.camera.setViewpoint(ev.viewpoint);
          }
        }
        this.options.earth.camera.onCameraChange(toOtherLinkFun);
      }
      var imageLayerJson = GV.Util.xmlToJson(GV.Util.strToXml(this.options.earth.getBaseLayer().toXml()));
      if (imageLayerJson.baseimage.image) {
        var sources = imageLayerJson.baseimage.image.map(function (v) {
          return new GV.GeneralLayerSource(v);
        });
        selfEarth.getBaseLayer().updateDataSource(sources);
      }
    }
    //初始化另外的球
    , initOtherEarth: function () {
      try {
        this.$otherEarth = new GV.GeoCanvas(this.$otherEarthElement, {
          map: {
            current_mode: '2D'
          }
        });
        this.$otherEarth.onReady((gvml) => {
          this.earthReady(gvml);
        });
      }catch (e){
        console.log('创建球失败!');
      }
    }
  }
  //ע����
  $.fn.GEOVISSplitScreen = function (options) {
    var splitScreen = new SplitScreen(this, options);
    return splitScreen;
  }
})(jQuery, window, document);

