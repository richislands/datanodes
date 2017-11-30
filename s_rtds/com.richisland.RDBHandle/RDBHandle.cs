using Com.Richisland.Proto;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Com.Richisland.RDBHandle
{
    public abstract class RDBHandle
    {
        #region properties
        /// <summary>
        /// 数据节点名称
        /// </summary>
        public static string Name = "";

        /// <summary>
        /// 采集点集合
        /// </summary>
        public static Hashtable AllDataDict = new Hashtable();
        //public static Dictionary<string, PbData> AllDataDict = new Dictionary<string,PbData>();

        #endregion

        #region method
        /// <summary>
        /// 初始化数据服务配置
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <param name="config">配置信息对象</param>
        /// <returns></returns>
        public abstract int InitConfig(string configName, PbConfig config);

        /// <summary>
        /// 开始服务
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <returns></returns>
        public abstract int Start(string configName);

        /// <summary>
        /// 停止服务
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <returns></returns>
        public abstract int Stop(string configName);

        /// <summary>
        /// 设置数据
        /// </summary>
        /// <param name="dataName">请求点集合名称</param>
        /// <param name="dataList">点数据集合</param>
        /// <returns></returns>
        public abstract int SetData(string dataName, Hashtable dataList);

        /// <summary>
        /// 清空数据
        /// </summary>
        /// <param name="configName">配置项名称</param>
        /// <param name="dataName">请求点集合名称</param>
        /// <returns></returns>
        public abstract int Dispose(string configName, string dataName);
        #endregion
    }
}
