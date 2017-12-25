## PixelFactory 接口说明

### 算法模块
#### 1.获取算法列表

> GET /api/module

* 返回值：
```json
[
    {
        "id": "OC-0.0.1",
        "name": "正射校正",
        "icon": "",
        "desc": "",
        "owner": "",
        "createDate": "",
        "type": "",
        "runMethod": "auto",
        "manual": false,
        "redirect": "",
        "ModuleClass": ""
    },
    {
        "id": "OC-0.0.1",
        "name": "正射校正",
        "icon": "",
        "desc": "",
        "owner": "",
        "createDate": "",
        "type": "",
        "runMethod": "auto",
        "manual": false,
        "redirect": "",
        "ModuleClass": ""
    },
    ...
]
```

#### 2.获取算法模块的详细信息

> GET /api/module/\<id\>

* 参数：id
* 返回值：
```json
{
    "id": "OC-0.0.1",
    "name": "正射校正",
    "op": "OC",
    "version": "0.0.1",
    "tmp": "tmp",
    "dirs": ["原始影像", "rpc文件"],
    "icon": "",
    "desc": "",
    "owner": "",
    "createDate": "",
    "type": "",
    "runMethod": "auto",
    "manual": false,
    "redirect": "",
    "ModuleClass": "llts",
    "Userproperty": {
        "InputParameter": {
            "InputFilePath": [
                { "name": "InputImgFileName", "title": "输入影像", "type": "string", "value": "../path" },
                { "name": "InputRPCFileName", "title": "RPC文件", "type": "string", "value": "../path" }
            ],
            "ReferenceImage": [
                { "name": "DEMFileName", "title": "参考高程", "type": "string", "value": 0.9 }
            ],
            "Configuration": [
                { "name": "PixelSpacing", "title": "分辨率", "type": "float", "value": 1.0 },
                { "name": "GridSize", "title": "格网大小", "type": "int", "value": 3 }
            ]
        },
        "OutputParameter": {
            "OutPutFilePath": [
                { "name": "OutputRPCFileName", "title": "输出文件", "type": "float", "value": 0.9 }
            ],
            "DataAttribute": [
                { "name": "DataFormat", "title": "影像格式", "type": "float", "value": 0.9 },
                { "name": "ImageTime", "title": "生产时间", "type": "float", "value": 0.9 },
                { "name": "MapProjection", "title": "投影类型", "type": "float", "value": 0.9 },
                { "name": "EarthModel", "title": "参考椭球", "type": "float", "value": 0.9 },
                { "name": "PixelSpacing", "title": "分辨率", "type": "float", "value": 0.9 },
                { "name": "SatelliteID", "title": "卫星标识", "type": "float", "value": 0.9 }
            ],
            "ProgramStatus": [
                { "name": "ReturnCode", "title": "运行转态", "type": "float", "value": 0.9 },
                { "name": "ReturnAnalyse", "title": "错误描述", "type": "float", "value": 0.9 }
            ],
            "tempfile": [
                { "name": "e-name", "title": "z-name", "type": "float", "value": 0.9 }
            ]
        }
    },
    "Systemproperty": {
        "DataTypes": [
            { "name": "DataType", "title": "数据类型", "type": "string", "value": "局部影像" }
        ],
        "SystemConfiguration": [
            { "name": "ThreadNum", "title": "线程个数", "type": "int", "value": 4 },
            { "name": "BlockSize", "title": "分块大小", "type": "int", "value": 2048 }
        ],
        "Freeze": [
            { "name": "FreezeExecute", "title": "冻结执行", "type": "string", "value": "" }
        ]
    }
}
```


### 流程模块
#### 1.流程列表
> GET /api/flow  
> GET /api/flow/query/\<key\>
* 返回值:
```json
[
    {
        "id": "xxx",
        "name": "",
        "icon": "",
        "desc": "",
        "owner": "",
        "createDate": "",
        "type": "",
        "runMethod": "auto",
        "version": "0.0.1",
        "key": ""
    },
    {
        "id": "xxx",
        "name": "xxx",
        "icon": "",
        "desc": "",
        "owner": "",
        "createDate": "",
        "type": "",
        "runMethod": "auto",
        "version": "0.0.1",
        "key": ""
    },
    ...
]
```

#### 2.流程详细信息
> GET /api/flow/\<id\>
* 参数：id
* 返回值：
```json
{
    "id": "xxx",
    "name": "xxx",
    "icon": "",
    "desc": "",
    "owner": "",
    "createDate": "",
    "type": "",
    "runMethod": "auto",
    "ModuleClass": "llts",
    "workflow": [       // 流程中的模块间的关系
        {
            "flow_id": "flow_1",
            "pre_id": "",
            "next_id": "flow_2"
        }
        {
            "flow_id": "flow_2",
            "pre_id": "flow_1",
            "next_id": ""
        }
        ...
    ],
    "modules": [        // 流程中用到的模块及模块的详细信息列表
        {
            "flow_id": "flow_1",
            ...
        },
        {
            "flow_id": "flow_2",
            ...
        }
    ],
    "IOMap": [          // 流程间输入输出关系列表
        {
            "output": {
                "id": "flow_1",
                "name": "xxx"
            },
            "input": {
                "id": "flow_1",
                "name": "xxxx"
            }
        },
        {
            
        }
    ]
}
```

