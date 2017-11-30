using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Com.Richisland.Proto;
using Google.Protobuf;
using System.Threading;
using log4net;
using System.IO;
using System.Runtime.InteropServices;
using System.Collections;

namespace Com.Richisland.RDBHandle
{
    public class RDB : RDBHandle
    {
        /// <summary>
        /// 配置信息集合
        /// </summary>
        private static Dictionary<string, PbConfig> AllConfigDict = new Dictionary<string, PbConfig>();

        /// <summary>
        /// 配置与采集点的集合
        /// </summary>
        private static Dictionary<string, List<string>> TagAndConfigDict = new Dictionary<string, List<string>>();

        /// <summary>
        /// 配置与线程对应的集合
        /// </summary>
        private static Dictionary<string, Thread> ConfigThreadDict = new Dictionary<string, Thread>();

        /// <summary>
        /// 线程状态
        /// </summary>
        private static Hashtable ThreadSttHash = new Hashtable();

        /// <summary>
        /// 记录日志
        /// </summary>
        private static ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        /// <summary>
        /// 构造函数
        /// </summary>
        public RDB()
        {
            try
            {
                // 读取标签点配置文件及开辟空间 返回 0 成功
                int result = 1;
                result = Rtds.rtds_init();
                if (result != 1)
                {
                    log.Debug(string.Format("rtds init failed，calling rtds_init method back result： {0}", result));
                }
                else
                {
                    log.Info("rtds init success");
                }
            }
            catch (Exception ex)
            {
                log.Debug(string.Format("rtds init failed，because {0}", ex.Message.ToString()));
            }
        }

        /// <summary>
        /// 初始化数据服务配置
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <param name="config">配置信息对象</param>
        /// <returns></returns>
        public override int InitConfig(string configName, PbConfig config)
        {
            int result = 1;

            try
            {
                // 私有配置信息维护
                if (!AllConfigDict.ContainsKey(configName))
                {
                    AllConfigDict.Add(configName, config);
                }
                // 增加配置点信息
                AddAllDataDict(configName, config);

                // 修改状态为已配置2
                SetRtdsStatus("2");
            }
            catch (Exception ex)
            {
                result = (int)eErrorCode.INIT_CFG_ERR;
                log.Debug("InitConfig Error：InitConfig failed，because " + ex.Message.ToString());
            }

            return result;
        }

        /// <summary>
        /// 开始服务
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <returns></returns>
        public override int Start(string configName)
        {
            int result = 1;

            try
            {                
                if (!ConfigThreadDict.ContainsKey(configName))
                {
                    Thread worker = new Thread(new ParameterizedThreadStart(Work));
                    worker.Name = configName;
                    worker.IsBackground = true;
                    worker.Start(configName);

                    ConfigThreadDict.Add(configName, worker);
                }
                // 首次给线程赋值true
                if (!ThreadSttHash.ContainsKey(configName))
                {
                    ThreadSttHash.Add(configName, true);
                }
                // 再次开启线程
                else
                {
                    ThreadSttHash[configName] = true;
                }                

                // 修改状态为已运行 3
                SetRtdsStatus("3");
            }
            catch (Exception ex)
            {
                result = (int)eErrorCode.START_ERR;
                log.Debug("Start Error：Start failed，because " + ex.Message.ToString());
            }

            return result;
        }

        /// <summary>
        /// 停止服务
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <returns></returns>
        public override int Stop(string configName)
        {
            int result = 1;    
        
            try
            {
                // 更新状态为2 已配置
                SetRtdsStatus("2");
                // 停止线程
                if (ThreadSttHash.ContainsKey(configName))
                {
                    ThreadSttHash[configName] = false;
                }
            }
            catch (ThreadAbortException ex)
            {
                result = (int)eErrorCode.STOP_ERR;
                log.Debug(string.Format("Stop Error：thread stop failed，because {0}", ex.Message.ToString()));
            }

            return result;
        }

        /// <summary>
        /// 设置数据
        /// </summary>
        /// <param name="dataName">请求点集合名称</param>
        /// <param name="dataList">点数据集合</param>
        /// <returns></returns>
        public override int SetData(string dataName, Hashtable dataList)
        {
            int result = 1;

            pb_data_sensor_list data_sensor_list = new pb_data_sensor_list();
            try
            {
                foreach (var data in dataList.Values)
                {
                    data_sensor_list.PbDataSensors.Add((pb_data_sensor)data);
                }
                MemoryStream mStream = new MemoryStream();
                data_sensor_list.WriteTo(mStream);

                result = Rtds.rtds_set_data(mStream.ToArray(), mStream.ToArray().Length);
                if (result != 1)
                {
                    log.Debug(string.Format("SetData Error：calling rtds_set_data method ，method returns：{0}", result));

                    result = (int)eErrorCode.SETDATA_ERR;
                }
            }
            catch (Exception ex)
            {
                result = (int)eErrorCode.SETDATA_ERR;
                log.Debug(string.Format("SetData Error：set data failed，because {0}", ex.Message.ToString()));
            }

            return result;
        }

