'''
### AIV平台Bot自动化程序管理模块
* 此模块的 run()函数,在用户的Bot模块中被调用,必须是最先运行的代码 (不一定是顺序排前面,
    相反,run应该写__main__里(在api开头的函数声明后面);
* 本模块是 AivAgent 端的核心。负责初始化用户开发的Bot自动化程序模块,并管理bot的api函数列表、参数等
* Aiv的Bot模块接口为api开头命名函数,以此开头的函数将自动注册为bot的api函数,在客户端可以直接被调用;
    如果api函数比较多,也可以分模块写,然后使用import导入;
* run()启动前,最好把Bot所在的路径添加到Path中,然后import入loguru(AIV Bot必备模块),否则容易报 
    import错误,找不到依赖包,然后初始化日志工具等,最后再调用run()函数;
* 根据AIV平台注册的Bot 接口,匹配api开头的函数,并把参数拼接和格式化,最后成功调用Bot的api函数;
* 每个Bot api 函数,都有三个阶段被AIV AGI调用,分别是 cmd='init'(Bot被初始化调用)、cmd='param'
    (初始化后获取参数)、cmd='run'(前端用户调用)三个阶段;
* 用户的Bot程序,由AIV AGI服务程序直接调用,而AIV AGI与AIV客户端(app/web)相连接,
* 关于调试: 找到安装目录下: aivc/bin/debug.bat,直接运行即可(运行前要把AIV AGI服务程序关闭);
* AIV AGI 服务程序管理地址: http://127.0.0.1:28067/
* 常用的工具函数,统一放在 aivtool.py 模块中(比如生成文件md5码的函数)
    (2023.12)
'''
import sys,os,time

aivBot = None
aivBotMmap = None

