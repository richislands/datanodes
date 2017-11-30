using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Com.Richisland.Proto;

using log4net;
using NetMQ;
using NetMQ.Sockets;
using Com.Richisland.RDBHandle;
using Google.Protobuf;
using System.Collections;
using System.IO;
using System.Threading;

namespace Com.Richisland.HandleService
{
    public class HandleService
    {
        /// <summary>
        /// 配置信息字典
        /// </summary>
        private static List<string> configList = new List<string>();

        /// <summary>
        /// 请求点信息字典
        /// </summary>
        private static Hashtable dataDict = new Hashtable();

        /// <summary>
        /// 响应端socket
        /// </summary>
        private ResponseSocket serverSocket = null;

        /// <summary>
        /// 存储配置名与绑定数据名对照关系
        /// </summary>
        private static Hashtable config_dataName_ht = new Hashtable();

        /// <summary>
        /// 富岛实时数据库服务实体对象
        /// </summary>
        private RDB rdb = null;

        /// <summary>
        /// 记录日志
        /// </summary>
        private static ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        /// <summary>
        /// 初始化配置
        /// </summary>
        /// <param name="ip"></param>
        /// <param name="name"></param>
        /// <param name="N"></param>
        /// <returns>1：成功 -1：失败</returns>
        public int Init(string ip, string name, string N)
        {
            int result = 1;
            // 校验name是否为s_rtds
            if (name.ToLower() != "s_rtds")
            {
                result = (int)eErrorCode.INIT_PARAM_ERR;
                log.Debug(string.Format("init error：zmq start failed，because {0}", "name not match"));
            }
            else
            {
                if (int.Parse(N) == 1)
                {
                    try
                    {
                        string port = (40000 + int.Parse(N) * 1000 + 9).ToString();
                        // 完成ZMQ的bind完成ZMQ监听 此处ip地址、端口号后续增加校验
                        string address = "tcp://" + ip + ":" + port;
                        serverSocket = new ResponseSocket();
                        serverSocket.Bind(address);

                        log.Info("zmq start success");

                        // 初始化rtds
                        rdb = new RDB();

                        // DataList增加富岛实时数据服务状态（s_rtds_status_N）并更新为1
                        pb_data_sensor s_rtds_stt = new pb_data_sensor();
                        s_rtds_stt.Name = "s_rtds_status_" + N;
                        s_rtds_stt.Value = ByteString.CopyFromUtf8("1");
                        s_rtds_stt.Time =  rdb.GetCurrentTimeUnix();
                        if (!RDB.AllDataDict.ContainsKey("s_rtds_status_" + N))
                        {
                            RDB.AllDataDict.Add(s_rtds_stt.Name, s_rtds_stt);
                        }

                        Hashtable Statu = new Hashtable();
                        pb_data_sensor dataSensor = (pb_data_sensor)RDB.AllDataDict[s_rtds_stt.Name];
                        if (!Statu.ContainsKey(dataSensor.Name))
                        {
                            Statu.Add(dataSensor.Name, dataSensor);
                        }
                        else
                        {
                            Statu[dataSensor.Name] = dataSensor;
                        }
                        if (!dataDict.Contains(dataSensor.Name))
                        {
                            dataDict.Add("all_status", Statu);
                        }
                        else
                        {
                            dataDict["all_status"] = Statu;
                        }
                    }
                    catch (Exception ex)
                    {
                        result = (int)eErrorCode.INIT_ZMQ_ERR;
                        log.Debug(string.Format("init error：zmq start failed，because {0}", ex.Message.ToString()));
                    }
                }
                else
                {
                    result = (int)eErrorCode.INIT_PARAM_ERR;
                    log.Debug("init error：zmq start failed，because param N is not 1");
                }
            }
            return result;
        }