        /// <summary>
        /// 清空数据
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <param name="dataName">请求点集合名称</param>
        /// <returns></returns>
        public override int Dispose(string configName, string dataName)
        {
            int result = 1;

            try
            {
                // 移除AllDataDict中点信息
                RemoveFromAllDataDict(configName);

                // 移除AllConfigDict中配置信息
                if (AllConfigDict.ContainsKey(configName))
                {
                    AllConfigDict.Remove(configName);
                }
                // 移除ConfigThreadDict中线程与configname关系
                if (ConfigThreadDict.ContainsKey(configName))
                {
                    ConfigThreadDict.Remove(configName);
                }
                // 移除ThreadSttHash中线程的状态
                if (ThreadSttHash.ContainsKey(configName))
                {
                    ThreadSttHash.Remove(configName);
                }
                // 更新状态为1 就绪
                SetRtdsStatus("1");
            }
            catch (Exception ex)
            {
                result = (int)eErrorCode.DISPOSE_ERR;
                log.Debug(string.Format("Dispose Error：dispose failed，because {0}", ex.Message.ToString()));
            }

            return result;
        }

        /// <summary>
        /// 开始读取数据并更新内存AllDataDict
        /// </summary>
        /// <param name="configObj">配置项名称</param>
        private void Work(object configObj)
        {
            string configName = configObj.ToString();
            // 获取数据更新周期
            int cycle = 0;
            foreach (KeyValuePair<string, PbConfig> kvp in AllConfigDict)
            {
                if (kvp.Key == configName)
                {
                    cycle = ((pb_config_rtds)kvp.Value).UpdateCycle;
                    break;
                }
            }
            while (GetThreadStt(configName))
            {
                var now = DateTime.Now;
                try
                {
                    pb_data_sensor_list pbDataList = new pb_data_sensor_list();
                    foreach (KeyValuePair<string, List<string>> kvp in TagAndConfigDict)
                    {
                        if (kvp.Value.Contains(configName))
                        {
                            pb_data_sensor dataObject = new pb_data_sensor();
                            dataObject.Name = kvp.Key;

                            pbDataList.PbDataSensors.Add(dataObject);
                        }
                    }

                    MemoryStream mStream = new MemoryStream();
                    pbDataList.WriteTo(mStream);

                    // 定义这个c#中用来接收c++返回数据的指针类型
                    IntPtr unmanaged_ptr = IntPtr.Zero;
                    int length = Rtds.rtds_get_cur_data(mStream.ToArray(), mStream.ToArray().Length, out unmanaged_ptr);

                    if (length > 0)
                    {
                        byte[] managed_data = new byte[length];
                        // 将非托管内存拷贝成托管内存，才能在c#里面使用
                        Marshal.Copy(unmanaged_ptr, managed_data, 0, length);

                        // 遍历返回标签点数据 并更新到内存中
                        pb_data_sensor_list data_sensor_list = pb_data_sensor_list.Parser.ParseFrom(managed_data);
                        foreach (pb_data_sensor pb_data_sensor in data_sensor_list.PbDataSensors)
                        {
                            if (AllDataDict.ContainsKey(pb_data_sensor.Name))
                            {
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Type = pb_data_sensor.Type;
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Size = pb_data_sensor.Size;
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Value = pb_data_sensor.Value;
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Time = pb_data_sensor.Time;
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Quality = pb_data_sensor.Quality;
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Status = pb_data_sensor.Status;
                                ((pb_data_sensor)AllDataDict[pb_data_sensor.Name]).Unit = pb_data_sensor.Unit;
                            }
                        }
                        // 清理C++内存空间
                        Rtds.rtds_release_mem(out unmanaged_ptr);
                    }
                    else
                    {
                        log.Debug(string.Format("GetData Error：calling rtds_get_cur_data method，method returns data length：{0}", length));
                    }
                    // 实时更新状态 为已运行 3
                    SetRtdsStatus("3");
                }
                catch (Exception ex)
                {
                    // 实时更新状态 为异常 4
                    SetRtdsStatus("4");
                    log.Debug(string.Format("GetData Error：update cache data failed，because {0}", ex.Message.ToString()));
                }
                // 如果数据更新周期为0 则只取一次数据
                if (cycle == 0)
                {
                    break;
                }
                else
                {
                    var cur = DateTime.Now;
                    TimeSpan ts = cur - now;
                    if (ts.TotalMilliseconds < cycle * 1000)
                    {
                        Thread.Sleep(cycle * 1000 - (int)ts.TotalMilliseconds);
                    }
                }
            }
        }