#### 3.保存流程接口
> POST /api/flow
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|可选字段,如果有该字段，表示修改指定的流程|
|content|xxxxx|必选，流程详细信息的json|
|uidata|xxxxxx|可选字段|

* 返回值：
```json
{
    "code": 0,
    "id": ""
}
```

#### 4.删除流程接口
> DELETE /api/flow
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|流程id|

* 返回值：
```json
{
    "code": 0
}
```


### 任务模块
#### 1.任务列表
> GET /api/task     获取所有任务  
> GET /api/task?flowId=**   获取和指定流程相关的任务
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|flowId|xxxxxxx|流程id，可选参数用于获取和某个流程相关的任务，如果没有该参数，则表示获取所有的任务|

* 返回值：
```json
[
    {
        "id": "***",
        "name": "***",
        "desc": "",
        "owner": "",
        "createDate": "",
        "flowId": "",
        "beginTime":"",
        "estimatedTime":"",
        "icon":""
    },
    ...
]
```

#### 2.任务详细信息
> GET /api/task/\<id\>
* 参数：id
* 返回值：
```json
{
    "id": "***",
    "name": "***",
    "desc": "",
    "owner": "",
    "createDate": "",
    "flowId": "",
    "dir": "",
    "dirclassify": "",
    "icon":"",
    "args": [   // 任务输入参数列表
        {"name": "", "title": "", "type": "", "value": "", "index": 0, "multi": "true"},
        {"name": "", "title": "", "type": "", "value": "", "index": 0, "multi": "true"}
    ]
}
```
* 说明
如果有多组输入，则index依次加1，应确保每组输入的index的值是相等的

#### 3.添加编辑任务
> POST /api/task
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|可选字段,如果有该字段，表示修改指定的任务|
|content|xxxxx|必选，任务详细信息的json，该json种可以没有id|

* 返回值：
```json
{
    "code": 0,  // 添加成功，返回0
    "id": ""    // 任务id
}
```

#### 4.删除任务
> DELETE /api/task
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|任务id|

* 返回值：
```json
{
    "code": 0
}
```

#### 5.执行任务
> POST /api/task/start
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|任务id|

* 返回值：
```json
{
    "code": 0
}
```

#### 6.暂停任务
> POST /api/task/pause
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|任务id|

* 返回值：
```json
{
    "code": 0
}
```

#### 7.继续任务
> POST /api/task/contine
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|任务id|

* 返回值：
```json
{
    "code": 0
}
```

#### 8.停止任务
> POST /api/task/stop
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|id   |xxxxxxx|任务id|

* 返回值：
```json
{
    "code": 0
}
```

#### 9.获取任务状态
> GET /api/task/state/\<id\>
* 参数：任务id
* 返回值： 
```json
{
    "id": "taskid",
    "state": 0/1/2,
    "errorCode": 0,
    "errorMessage": "",
    "detail": {
        "flow_id": {
            "code": 0/1/2,      // 模块运行状态
            "exitCode": 0,      // 算法代码的运行状态，正常为0，程序崩溃返回非0
            "returnCode": 0,    // 算法的返回值，0为正常，非0表示执行错误
            "returnMsg": "",    // 错误原因
            "detail": "",       // 详情id
            "fsid": "",         // 输出文件系统目录id
            ...                 // 其他字段
        },
        "flow_id2": {
            "code": 0,
            ...
        }
    }
}
```
* 说明：

| 返回值 | desc |
|:---:|:----|
|0   |等待，还未执行|
|1  |正在运行|
|2  |已完成|

### 文件系统
#### 1.创建任务目录
> POST /api/fs/dir/prepare  
* 参数  

| key | value | desc |
|:---|:-----:|:----|
|flowId|xxxxxxx|任务关联的流程|
|dir| xxxxxx| 任务的数据根目录id|
|classify|xxxxxx|可选参数（默认我的资源）|

* 返回值
```json
{
    "code": 0
}
```

#### 2.获取任务目录列表
> GET /api/fs/list/\<id\>
* 参数 taskid
* 返回值
```json
{
    "code": 0,
    "type": "dir",
    "path": "任务名",
    "url": "",
    "childs": [
        {
            "type":"dir",
            "path":"input",
            "url": "",
            "childs": [
                
            ]
        },
        {
            "type":"file",
            "path":"xxx.tiff",
            "url": ""
        }
    ]
}
```

### 登陆接口
#### 1、登陆
> GET /user/login?redirect=***
* 参数 redirect 可选参数
* 返回值 如果有redirect，则登陆后跳转到redirect指向的页面，没有则跳转到默认的页面


### 其他接口
#### 1.保存流程ui信息
> POST /api/flow/ui/data
* 参数：

| key | value | desc |
|:---|:-----:|:----|
|flowId|xxxxxxx|流程id|
|content| xxxxxx|要保存的信息|

