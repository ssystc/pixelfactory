function createchars(msg,dataUrl){
		document.body.removeChild(document.getElementById('main'));
		document.body.removeChild(document.getElementById('closeBtn'));
	var ecahrs = document.createElement('div');
	document.body.appendChild(ecahrs);
	ecahrs.setAttribute('id','main');
	ecahrs.style.width = "800px";
	ecahrs.style.height = "500px";
//	ecahrs.style.border = "1px solid red";
	ecahrs.style.position = "absolute";
	ecahrs.style.zIndex = "999";
	ecahrs.style.top = "40px";
	ecahrs.style.right = "0px";
//	ecahrs.style.background = "rgba(0,0,0,0.9)";
	//关闭按钮
	var BTN = document.createElement('div');
			ecahrs.style.display = "block";
		BTN.style.display = "block";
	BTN.setAttribute('id','closeBtn');
	BTN.style.width = "50px";
	BTN.style.height = "30px";
	BTN.style.position = "absolute";
	BTN.style.top = "50px";
	BTN.style.right = "0px";	
	BTN.style.zIndex = "9999999";
//	BTN.style.background = "rgba(0,0,0,1)";	
	BTN.style.color = "white";	
	BTN.innerHTML = "关闭";
	document.body.appendChild(BTN);
	BTN.onclick = function(){
		ecahrs.style.display = "none";
		BTN.style.display = "none";
	}
	var pointstr = msg;
	var pointarr = pointstr.split(";");
	 GAjax({
	 	type : 'get',
	 	url : dataUrl,
	 	data : {startTime:'2016-09',endTime:"2017-01",points:""+pointarr[0]+"@"+pointarr[1]+","+pointarr[0]+"@"+pointarr[3]+","+pointarr[2]+"@"+pointarr[3]+","+pointarr[2]+"@"+pointarr[1]+""},
	 	dataType: "json",
	 	async : true,
	 	success : function(resonse){
	 		var jsonData = JSON.parse(resonse);
	 		console.log(jsonData);
	 		echarslist(jsonData);
	 	},
	 	fail : function(status){
	 		alert("服务器报错状态码为"+status)
	 	}
	 });
		 
	function echarslist(jsonData){						
		// 基于准备好的dom，初始化echarts实例
	    var myChart = echarts.init(document.getElementById('main')); 
			
		var dataMap = {};

		var bmmbArr = [];
		var kzmbArr = [];
		var smmbArr = [];
		var sxmbArr = [];
		var bumingArr = [];
		var woArr = [];
		var youArr = [];
		var diArr = [];
		
		console.log(jsonData)
		for(var i=0;i<jsonData.length;i++){
			bmmbArr.push(jsonData[i].bmmb);
			kzmbArr.push(jsonData[i].kzmb);
			smmbArr.push(jsonData[i].smmb);
			sxmbArr.push(jsonData[i].sxmb);
			bumingArr.push(jsonData[i].buming);
			woArr.push(jsonData[i].wo);
			youArr.push(jsonData[i].you);
			diArr.push(jsonData[i].di);
		}
		//柱状图
		var arr1 = {
			bmmb : bmmbArr,
			kzmb : kzmbArr,
			smmb : smmbArr,
			sxmb : sxmbArr
		}
		//折线图
		var arr2 = {
			buming : bumingArr,
			wo : woArr,
			you : youArr,
			di : diArr
		}	
		var option = {
		    baseOption: {
		    	
		        timeline: {
		            // y: 0,
		            axisType: 'category',
		            // realtime: false,
		             show : false,
		            autoPlay: true,
		            // currentIndex: 2,
		            playInterval: 1000,
		            // controlStyle: {
		            //     position: 'left'
		            // },
		        
		            
		        },
		        title: {
		            subtext: ''
		        },
		        tooltip: {},
		        legend: {
		        	
		            x: 'center',
		            data: [{
		                name:'不明目标',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            }, {
		                name:'空中目标',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            }, {
		                name:'水面目标',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            },{
		                name:'水下目标',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            }, {
		                name:'不明',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            }, {
		                name:'我方',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            }, {
		                name:'友方',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            } ,{
		                name:'敌方',
		                textStyle:{
		                    fontSize:12,
		                    fontWeight:'bolder',
		                    color:'#999'
		                },		               
		            }],
		          
		  
		        },
		        calculable : true,
		        grid: {
		            top: 80,
		            bottom: 60
		        },
		        xAxis: [
		            {
		                'type':'category',
		                'axisLabel':{'interval':0},
		                'data':[		                    
		                    '2016-09','2016-10','2016-11','2016-12'
		                ],
		                splitLine: {show: false},
		                axisPointer: {
		                	type: 'shadow'                
		                },
		                axisLine : {
		                	lineStyle : {
		                		color : "#999"
		                	}
		                }
		            }
		        ],
		        yAxis: [
		            {
		                type: 'value',
		                name: '数据量（幅）',
		                // max: 53500
		                
		              //  max: 500000
		                axisLine : {
		                	lineStyle : {
		                		color : "#999"
		                	}
		                }
		            },
		             {
		                type: 'value',
		                name: '数据总量（幅）',
		                // max: 53500
		                
		              //  max: 500000
		            }
		            
		        ],
		        series: [
		          
		            {name: '不明目标', type: 'bar'},
		            {name: '空中目标', type: 'bar'},
		            {name: '水面目标', type: 'bar'},
		            {name: '水下目标', type: 'bar'},
		//          {
		//          	 tooltip : {
		//      trigger: 'item',
		//      formatter: "({d}%)"
		//  },
		//              name: '各个节点数据量占比',
		//              type: 'pie',
		//              center: ['21%', '20%'],
		//              radius: '28%'
		//          },
		             {name: '不明', type: 'line'},
		            {name: '我方', type: 'line'},
		            {name: '友方', type: 'line'},
		            {name: '敌方', type: 'line'}
		        ]
		    },
		    options: [
		        {
		            title: {
		            	text: '态势分析表',
		            	textStyle:{
		            		color:"white"
		            	}
		            	},
		            tooltip: {
		        		trigger: 'axis',
		        		axisPointer: {
		            		type: 'cross',
		            		crossStyle: {
		                		color: '#ffffff'
		            		}
		        		}
		    		},
		    series: [
		               
		                {data: arr1.bmmb},
		                {data: arr1.kzmb},
		                {data: arr1.smmb},
		                {data: arr1.sxmb},
		//              {data: [
		//                  {name: '北京', value: dataMap.dataPIS['2006sum']},
		//                  {name: '苏州', value: dataMap.dataSIS['2006sum']},
		//                  {name: '无锡', value: dataMap.dataTIS['2006sum']}
		//              ]},
		                {data: arr2.buming,yAxisIndex: 1,},
		                {data: arr2.wo,yAxisIndex: 1,},
		                {data: arr2.you,yAxisIndex: 1,},
		                {data: arr2.di,yAxisIndex: 1,}
		            ]
		        }
		    ]
		};
		// 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);  
	}	
	
}
