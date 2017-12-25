var geovis_tag_container = document.getElementsByClassName('geovis_tag_container')[0]
var geovis_tag_title_cancel = document.getElementsByClassName('geovis_tag_title_cancel')[0]
var geovis_tag_content_func_span = document.getElementsByClassName('geovis_tag_content_func_span')

//点击变色
var Num = geovis_tag_content_func_span.length
for(var i =0;i<Num; i++){
    geovis_tag_content_func_span[i].onclick = function () {
        if( this.style.background == 'rgb(36, 121, 148)'){
            this.style.background = '#AA671E';
        }else if( this.style.background == 'rgb(170, 103, 30)'){
           this.style.background = 'rgb(36, 121, 148)'
        }
    }
}

//点击关闭
geovis_tag_title_cancel.onclick = function() {
    console.log(geovis_tag_container)
    geovis_tag_container.style.display = 'none'
}