* 返回值:
```json
{
    "code": 0
}
```


#### 2.获取流程ui信息
> GET /api/flow/ui/data/\<id>\
* 参数：流程id
* 返回值：保存的ui信息或空字符串



## 算法流程输入输出规则
1. 输入输出应当指定为文件，不能使用文件夹(出图分幅模块除外)
2. 对于有多个相同类型输入的模块，在模块定义文件中指定一个即可，并将mulit字段设置为true，不写将默认为false，如ImageMatch-batch，在模块定义的json中的输入文件的写法如下：
```json
{
    "InputFilePath": [
        {
            "name": "InputPANFileName",
            "title": "输入影像",
            "type": "file",
            "value": "",
            "mulit": true
        }
    ]
}
```
假如指定了5景影像，在算法执行的时候，将得到如下的输入：
```json
{
    "InputFilePath": [
        {
            "name": "InputPANFileName",
            "title": "输入影像",
            "type": "file",
            "value": "**/pan/GF2_****/GF2_***.tiff",
            "index": 0,
            "mulit": true
        },
        {
            "name": "InputPANFileName",
            "title": "输入影像",
            "type": "file",
            "value": "**/pan/GF2_****/GF2_***.tiff",
            "index": 1,
            "mulit": true
        },
        {
            "name": "InputPANFileName",
            "title": "输入影像",
            "type": "file",
            "value": "**/pan/GF2_****/GF2_***.tiff",
            "index": 2,
            "mulit": true
        },
        {
            "name": "InputPANFileName",
            "title": "输入影像",
            "type": "file",
            "value": "**/pan/GF2_****/GF2_***.tiff",
            "index": 3,
            "mulit": true
        },
        {
            "name": "InputPANFileName",
            "title": "输入影像",
            "type": "file",
            "value": "**/pan/GF2_****/GF2_***.tiff",
            "index": 4,
            "mulit": true
        }
    ]
}
```
3. 对于有多个输出的，和上面的类似，但是需要算法将输出结果按照上面的格式分开写到json中，需要注意index的值，比如BundleAdj模块，在json里面是这样的定义的：
```json
{
    "OutPutFilePath": [
        {
            "multi": true,
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "",
            "suffix": "_BundleAdj.rpc"
        }
    ]
}
```
传递给算法的如下所示：
```json
{
    "OutPutFilePath": [
        {
            "multi": "true",
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "***/output/BundleAdj/***_BundleAjd.rpc",
            "suffix": "_BundleAdj.rpc"
        }
    ]
}
```
假如算法有5个输出，需要按照如下格式写json文件：
```json
{
    "OutPutFilePath": [
        {
            "multi": "true",
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "***/output/BundleAdj/***_BundleAjd.0.rpc",
            "suffix": "_BundleAdj.rpc",
            "index": 0
        },
        {
            "multi": "true",
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "***/output/BundleAdj/***_BundleAjd.1.rpc",
            "suffix": "_BundleAdj.rpc",
            "index": 1
        },
        {
            "multi": "true",
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "***/output/BundleAdj/***_BundleAjd.2.rpc",
            "suffix": "_BundleAdj.rpc",
            "index": 2
        },
        {
            "multi": "true",
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "***/output/BundleAdj/***_BundleAjd.3.rpc",
            "suffix": "_BundleAdj.rpc",
            "index": 3
        },
        {
            "multi": "true",
            "name": "OutputRPC",
            "title": "RPC输出目录",
            "type": "string",
            "value": "***/output/BundleAdj/***_BundleAjd.4.rpc",
            "suffix": "_BundleAdj.rpc",
            "index": 4
        }
    ]
}
```
输出的index应当能与前面的ImageMatch的输入的index对应上

4. 多景到单景的算法，流程会提供并行化的处理方式，算法不需要处理。需要注意的是，流程在处理并行的时候会将原来的模块的flowid替换成flowid-index的形式，比如输入有5景影像，流程中有模块的flowid为match，那么流程在执行时，模块的flowid会变成match-0,match-1,match-2,match-3,match-4


## 错误码说明
| value | desc |
|:-----:|:----|
|0|正常|
|-1|请求中没有content|
|-2|请求中没有找到flowId|
|-3|请求中没有找到taskId|
|-4|未找到指定id的workflow|
|-5|未找到指定id的task|
|-6|请求中未找到dir|
|-7|workflow的content中未找到modules字段|
|-8|目录不存在|
|-9|llts操作失败|
|-10|出现异常|
|-11|未知的操作|
|-100|向workflow中重复添加模块|
|-110|没有起始module|
|-111|没有结束module|
|-200|连接模块出错|
|-300|任务没有在运行|
|-301|任务已经在运行了，无需重复提交|
|-310|没有找到任务|
|-400|列出目录失败|
|-401|下载文件失败|
|-402|获取netimgurl失败|
|-403|在webos上创建目录失败|
|-404|在webos上创建文件失败|
|-405|上传tiff文件失败|
|-406|上传文件失败|
|-407|llts调用出错|
|-500|json文件加载问题|