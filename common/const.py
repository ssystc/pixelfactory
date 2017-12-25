# coding: utf-8


class ErrorCode(object):
    NoError = 0
    NoContentInReq = -1               # 请求中未找到content
    NoFlowIdInReq = -2               # 请求中没有找到flowId
    NoTaskIdInReq = -3               # 请求中没有找到taskId
    NotFindFlowById = -4                # 未找到指定id的workflow
    NotFindTaskById = -5        # 未找到指定id的task
    NoDirInReq = -6             # 请求中未找到dir
    NoModulesInFlow = -7        # workflow的content中未找到modules字段
    DirNotExist = -8             # 目录不存在
    LLTSError = -9              # llts操作失败
    ExceptionError = -10        # 出现异常
    UnknowOption = -11             # 未知的操作
    NotFindTaskStateById = -12    #未能找到指定id的taskstate
    NotFindUiDataByFlowId = -13  #未能查到指定flowid的uidata
    NotFindTaskByFlowId = -14    #未能查到指定flowid的task
    NotFindStateClanByTask = -15   #未能根据taskid查到对应的stateclan
    StartRestModuleError = -16     #启动RestModule出错
    AddDuplicationTaskName = -17    #同一流程中添加重名的任务
    CannotDeleteMutualFlow = -18    #非拥有者无法删除共有流程
    # workflow 相关
    DuplicateModule = -100              # 向workflow中重复添加模块
    NoStartModule = -110          # 没有起始module
    NoEndModule = -111            # 没有结束module
    ConnectModuleError = -200           # 连接模块出错
    # 任务相关
    TaskNotInRuning = -300          # 任务没有在运行
    TaskAlreadyInRuning = -301      # 任务已经在运行了，无需重复提交
    TaskStartNoUser = -302          # 任务因为没有用户，无法启动
    TaskNotFind = -310              # 没有找到任务
    # 相关服务
    ListDirError = -400             # 列出目录失败
    DownloadFaild = -401            # 下载文件失败
    GetNetimgUrlFaild = -402        # 获取netimgurl失败
    CreateDirOnWebosFaild = -403    # 在webos上创建目录失败
    CreateFileOnWebosFaild = -404   # 在webos上创建文件失败
    RenameDirOnWebosFaild = -405    # 重命名目录失败
    UploadTiffFileFaild = -406      # 上传tiff文件失败
    UploadFileFaild = -407          # 上传文件失败
    LLTSCallError = -408            # 调用llts出错
    FindTiffDataError = -409        # 查询tiff影像信息错误
    # 文件错误
    LoadJsonError = -500            # 读取json文件出错
    PrepareInputsError = -501       # 准备输入文件出错
    PrepareOutputsError = -502      # 准备输出文件出错
    WriteModuleJsonError = -503     # 写入module json文件失败
    # 登陆
    LoginError = -600               # 登录失败
    NotUserLogin = -601             # 用户未登陆
    NotFindUser = -602              # 查询不到用户（根据session中的uid）

    

class TaskMessageField(object):
    Type = '__TYPE__'
    Id = '__ID__'
    Content = '__CONTENT__'
    ErrCode = '__CODE__'
    UserUid = '__USER_UID__'

class TaskRequestType(object):
    StartTask = '__START_TASK__'
    StopTask = '__STOP_TASK__'
    PauseTask = '__PAUSE_TASK__'
    ContinueTask = '__CONTINUE_TASK__'
    UnKnown = '__UNKNOWN__'