## 1、初始化Aiv Bot 的第一个函数=======================================================================
def run(botId=None,callFun=None,logLevel = 'INFO', option = None) -> None:
    '''
        ### 注册AIV平台的Bot
        - param
            - botId:   Aiv平台分配的bot唯一的token
            - callfun:  程序初始化后,回调的函数
            - logLevel: 可选 'DEBUG','INFO','SUCCESS','WARNING','ERROR','CRITICAL' 
            - option: 当前Bot的参数(如: reload,timeout, ...)
        - desc
        * 此函数,必须是在用户Bot中执行的第一行代码(__main__中,但应该在bot api函数<以api开头>声明之后)
        * 当前模块下,所有以 api 开头的函数,都自动注册为aiv系统的bot接口函数
            其它不用作为bot api函数输出的函数,可以用"_"开头,或用其它命名开头
        * 在bot api函数内,可以调用 regParser() 注册bot api函数调用的参数,包含默认值、数据类型、可选值等等
        ### 本函数必须在模块的 "__main__" 后面调用,并且不能包裹在函数里面调用！
    '''
    try:
        import inspect
        # inspect.stack() 返回函数的调用栈
        frame = inspect.stack()
        if frame[1][3] != '<module>':
            raise Exception('run() 函数必须在用户的bot模块"__main__"下调用,且不能包裹在函数中调用')
        
        obj = inspect.getmembers(frame[1][0]) #  
        #数据是[(,) , (,) , (,) , (,)] 这样的
        globalvar = None 
        for tup in obj:
            if tup[0]=='f_globals': #字段'f_globals'记录的值 ,等同于函数 globals() 返回的值, 但globals()必须在自己的模块下运行,灵活性不足
                globalvar = tup[1]
                break

        from .aivapp import _aivAppInit #初始化全局路径、环境变量、logger
        _aivAppInit(globalvar['__file__'],False,loglevel=logLevel)
        
        import asyncio
        from loguru import logger
        import cv2 #对于用到opencv-python包,在用nuitka编译,如果在main.exe代码中不显式import cv2
        # 会导至以下错误：
        # ImportError: DLL load failed while importing cv2: 找不到指定的模块。

        os.environ['PYTHONUNBUFFERED'] = '1' #禁用标准输出的缓冲区 2023.10
        # 当使用Python调用FFmpeg时，如果输出信息太多，可能会导致标准输出（stdout）
        # 缓冲区溢出并引发错误。这通常是因为输出信息超过了缓冲区的容量。
        # 标准输出的默认缓冲区大小通常是8192字节,通过设置环境变量PYTHONUNBUFFERED为1来禁用缓冲区

        # 设置日志保存的文件路径,每一个子进程都要设置一次(loguru) 2024.2
        botPath = os.path.dirname(os.path.abspath(globalvar['__file__'])) #Bot程序路径
        from .aivtool import setLogFile  
        #设置日志保存的文件路径和级别,默认把WARNING级别的日志保存在执行程序目录的botError.log文件中(但不影响控制台输出的日志) 2024.2 
        logFile = os.path.join(botPath,'botError.log') #在bot模块根目录下生成一个日志文件 2024.3
        setLogFile(logFile, logLevel= 'INFO')  #默认只显示 INFO信息(只影响写入本地文件的日志等级,不影响控制台输入日志的等级)
        

        global aivBot
        aivBot = AivBot()
        aivBot.botInfo.path = botPath
        # aivBot.botInfo.botName = botName
        aivBot.botInfo.botId = botId
        aivBot.botOption = option # 当前Bot的配置内容
        # logger.warning('Bot的Option是: {}'.format(aivBot.botOption))

        aivBot.regBotApi(globalvar)

        from .aivmmap import AivBotMmap
        global aivBotMmap
        # print('AivBot收到的 taskMMAPName333 ==> {}'.format(aivBot.taskMMAPName))
        aivBotMmap = AivBotMmap(aivBot)
        # aivBotMmap.aivBot = aivBot
        aivBotMmap.onStartTask = aivBot.onStartTask #响应AGI调用Bot的api接口执行任务的事件
        aivBotMmap.onInitBot = aivBot.onBotApiData #响应AGI获取Bot的api接口数据事件 2024.4

        if callFun is not None:
            callFun()  #调用用户设置的回调函数----------

        aivBot.initParam() # 加载 Bot Api的参数,在这里,可以选择性加载 2023.11

        ''' 2023.11
            用线程检测进程 wcPid 是否退出
            用线程检测 wcPid 进程是否退出(不是用 asyncio 协程,是用 threading 检测),如果wcPid进程退出,线程也跟着退出 
            原因是 asyncio的所有子协程都是在进程的主线程运行, 当Aiv平台的bot模块运行任务时,基本是上独占模式(死循环)
            这样如果用户中止任务,虽然bot模块也收到 TaskState.taskProExit 信号,但 aivBotMmap.run() 阻塞在运行任务上
            没办法响应  TaskState.taskProExit 信号, 但线程是可以的.因此,在 aivBotMmap.run()检测任务是否中止信号上,
            另外用线程 threading 建立一个独立于主线程的子线程,用于检测wcPid是否退出(这里是检测aivwc.py 的进程)。这样,
            当协程失灵时,threading的线程仍然可用,可以保证用户下达的中止指令可以执行。
        '''
        aivBotMmap.createCheckPidThread([aivBot.botInfo.ppid,aivBot.botInfo.wcpid],aivBot.botInfo.botName)

        logger.debug('Bot模块[ {} ]启动成功.'.format(aivBot.botInfo.botName))
        # 协程函数
        async def _main():
            # aivBotMmap的功能主要是检测是否有新任务(抢单),二是检测任务的状态,如果任务被前端取消,则马上退出进程
            # 另外,也要不断检测任务是否超时,超时就自动中止进程 2023.11
            asyncio.create_task(aivBotMmap.run())  
            while True:
                await asyncio.sleep(0.2) #只要主程序不退出,上面的两个协程就一直运行

        asyncio.run(_main())
    except Exception as e:
        from loguru import logger
        logger.warning('运行Bot.run() 出错! Error= {}'.format(e))

