$('<div>').addClass('os-mydingyue os-myspaceitem').appendTo($(".rightPanel"));
$('.os-mydingyue').css({
  background: 'rgba(15,15,15,0.9)',
  color: 'white'
});
$(".os-mydingyue").html('<div class="g-subscribeTitle">我的订阅</div><div class="g-subscribeContent"><div class="g-newSubscribe">新增订阅</div><ul class="g-subscribeList"></ul></div><div class="g-secondContent"></div>')
var innerContent = '';
for (var i = 1; i < 16; i++) {
  innerContent += '<li style="display: grid; grid-template-columns: 80px auto"><img src="assets/image/31.png"><div style="display: grid;grid-template-columns: auto auto"><p class="g-liTitle fl">南海局势' + i + '</p><p class="g-changeCon fr"><span>2016-12-11</span><img title="取消关注" src="assets/image/gcancel.png" /><img title="删除" src="assets/image/gdelect.png" /></p><p class="fl" style="grid-column-start: 1;grid-column-end: 3;">南海局势总体良好</p></div></li>'
}
$(".g-subscribeList").append(innerContent);
//我的订阅鼠标移入移出事件
$('body').on('mouseover', '.g-subscribeList li', function () {
  $(this).css('background', '#393939');
  $(this).find('.g-changeCon span').html('');
  $(this).find('.g-changeCon img').css('display', 'block');
})
$('body').on('mouseout', '.g-subscribeList li', function () {
  $(this).css('background', 'none')
  $(this).find('.g-changeCon span').html('2016-12-11');
  $(this).find('.g-changeCon img').css('display', 'none');
});
//我的订阅鼠标点击事件
var gScrollTop = 0; //滚动条状态
var gNowState = 0; //当前被点击的是第几条
$('.os-mydingyue li').click(function () {
  gScrollTop = $('.g-subscribeContent').scrollTop();
  gNowState = $(this).index();
  $(".g-secondContent").html('<div class="g-goprev"><img src="assets/image/goprev.png"><span>' + $(this).find('.g-liTitle').text() + '</span></div><div class="g-secondul"></div>');
  var gSecondUl = '';
  var gTimeUl = '';
  for (var i = 0; i < 2; i++) {
    for (var j = 0; j < 2; j++) {
      gTimeUl += '<li style="display: grid; grid-template-columns: 80px auto"><img src="assets/image/31.png"><div style="display: grid;grid-template-columns: auto auto"><p class="g-liTitle fl">南海局势' + j + '</p><p class="g-senChangeCon fr"><span>2016-12-11</span></p><p class="g-senImg"><img title="收藏" src="assets/image/gcollection.png" /><img title="分享" src="assets/image/gshare.png" /></p><img class="g-nowImg" title="删除" src="assets/image/gdelect.png" /></div></li>';
    }
    gSecondUl += '<ul><li class="g-timeUl">2016-12-13</li>' + gTimeUl + '</ul>';
    gTimeUl = '';
    // $(".g-timeUl").after(gTimeUl);
  }
  $(".g-secondul").append(gSecondUl);
  $(".g-subscribeContent").css('display', 'none');
  $(".g-secondContent").css('display', 'block');
  //我的订阅第二级内容鼠标移入移出事件
  $('body').on('mouseover', '.g-secondContent li', function () {
    $(this).css('background', '#393939');
    $(this).find('.g-nowImg').css('display', 'block');
  })
  $('body').on('mouseout', '.g-secondContent li', function () {
    $(this).css({'background': 'none'});
    $(this).find('.g-nowImg').css('display', 'none');
  });
  //第二级内容删除功能
  $('.os-mydingyue li').on('click', '.g-nowImg', function () {
    $(this).parent().parent().remove();
  });
});
//返回上一级
$('body').on('click', '.g-goprev', function () {
  $(".g-subscribeContent").css('display', 'block');
  $(".g-secondContent").css('display', 'none');
  $('.g-subscribeContent').scrollTop(gScrollTop);
  $('.os-mydingyue li').css('background', 'none');
  $('.os-mydingyue li').eq(gNowState).css('background', '#393939');
});
//取消关注功能
$('.os-mydingyue li').on('click', '.g-changeCon img:nth-child(2)', function (event) {
  event.stopPropagation();
  alert("将此条从数据库中删除");

});
//删除功能
$('.os-mydingyue li').on('click', '.g-changeCon img:last-child', function (event) {
  $(this).parent().parent().parent().remove();
  event.stopPropagation();
});

//新增订阅功能部分
$('.g-newSubscribe').click(function () {
  $("#g-addSubscribe").css('display', 'block');

});
$('.g-cancalSubscribe').click(function () {
  $("#g-addSubscribe").css('display', 'none')
});
$('.g-saveSubscribe').click(function () {
  alert("a")
  var val1 = $(".g-Subscribeval1").val();
  var val2 = $(".g-Subscribeval2").val();
  var val3 = '';
  $(".g-newTable tr:nth-child(3) td input").each(function (index, domEle) {
    if ($(domEle).prop('checked')) {
      val3 += $(domEle).next('span').text();
    }
  });
  var val4;
  $(".g-newTable tr:nth-child(4) td span").each(function (index, domEle) {
    if ($(domEle).is('.g-newstyle')) {
      val4 = $(domEle).text()
    }
  });
  var val5 = $(".g-Subscribeval5").val();
  if (val1.length == 0 || val2.length == 0 || val3.length == 0 || val4 == undefined || val5.length == 0) {
    $(".g-dangerSubscribe").css('display', 'block');
  } else {
    $(".g-dangerSubscribe").css('display', 'none');
    alert(val1 + "--" + val2 + "--" + val3 + "--" + val4 + "--" + val5);
  }
});
$(".g-newTable tr:nth-child(4) td span").click(function () {
  $(".g-newTable tr:nth-child(4) td span").removeClass("g-newstyle");
  $(this).addClass("g-newstyle");
})
$(".g-newTable tr:last-child input").click(function () {
  $(".g-source").slideToggle();
})
$(".g-source p").on('click', function () {
  $(this).next('ul').slideToggle();
  if ($(this).find('img').attr('src') == 'assets/image/gb.png') {
    $(this).find('img').attr('src', 'assets/image/gr.png');
  } else {
    $(this).find('img').attr('src', 'assets/image/gb.png');
  }
})
$(".g-source ul li").on('click', function () {
  $(".g-newTable tr:last-child input").val($(this).text());
  $(".g-source ul li").css("color", "#c0c0c0");
  $(this).css("color", "#2499e4");
});
