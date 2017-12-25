// ;(function($,window){
// 	var jishu = 1;
// 	$.fn.GEOVISTMySpace = function(){
// 		if(jishu % 2 == 0){
// 			$('.rightPanel').animate({
// 				'right':'-400px'
// 			},700);
// 		}else{
// 			$('.rightPanel').animate({
// 				'right':'0px'
// 			},700);			
// 		}
// 		jishu++;
// 	}

// })(jQuery,window)

;
(function($, window, document, undefined) {
    var RightItem = function(ele, options) {
    var rightright = {
    		rightItem: {
		        element: '.rightPanel',
		        img: {
		            img1: 'images/订阅h.png',
		            img2: 'images/收藏1.png',
		            img3: 'images/历史1.png',
		            img4: 'images/消息h.png'
		        },

		        saveImgUrl: 'E:/gv520170525/GV5_Explorer/work_dir/h5Framwork/images/',
		        showArea: {
		             Area1: {
		                name: '我的订阅',
		                index: 0,
		                img: 'images/订阅h.png',
		                sources: {
		                     cssurl: 'libs/plugins/os-mySubscribe/os-mySubscribe.css',
		                     jsurl: 'libs/plugins/os-mySubscribe/os-mySubscribe.js',
		                }
		            },
		            Area2: {
		                name: '我的收藏',
		                index: 1,
		                img: 'images/收藏1.png',
		                sources: {
		                    cssurl: 'libs/plugins/os-myCollect/os-myCollect.css',
		                    jsurl: 'libs/plugins/os-myCollect/os-myCollect.js',
		                }
		            },
		            Area3: {
		                name: '我的历史',
		                index: 2,
		                img: 'images/历史1.png',
		                sources: {
		                    cssurl: 'libs/plugins/os-myHistory/os-myHistory.css',
		                    jsurl: 'libs/plugins/os-myHistory/os-myHistory.js',
		                }
		            },
		            Area4: {
		                name: '我的信息',
		                index: 3,
		                img: 'images/消息h.png',
		                sources: {
		                    cssurl: 'libs/plugins/os-myMessage/os-myMessage.css',
		                    jsurl: 'libs/plugins/os-myMessage/os-myMessage.js',
		                }
		            }
		        }
		    };
		};
        this.$element = ele;
        this.img1 = rightItem.rightItem.img.img1;
        this.img2 = rightItem.rightItem.img.img2;
        this.img3 = rightItem.rightItem.img.img3;
        this.img4 = rightItem.rightItem.img.img4;
        this.options = $.extend(options);
        this.init();
    };
    RightItem.prototype = {
            init: function() {
                var that = this;
                $('<div>').addClass('g-myspaceR fr').appendTo(that.$element);
                $('.g-myspaceR').data('earth', that.options.earth);
                $('.g-myspaceR').data('imgUrl', that.options.saveImgUrl);
                $('.rightPanel').css('height', ($(window).height() - 100) + 'px'); //设置高度
                $('.g-myspaceR').css('height', ($(window).height() - 100) + 'px'); //设置高度
                $('<ul><li class="g-subscribe"><img src="' + that.img1 + '"></li><li class="g-collection"><img src="' + that.img2 + '"></li><li class="g-history"><img src="' + that.img3 + '"></li><li class="g-message"><img src="' + that.img4 + '"></li></ul>').appendTo($('.g-myspaceR'));
                //加载初始设置的sources(js)(css)
                that._addCssJs(that.options.showArea.Area1.sources.jsurl, that.options.showArea.Area1.sources.cssurl);
                that._addCssJs(that.options.showArea.Area2.sources.jsurl, that.options.showArea.Area2.sources.cssurl);
                that._addCssJs(that.options.showArea.Area3.sources.jsurl, that.options.showArea.Area3.sources.cssurl);
                that._addCssJs(that.options.showArea.Area4.sources.jsurl, that.options.showArea.Area4.sources.cssurl);
                //初始化判断 我的订阅 中index索引是否存在
                that._toggleIndex(that.options.showArea.Area1.index);
                that._toggleIndex(that.options.showArea.Area2.index);
                that._toggleIndex(that.options.showArea.Area3.index);
                that._toggleIndex(that.options.showArea.Area4.index);

            },
            _addCssJs: function(jsurl, cssurl) {
                if (jsurl) {
                    $.getScript(jsurl, function() {
                        if (cssurl) {
                            $('<link>').attr({
                                rel: 'stylesheet',
                                href: cssurl
                            }).appendTo('head');
                        }
                    });
                }
            },
            _toggleIndex: function(index) {
                if (index || index == 0) {
                    $('.g-myspaceR ul li:first-child').css('background', 'rgb(87, 87, 87)');
                    $('.g-myspaceR ul li').eq(index).click(function() {
                        $('.g-myspaceR ul li').css('background', '#2b2b2c');
                        $(this).css('background', 'rgb(87, 87, 87)');
                        $('.os-myspaceitem').css('display', 'none');
                        $('.os-myspaceitem').eq(index).css('display', 'block');

                        $.fn.GEOVISMySpaceWinClose();

                    });
                } else {
                    alert(index)
                }
            }
        }
        //注册插件
    $.fn.GEOVISTRItem = function(options) {
        var rightItem = new RightItem(this, options);
        return rightItem;
    }
})(jQuery, window, document);