class AivBotInfo:
    def __init__(self) -> None:
        self.pid = os.getpid() # 当前进程的PID
        self.ppid = None #父进程的pid,根据父进程pid,如果它退出,自己也退出
        self.wcpid = None # 同级子进程 wc的进程pid,如果在命令行参数中传入此值,则可以监控此值,同步退出进程 2023.11
        self.botId = ''
        self.botName = ''
        self.path = '' #主执行文件路径(含文件名)
        self.taskMMAPName = '' #当前任务启用的共享内存名称
        self.isGetBotApi = False #是否是初始化Bot的Api接口

    def getBotInfo(self):
        '''
            返回当前模块的信息
        '''
        return {
            'botName': self.botName,
            'botId' : self.botId,
            'path': self.path,
            'pid': self.pid,
            'ppid': self.ppid,
            'wcpid': self.wcpid,
            'taskMMAPName': self.taskMMAPName
        }

class AivBot:
    def __init__(self) -> None:
        self.task = None #用于临时记录任务信息, 在 addFileToTaskOutParam()调用
        self.botOption = None
        self.botInfo = AivBotInfo()
        self.api = [] # 记录当前bot模块所有的Api信息

        if len(sys.argv)>1:
            self.botInfo.ppid = int(sys.argv[1]) #如果命令行第一个参数传应用的主进程pid过来
        if len(sys.argv)>2:
            self.botInfo.taskMMAPName = sys.argv[2] #这个是前端传过来的 taskId (32位长度的字符串,全球唯一)
        if len(sys.argv)>3:
            self.botInfo.wcpid = int(sys.argv[3])  # 同级子进程 wc的进程pid,如果在命令行参数中传入此值,则可以根据此值,同步退出进程
        if len(sys.argv)>4:
            self.botInfo.botName = sys.argv[4] #第4个参数传 botName 2023.12
        if len(sys.argv)>5:
            # 所有参数都必须转成str类型传进子进程,因为这里要对比 == 'True'
            self.botInfo.isGetBotApi = sys.argv[5] == 'True' #第5个参数传决定当前进程是任务进程还是获取Bot数据的进程 2024.4
            

        # print('AivBot收到的 taskMMAPName ==> {}'.format(self.taskMMAPName))


    def initParam(self):
        from loguru import logger

        if self.api is not None:
            # logger.debug('self.api 不为空!')

            for aivApi in self.api:
                # logger.debug('循环所有Api {}'.format(aivApi['name']))
                if aivApi['paramIn'] is None:
                    try:
                        callParam = {'sysInfo':aivBotMmap.sysInfo} #把任务信息和系统信息打包,一起给bot的api传参
                        aivApi['fun']('init', callParam) #执行api的初始化函数, 传递 cmd = 'param' 指令进去
                    except Exception as e:
                        logger.warning('函数: {}获取参数阶段出错, Error= {}'.format(aivApi['name'],e))
        
        
            # 检查所有的Api函数的参数是否都设置了---
            haveParam = True
            for aivApi in self.api:
                if aivApi['paramIn'] is None:
                    haveParam = False
                    break

            if haveParam:
                logger.debug('Bot模块 {} 载入完成!'.format(self.botInfo.botName))
                # break

    def onBotApiData(self):
        ''' 2024.4
            响应AGI向当前Bot获取api接口数据的事件
            self.api 中的数据是api对象列表,api中包含function的内存地址,它们是不能转换成Json数据.
            (aivtool.py中的_aiv_json()在转换成JSON数据时,会自动抛弃指向function内存地址的数据)

            botApi: Bot的api列表(api中也有每个api的配置: 'apiOption' 字段)
            botOption: Bot的全局配置参数(如:reload,timeout等)
        '''
        return {'botApi': self.api, 'botOption': self.botOption}
        

    def onStartTask(self,task):
        ''' 2023.09
            ### 生成调用函数的参数
            * 前端返回服务器,服务器调用 Bot 的参数,是一个dict列表,本函数用 parser.parse_args 把dict转换成 Namespace 命名空间
            * 此函数把多余的数据删除,只留下类似格式dict: {'参数名1': '参数值1','参数名2': '参数值2', ... } 
        '''
        from loguru import logger
        # from .aivtool import getFileInfo
        # logger.debug('aivBot 收到的启动任务参数是: task ==> {}'.format(task))

        # ======= 调api的参数准备 ============================================== 1
        try:
            # 检测是否有输入参数 'paramIn'
            if task['paramIn'] is None:
                raise Exception("任务的 ParamIn 为空！")
            
            self.task = task
            self.task['result']['apiTimeStart'] = int(time.time()*1000) # api的启动时间(毫秒)

            # 检查是否有调用的bot api 函数名
            apiName = task['apiInfo'].get('name',None)
            if apiName is None:
                logger.error('客户端没有指定要调用的bot api函数名! ')

            if len(self.api)==0:
                logger.error('检测到Bot: {} 无注册任何api函数.'.format(self.botInfo.botName))


            apiName = apiName.strip()
            # 根据任务给定的api函数名,找出 bot 对应的真实函数 (通过 botName)
            apiFun = None
            apiOption = None
            for api in self.api:
                if api['name'].strip().lower() == apiName.lower():

                    apiFun = api['fun']
                    apiOption = api['apiOption'] #对于 api的配置,用户可以在api函数中自行利用
                    break

            if apiFun is None:
                raise Exception('本地Bot模块无api函数:[ {} ]! 请检测Bot模块的api函数名称.'.format(apiName))
            

            # ============正式调用bot api 函数 =========================================================== 2 
            from .aivmmap import TaskResultCode
        
            # 运行bot api函数('run'阶段)----------------------------------------------
            callParam = {'sysInfo':aivBotMmap.sysInfo, 'taskInfo': task, 'apiOption': apiOption} #把任务信息和系统信息打包,一起给bot的api传参
            retTask = apiFun('run',callParam) #调用用户Bot的api函数 2024.4
            # logger.warning('Bot api {} 运行返回结果是: {}'.format(apiName,retTask))
            # -----------------------------------------------------------------------

            # 根据生成的文件,生成文件信息---------------------------------
            # paramOut = task['paramOut']
            # for param in paramOut:
            #     if (param['type'].lower() == 'file') and (param['data'] is not None):  
            #         for i in range(len(param['data'])):
            #             file = param['data'][i]
            #             # 根据文件名生成文件信息（如果文件没有生成在磁盘,则部分信息为空<如文件大小、md5码等>)
            #             param['data'][i] = getFileInfo(file['path']) #用函数getFileInfo 生成文件的信息 更新原来的文件信息
            #             # print('文件信息是:',fileInfo)
            # ---------------------------------------------------------
            
            if retTask is None or  retTask['result']['code'] != 200:
                # 设置成功标志
                aivBotMmap.setTaskResultCode(TaskResultCode.taskOk,'Bot:{} 的api {}运行完成.'.format(self.botInfo.botName, apiName)) # 设置为OK状态

        except Exception as e:
            errMsg = 'Bot模块[ {} ]的api函数:{} 执行出现错误: {}'.format(self.botInfo.botName,api['name'],e)
            logger.warning(errMsg)
            aivBotMmap.setTaskResultCode(TaskResultCode.taskSvr,errMsg) # 设置为服务器出错状态,并把出错信息回传js端 2023.12
        finally:
            self.task['result']['apiTimeEnd'] = int(time.time()*1000) # api运行的结束时间(毫秒)
            aivBotMmap.endTask() # api函数内修改了task对象,也会同步返回
            # logger.warning('apiFun finally 运行完成222!') 


    def push(self,type,data):
        '''
            添加输出内容
            type: 可选值 'file','string'
            data: 输出的具体内容(文件路径、字符串等)  
        '''
        from loguru import logger
        if self.task is None:
            logger.warning("如果是 cmd =='init' 阶段, push()函数不能使用! 需要在 cmd =='run' 阶段, 请加上if cmd == 'run' 语句")
            return
        
        if type.lower() == 'string':
            self._addStringToTaskOutParam(data)

        if type.lower() == 'file':
            self._addFileToTaskOutParam(data)

        
        logger.debug('当前输出的内容是: {}'.format(self.task['paramOut']))


    def getParamList(self,type= None, paramName= None):
        ''' 2024.6
            获取客户端的传参
            这里目的是方便开发者可以快速获取客户端的传参 (因为客户的传参多重嵌套,容易混淆。可以先在iBot函中print(param)显示整个参数结构)
            @param type 指定要读取的参数类型：可选 'string','file'
            @param paramName  指定要读取的参数名称(留空则只读取大类出来) 
            @result 返回值是一个列表 [] , 注意!
        '''

        paramIn = self.task['paramIn']
        if(type is None):
            return paramIn
        else:
            for param in paramIn:
                if param['type'].lower() == type.lower():
                    if paramName is None:
                        return param['data']  #返回所有数据 (如果是'string',可能有多个 'string'类型的参数在  paramIn 对象中; 而如果 'file'类型,则都只会写入一个对象中) 2024.6
                    
                    else:
                        if param['name'].lower() == paramName.lower(): # 比如获取 'prompt'参数的值:  getParam('string','prompt')
                            return param['data']  #读出所有行 (param['data'] 是一个列表)
       
        return None
                   
   
    def _addFileToTaskOutParam(self,filePath):
        from loguru import logger
        if not os.path.exists(filePath):
            logger.warning('找不到文件: {}'.format(filePath))
            return
        
        if self.task is None:
            logger.warning('没有任务信息')
        else:
            # logger.debug('接收新的回传文件: {}'.format(filePath))
            # def _caleFile(): #统计生成的文件数量及所有文件大小, 以便后期统计
            #     fileCount,fileSize = 0,0
            #     for paramOut in self.task['paramOut']:
            #             if paramOut['type'].lower() == 'file':
            #                 for file in paramOut['data']:
            #                     fileCount += 1
            #                     fileSize = fileSize + file['size']
            #     return {'fileCount': fileCount, 'allFileSize': fileSize}

            from .aivtool import getFileInfo         
            currParam = None
            isEmptyFile = True
            if len(self.task['paramOut']) > 0:                
                for param in self.task['paramOut']:
                    # 'paramOut'里面必须有且仅有一条 'type'=='FILE'的记录 2024.4
                    if param['type'].lower() == 'file' and param['data'] is not None:
                        isFind = False
                        currParam = param
                        # 如果已经存在 param['type'] == 'FILE' 的记录,则查询当前文件是否保存在里面
                        for file in param['data']:
                            if file['path'].lower() == filePath.lower():
                                isFind = True
                                break

                        if not isFind:
                            # logger.debug('接收新的回传文件: {}'.format(filePath))
                            # 如果判断没有保存,则新增一个文件记录到 'data'数组
                            param['data'].append(getFileInfo(filePath))

                        isEmptyFile = False

            if isEmptyFile: #没有 'type' == 'FILE' 的记录,直接添加一条
                currParam = {'type': 'file', 'data': [getFileInfo(filePath)]}
                self.task['paramOut'].append(currParam)

            # option = _caleFile()
            # currParam['option'] = option


    def _addStringToTaskOutParam(self, text):

        def _caleText(): #统计生成的文字行数及字数,以便后期评估生成的数据
            line,textLong = 0,0
            for paramOut in self.task['paramOut']:
                    if paramOut['type'].lower() == 'string':
                        for text in paramOut['data']:
                            line += text.count('\n') #计算每个字符串中包含多少个'\n'即是多少行
                            textLong += len(text)
            return {'lineCount': line, 'textCount': textLong}

        isEmptyText = True
        currParam = None
        if len(self.task['paramOut'])>0:
            for param in self.task['paramOut']:
                # 'paramOut'里面必须有且仅有一条 'type'=='STRING'的记录 2024.4
                if param['type'].lower() == 'string' and param['data'] is not None:
                    currParam = param
                    param['data'].append(text)
                    isEmptyText = False
                    break
 
        if isEmptyText:      
            currParam = {'type':'string', 'data': [text]}    
            self.task['paramOut'].append(currParam)

        option = _caleText() #统计生成的文字行数及字数 (如果是文件数据,则由aivc模块统计生成的文件总大小和文件数量) 2024.6
        currParam['option'] = option
        


    def regBotApi(self,glob:dict): #利用 globals() 读取指定模块的所有函数名
        ''' 2023.10
        ### 注册 bot 模块
        * 参数 glob 包含有模块的函数及函数地址！
        * 将自动注册所有用户自定义的函数!(除以横线'_'开头的和run()函数)
        * Api 函数必须有两个参数,分别是(cmd, parser)
        * 可以导入其它模块的函数成为api函数 : from xxx.xxx import xxxxfun
        '''
        from loguru import logger
        from .aivtool import checkReservedName
        lst = list(glob)
        import types
        # logger.debug('bot 模块所有参数如下 (包含模块内所有函数、方法名称和内存地址): \n{}'.format(glob))

        #循环模块的所有函数,把aiv 开头的函数自动导入----------------------------------
        for fun_name in lst:
            fun = glob[fun_name]   
            if (type(fun) == types.FunctionType) or (type(fun) == types.MethodType): #判断是方法（而不是属性)
                if fun_name != 'run' and not fun_name.startswith('_'): #排除检测 run()函数和 "_"开头的函数 2024.3 ,其它函数都可以导出                              
                    
                    if not checkReservedName(fun_name,'Bot: {} 的Api函数'.format(self.botInfo.botName)):
                        
                        title = ''
                        if fun.__doc__ is not None:
                            title = fun.__doc__.strip()[:16] #读取函数备注内容,取前16个字符

                        # apidict 只记录静态的信息
                        apidict = {'bot':self.botInfo.botName, 'name':fun_name, 'title': title, 'fun':fun,'paramIn':None,'apiOption':None}
                        self.api.append(apidict)

                        # callParam = {'bot':self, 'sysInfo':aivBotMmap.sysInfo} #把任务信息和系统信息打包,一起给bot的api传参  
                        # fun('init', callParam) #初始化Api函数
                 

        logger.info('\nbot模块:[ {} ] api函数初始化完成.'.format(self.botInfo.botName))

        if len(self.api)==0:
            logger.warning('Bot: {} 还没有注册任何 api 函数.'.format(self.botInfo.botName))
        else:
            logger.debug('\nrun() 成功启动bot模块:{} \n它的api函数列表是: \n{}'.format(self.botInfo.botName,self.api))


    def getOutPath(self,childPath):
        ''' 
            在AIV系统默认的输出目录中创建一个子文件夹
            可以在此目录基础上新建一个子目录给每个Bot专用 ,在设置'sys.outDir'目录里的生成文件会定时被清理, 
            可以避免系统运行久了垃圾过多的问题. (每隔10分钟系统清理一次超过24小时未使用的临时文件,比如图片、社频等)
            客户端一般都是生成图片或程序即会自动下载,AGI端无需长期保存. 2024.3
        '''
        outPath = aivBotMmap.sysInfo['sys.outDir'] 
        outPath = os.path.normpath(os.path.join(outPath,childPath)) #需要用normpath()规范化路径
        if not os.path.exists(outPath):
            os.mkdir(outPath)
        return outPath





    