        /// <summary>
        /// ZMQ通信、接收到命令及参数、根据命令进行相应处理
        /// </summary>
        public void Run()
        {
            int result = 1;
            while (true)
            {
                // 等待接收Message
                var message = serverSocket.ReceiveMultipartMessage();
                // 获取命令
                var Command = message[0].ConvertToString();

                string typeName = "";
                string configName = "";
                string dataName = "";
                byte[] pbData = null;
                // switch case 进行判断
                switch (Command)
                {
                    case "bind_config":
                        typeName = message[1].ConvertToString();
                        byte[] configData = message[2].Buffer;
                        configName = message[3].ConvertToString();
                        result = bind_config(typeName, configData, configName);
                        break;
                    case "bind_data":
                        typeName = message[1].ConvertToString();
                        pbData = message[2].Buffer;
                        dataName = message[3].ConvertToString();
                        result = bind_data(typeName, pbData, dataName);
                        break;
                    case "start_service":
                        configName = message[1].ConvertToString();
                        result = start_service(configName);
                        break;
                    case "stop_service":
                        configName = message[1].ConvertToString();
                        result = stop_service(configName);
                        break;
                    case "set_data":
                        typeName = message[1].ConvertToString();
                        pbData = message[2].Buffer;
                        dataName = message[3].ConvertToString();
                        result = set_data(dataName, typeName, pbData);
                        break;
                    case "get_data":
                        dataName = message[1].ConvertToString();
                        pb_data_sensor_list data_sensor_list = null;
                        result = get_data(dataName, ref data_sensor_list);
                        if (result == 1)
                        {
                            var msg = new NetMQMessage();
                            msg.Append("pb_data_sensor_list");
                            MemoryStream sm = new MemoryStream();
                            data_sensor_list.WriteTo(sm);
                            msg.Append(sm.ToArray());
                            serverSocket.SendMultipartMessage(msg);
                            log.Debug(string.Format("server response：{0} pb_data_sensor in data_sensor_list", data_sensor_list.PbDataSensors.Count));
                        }
                        else
                        {
                            serverSocket.SendFrame(result.ToString());
                            log.Debug(string.Format("server response：result = 0x{0:X2}", result));
                        }
                        break;
                    case "dispose_data":
                        // 清空绑定的数据 缺少判断状态
                        configName = message[1].ConvertToString();
                        dataName = message[2].ConvertToString();
                        result = dispose_data(configName, dataName);
                        break;
                    case "auto_get_data":
                        break;
                }
                Thread.Sleep(100);
                if (Command != "get_data")
                {
                    serverSocket.SendFrame(result.ToString());
                    log.Debug(string.Format("server response：result = 0x{0:X2}", result));
                }
            }
        }

        /// <summary>
        /// 初始化配置
        /// </summary>
        /// <param name="configType">配置类型</param>
        /// <param name="configData">配置信息</param>
        /// <param name="configName">配置信息别名</param>
        /// <returns>1：成功 -1：失败</returns>
        private int bind_config(string configType, byte[] configData, string configName)
        {
            int result = 1;
            PbConfig pbConfig = pb_config_rtds.Parser.ParseFrom(configData);
            pb_config_rtds cfg = (pb_config_rtds)pbConfig;

            log.Debug(string.Format("server received：command：{0}, pbConfigType：{1}, configName：{2}, {3} tags in Config", "bind_config", configType, configName, cfg.TagInfors.Count));

            if (configType.ToLower() != "pb_config_rtds")
            {
                result = (int)eErrorCode.CFG_PARAM_ERR;
                log.Debug(string.Format("bind_config error：params {0} ≠ pb_config_rtds", configType));
            }
            else
            {
                if (!string.IsNullOrEmpty(configName))
                {
                    if (cfg.TagInfors.Count > 0)
                    {
                        result = rdb.InitConfig(configName, pbConfig);
                        if (result == 1)
                        {
                            if (!configList.Contains(configName))
                            {
                                configList.Add(configName);
                            }
                        }
                        else
                        {
                            result = (int)eErrorCode.BIND_CFG_ERR;
                        }
                    }
                    else
                    {
                        result = (int)eErrorCode.CFG_NOTAG_ERR;
                        log.Debug("bind_config error：init config data is empty");
                    }
                }
                else
                {
                    result = (int)eErrorCode.CFG_PARAM_ERR;
                    log.Debug("bind_config error：params configName is null");
                }
            }
            return result;
        }