        /// <summary>
        /// 获取当前运行状态
        /// </summary>
        /// <param name="runTag"></param>
        /// <param name="runTagValue"></param>
        /// <returns></returns>
        private static string GetRunStatus(string runTag, string runTagValue)
        {
            if (AllDataDict.ContainsKey(runTag))
            {
                runTagValue = ((pb_data_sensor)AllDataDict[runTag]).Value.ToStringUtf8();
            }
            else
            {
                runTagValue = "notexist";
            }
            return runTagValue;
        }

        /// <summary>
        /// 新增采集点信息
        /// </summary>
        /// <param name="configName">配置信息名称</param>
        /// <param name="Config">配置信息</param>
        private void AddAllDataDict(string configName, PbConfig Config)
        {
            pb_config_rtds config_rtds = (pb_config_rtds)Config;
            foreach (var tag in config_rtds.TagInfors)
            {
                pb_data_sensor dataObject = new pb_data_sensor();
                dataObject.Name = tag.Name;
                dataObject.Type = pb_data_type.EnumInt32;
                dataObject.Size = 0;
                dataObject.Value = ByteString.CopyFromUtf8("");
                dataObject.Time = 0;
                dataObject.Quality = 128;
                dataObject.Status = pb_data_status.Nonexist;
                dataObject.Unit = pb_data_unit.NoneUnit;
                if (!AllDataDict.ContainsKey(dataObject.Name))
                {
                    AllDataDict.Add(dataObject.Name, dataObject);
                }

                // 建立configName与配置点的关系                
                if (!TagAndConfigDict.ContainsKey(dataObject.Name))
                {
                    List<string> ConfigNameList = new List<string>();
                    TagAndConfigDict.Add(dataObject.Name, ConfigNameList);
                    TagAndConfigDict[dataObject.Name].Add(configName);
                }
                else
                {
                    TagAndConfigDict[dataObject.Name].Add(configName);
                }
            }
        }

        /// <summary>
        /// 移除采集点信息
        /// </summary>
        /// <param name="configName">配置信息名称</param>
        private void RemoveFromAllDataDict(string configName)
        {
            if (AllConfigDict.ContainsKey(configName))
            {
                pb_config_rtds configObject = (pb_config_rtds)AllConfigDict[configName];
                // 校验采集点在其他配置中是否使用
                foreach (var tagObject in configObject.TagInfors)
                {
                    if (TagAndConfigDict.ContainsKey(tagObject.Name))
                    {
                        if (TagAndConfigDict[tagObject.Name].Count == 1)
                        {
                            if (AllDataDict.ContainsKey(tagObject.Name))
                            {
                                AllDataDict.Remove(tagObject.Name);
                            }
                            TagAndConfigDict.Remove(tagObject.Name);
                        }
                        else
                        {
                            TagAndConfigDict[tagObject.Name].Remove(configName);
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 获取线程状态
        /// </summary>
        /// <param name="configName">线程名称</param>
        /// <returns></returns>
        private bool GetThreadStt(string configName)
        {
            bool threadStt = false;
            if (ThreadSttHash.ContainsKey(configName))
            {
                threadStt = (bool)ThreadSttHash[configName];
            }
            return threadStt;
        }

        /// <summary>
        /// 设置服务状态
        /// </summary>
        /// <param name="value"></param>
        private void SetRtdsStatus(string value)
        {
            // 实时更新状态
            if (AllDataDict.ContainsKey("s_rtds_status_1"))
            {
                ((pb_data_sensor)AllDataDict["s_rtds_status_1"]).Value = ByteString.CopyFromUtf8(value);
                ((pb_data_sensor)AllDataDict["s_rtds_status_1"]).Time = GetCurrentTimeUnix();
            }
        }

        /// <summary>
        /// 获取当前本地时间戳
        /// </summary>
        /// <returns></returns>      
        public long GetCurrentTimeUnix()
        {
            TimeSpan cha = (DateTime.Now - TimeZone.CurrentTimeZone.ToLocalTime(new System.DateTime(1970, 1, 1)));
            long t = (long)cha.TotalSeconds;
            return t;
        }
    }
}
