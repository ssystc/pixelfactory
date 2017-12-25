
	        // 使用刚指定的配置项和数据显示图表。
//	        myChart.setOption(option);

class LayChartTool extends GV.Tool {

  init() {
  	this.getJSonTool = this.earth.getMapTool('GetJSonTool').select();
  	this.css('./LayChartTool.css');
  	this.script('./echarts-all.js');
    this.html('./LayChartTool.html');
 
	console.log("...");
	this.getJSonTool.on('sendJSon', this.onJSonData.bind(this));
  }
  
   remove() {
    this.earth.clearMapTool();
  }
  
  
  onJSonData(msg){
  	    console.log(msg); 
 // 	var msgJson = JSON.parse(msg);
  	var getCoords = function(coordinates) {
        var coords = {longitude:[], latitude:[], height:[],xCoords:[]};
     //   var xCoord = {coord:[0.1,0.2]};
        for(var i in coordinates) {
        	var xCoord = {coord:[]};
            coords.longitude.push(coordinates[i][0]);
      //      coords.latitude.push(_aAcoordinates[i][1]);
            coords.height.push(coordinates[i][2]);
            xCoord.coord.push(coordinates[i][0]);
            xCoord.coord.push(coordinates[i][1]);
            coords.xCoords.push(xCoord.coord);
        }
        return coords;
    };
	const coords = getCoords(msg.coordinates);
	console.log("......");
	
	this.echart(coords);
  }
  
  echart(data) {
  	const myChart = echarts.init(document.getElementById('main'));
  	var maxHeight,minHeight;
  //	var xFirst=JSON.stringify(data.xCoords[0]);
  //	var xNext=JSON.stringify(data.xCoords[150]);
  //	var xNext=JSON.stringify(data.xCoords[300]);
  	for(var i in data.height) {
  		maxHeight=minHeight=data.height[0];
  		if(minHeight>data.height[i]) {
  			minHeight=data.height[i];
  		};
  	    if(maxHeight<data.height[i]) {
  			maxHeight=data.height[i];
  		} 		 		
  	}
  	

    
	// 指定图表的配置项和数据
	const option = {
		
		
			    tooltip: {
			        trigger: 'axis'
			    },
			    toolbox: {
			        show: true,
			        feature: {
			            dataZoom: {
			                yAxisIndex: 'none'
			            },
			            dataView: {readOnly: false},
			            magicType: {type: ['line', 'bar']},
			            restore: {},
			            saveAsImage: {}
			        }
			    },
			    //背景颜色rgba(a,s,x,0.3)前三位决定颜色，最后一位决定透明度范围0-1,逗号隔开
			    backgroundColor:"rgba(200,200,100,0.3)",
			    xAxis:  {
			       type: 'category',
			        //横坐标名称和样式
			        name:"经，纬",
			     //   min:data.longitude[0],
			     //   max:data.longitude[300],
			        nameTextStyle:{
			        	color:"rgba(150,150,0,0.8)"
			        },
			        //x轴刻度对应文字样式
			        axisLabel:{
			        	textStyle:{
			        		color:"rgba(200,100,0,0.8)"
			        	}
			        },
			        boundaryGap: false,
			        //横坐标
			        data: data.xCoords
			    },
			    yAxis: {
			  type: 'value',
			         //纵坐标名称和样式
			        name:"高 ",
			        min:minHeight,
			        max:maxHeight,
			        nameTextStyle:{
			        	color:"rgba(150,150,0,0.8)"
			        },
			        axisLabel: {
			            formatter: '{value} M',
			            textStyle:{
			        		color:"rgba(200,100,0,0.8)"
			        	}
			        }
			    },
			    series: [
			        {
			        	name: '高',
			            type:'line',
			             lineStyle: {
                normal: {
                    opacity: 0
                }
            },
            stack: 'confidence-band',
            symbol: 'none',
			            data:data.height,
			            markPoint: {
			                data: [
			                    {type: 'max', name: '最大值'},
			                    {type: 'min', name: '最小值'}
			                ]
			            },
			            markLine: {
			                data: [
			                    {type: 'average', name: '平均值'}
			                ]
			            },
			            textStyle:{
			            	color:"red"
			            },
			            markLine: {
			                data: [
			                    {type: 'average', name: '平均值'}
			                ]
			            }
			        }
			    ]
			};

			myChart.setOption(option);
	
  }

}

//# sourceURL=LayChartTool.js 