        /// <summary>
        /// 绑定数据
        /// </summary>
        /// <param name="pbDataType">数据类型</param>
        /// <param name="pbData">数据信息</param>
        /// <param name="dataName">绑定数据别名</param>
        /// <returns>1：成功 -1：失败 -2：请求点不在集合中</returns>
        private int bind_data(string pbDataType, byte[] pbData, string dataName)
        {
            int result = 1;
            pb_data_sensor_list data_sensor_list = pb_data_sensor_list.Parser.ParseFrom(pbData);

            log.Debug(string.Format("server received：command：{0}, pbDataType：{1}, dataName：{2}, {3} tags in bind_data", "bind_data", pbDataType.ToLower(), dataName, data_sensor_list.PbDataSensors.Count));

            if (pbDataType.ToLower() != "pb_data_sensor_list")
            {
                result = (int)eErrorCode.BIND_PARAM_ERR;
                log.Debug(string.Format("bind_data error：params {0} ≠ pb_data_sensor_list", pbDataType));
            }
            else
            {
                // 判断绑定数据是否为空
                if (data_sensor_list.PbDataSensors.Count > 0)
                {
                    // 判断请求点是否在集合中                    
                    foreach (var data_sensor in data_sensor_list.PbDataSensors)
                    {
                        if (!RDB.AllDataDict.ContainsKey(data_sensor.Name))
                        {
                            result = (int)eErrorCode.BIND_NOTIN_ERR;
                            log.Debug("bind_data error：the tag " + data_sensor.Name + " not exist");
                            break;
                        }
                    }
                    if (result != 0x03090203)
                    {
                        Hashtable PbList = new Hashtable();
                        foreach (var data_sensor in data_sensor_list.PbDataSensors)
                        {
                            pb_data_sensor dataSensor = (pb_data_sensor)RDB.AllDataDict[data_sensor.Name];
                            if (!PbList.Contains(dataSensor.Name))
                            {
                                PbList.Add(dataSensor.Name, dataSensor);
                            }
                        }
                        // 绑定dataName与AllDataDict
                        if (!dataDict.ContainsKey(dataName))
                        {
                            dataDict.Add(dataName, PbList);
                        }
                        else
                        {
                            dataDict[dataName] = PbList;
                        }
                    }
                }
                else
                {
                    result = (int)eErrorCode.BIND_NOTAG_ERR;
                    log.Debug("bind_data error：bind data is empty");
                }
            }
            return result;
        }

        /// <summary>
        /// 开始服务
        /// </summary>
        /// <param name="configName">配置信息别名</param>
        /// <returns></returns>
        private int start_service(string configName)
        {
            int result = 1;
            log.Debug(string.Format("server received：command：{0}, configName：{1}", "start_service", configName));
            // 判断是否初始化配置
            if (!configList.Contains(configName))
            {
                result = (int)eErrorCode.START_NOCFG_ERR;
                log.Debug("start_service error：param " + configName + " not exist");
            }
            else
            {
                result = rdb.Start(configName);
                if (result != 1)
                {
                    result = (int)eErrorCode.START_SERVICE_ERR;
                }
            }
            return result;
        }

        /// <summary>
        /// 停止服务
        /// </summary>
        /// <param name="configName">配置信息别名</param>
        /// <returns></returns>
        private int stop_service(string configName)
        {
            int result = 1;
            log.Debug(string.Format("server received：command：{0}, configName：{1}", "stop_service", configName));
            // 判断是否初始化配置
            if (!configList.Contains(configName))
            {
                result = (int)eErrorCode.STOP_NOCFG_ERR;
                log.Debug("start_service error：param " + configName + " not exist");
            }
            else
            {
                result = rdb.Stop(configName);
                if (result != 1)
                {
                    result = (int)eErrorCode.STOP_SERVICE_ERR;
                }
            }
            return result;
        }

        /// <summary>
        /// 获取数据
        /// </summary>
        /// <param name="dataName">获取数据别名</param>
        /// <param name="data_sensor_list">返回数据集合</param>
        /// <returns></returns>
        private int get_data(string dataName, ref pb_data_sensor_list data_sensor_list)
        {
            int result = 1;
            log.Debug(string.Format("server received：command：{0}, dataName：{1}", "get_data", dataName));

            // 判断dataName在dataDict集合中是否存在
            if (!dataDict.ContainsKey(dataName))
            {
                result = (int)eErrorCode.GET_NONAME_ERR;
                log.Debug("get_data error：param " + dataName + " not exist");
            }
            else
            {
                data_sensor_list = new pb_data_sensor_list();

                data_sensor_list.ListId = 1;
                Hashtable TmpTable = (Hashtable)dataDict[dataName];
                foreach (var value in TmpTable.Values)
                {
                    data_sensor_list.PbDataSensors.Add((pb_data_sensor)value);
                }
            }
            return result;
        }

        /// <summary>
        /// 设置数据
        /// </summary>
        /// <param name="dataName">数据别名</param>
        /// <param name="pbDataType">数据类型</param>
        /// <param name="pbData">数据内容</param>
        /// <returns></returns>
        private int set_data(string dataName, string pbDataType, byte[] pbData)
        {
            int result = 1;
            pb_data_sensor_list data_sensor_list = pb_data_sensor_list.Parser.ParseFrom(pbData);

            log.Debug(string.Format("server received：command：{0}, pbDataType：{1}, dataName：{2}, {3} tags need set_data", "set_data", pbDataType.ToLower(), dataName, data_sensor_list.PbDataSensors.Count));

            if (pbDataType.ToLower() != "pb_data_sensor_list")
            {
                result = (int)eErrorCode.SET_PARAM_ERR;
                log.Debug(string.Format("set_data error：param {0} ≠ pb_data_sensor_list", pbDataType));
            }
            else
            {
                if (!dataDict.ContainsKey(dataName))
                {
                    result = (int)eErrorCode.SET_NONAME_ERR;
                    log.Debug("set_data error：param " + dataName + " not exist");
                }
                else
                {
                    Hashtable dataList = new Hashtable();
                    Hashtable bind_data_sensor_list = (Hashtable)dataDict[dataName];                    

                    // 以绑定的数据为准
                    if (data_sensor_list.PbDataSensors.Count > 0)
                    {
                        // 要设置的标签点必须是绑定数据的子集
                        if (data_sensor_list.PbDataSensors.Count <= bind_data_sensor_list.Count)
                        {
                            // 校验要设置的标签点是否绑定
                            foreach (var data_sensor_l in data_sensor_list.PbDataSensors)
                            {
                                if (bind_data_sensor_list.Contains(data_sensor_l.Name))
                                {
                                    if (!dataList.ContainsKey(data_sensor_l.Name))
                                    {
                                        dataList.Add(data_sensor_l.Name, data_sensor_l);
                                    }
                                }
                                else
                                {
                                    result = (int)eErrorCode.SET_NOTBIND_ERR;
                                    log.Debug("set_data error：the tag " + data_sensor_l.Name + " not bind");
                                    break;
                                }
                            }
                            if(result != 0x03090605)
                            {
                                result = rdb.SetData(dataName, dataList);
                                if (result != 1)
                                {
                                    result = (int)eErrorCode.SET_DATA_ERR;
                                }
                            }
                        }
                        else
                        {
                            result = (int)eErrorCode.SET_MORE_ERR;
                            log.Debug("set_data error：set data is too much，is more than bind data");
                        }
                    }
                    else
                    {
                        result = (int)eErrorCode.SET_NOTAG_ERR;
                        log.Debug("set_data error：set data is empty");
                    }
                }                
            }
            return result;
        }

        /// <summary>
        /// 清空数据
        /// </summary>
        /// <param name="configName">配置项别名</param>
        /// <param name="dataName">数据别名</param>
        /// <returns></returns>
        private int dispose_data(string configName, string dataName)
        {
            int result = 1;
            log.Debug(string.Format("server received：command：{0}, configName：{1}, dataName：{2}", "dispose_data", configName, dataName));

            // 未初始化配置
            if (!configList.Contains(configName))
            {
                result = (int)eErrorCode.DISPOSE_NOCFG_ERR;
                log.Debug("dispose_data error：param " + configName + " not exist");
            }
            else
            {
                result = rdb.Dispose(configName, dataName);
                if (result == 1)
                {
                    if (!string.IsNullOrEmpty(dataName))
                    {
                        if (dataDict.ContainsKey(dataName))
                        {
                            dataDict.Remove(dataName);
                        }
                        else
                        {
                            result = (int)eErrorCode.DISPOSE_NONAME_ERR;
                            log.Debug("dispose_data error：param " + dataName + " not exist");
                        }
                    }
                    configList.Remove(configName);
                }
                else
                {
                    result = (int)eErrorCode.DISPOSE_DATA_ERR;
                }
            }
            return result;
        }
    }
}
