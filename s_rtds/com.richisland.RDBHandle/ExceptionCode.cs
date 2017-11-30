using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Com.Richisland.RDBHandle
{
    #region 定义枚举类型
    /// <summary>
    /// 错误码
    /// </summary>
    public enum eErrorCode
    {
        INIT_PARAM_ERR = 0x03090001,        // Init 参数异常
        INIT_ZMQ_ERR = 0x03090002,          // Init zmq服务启动异常
        CFG_PARAM_ERR = 0x03090101,         // bind_config 参数异常
        CFG_NOTAG_ERR = 0x03090102,         // bind_config 初始化标签点为空
        BIND_CFG_ERR = 0x03090103,          // bind_config 初始化配置失败
        BIND_PARAM_ERR = 0x03090201,        // bind_data 参数异常
        BIND_NOTAG_ERR = 0x03090202,        // bind_data 绑定数据为空
        BIND_NOTIN_ERR = 0x03090203,        // bind_data 绑定数据不在集合中
        START_NOCFG_ERR = 0x03090301,       // start_service configName不存在
        START_SERVICE_ERR = 0x03090302,     // start_service 失败
        STOP_NOCFG_ERR = 0x03090401,        // stop_service configName不存在
        STOP_SERVICE_ERR = 0x03090402,      // stop_service 失败
        GET_NONAME_ERR = 0x03090501,        // get_data dataName不存在
        SET_PARAM_ERR = 0x03090601,         // set_data 参数异常
        SET_NONAME_ERR = 0x03090602,        // set_data dataName不存在
        SET_NOTAG_ERR = 0x03090603,         // set_data 设置数据为空
        SET_MORE_ERR = 0x03090604,          // set_data 设置数据总数大于绑定数据总数
        SET_NOTBIND_ERR = 0x03090605,       // set_data 设置数据存在标签点未绑定
        SET_DATA_ERR = 0x03090606,          // set_data 设置数据失败
        DISPOSE_NOCFG_ERR = 0x03090701,     // dispose_data  configName不存在
        DISPOSE_NONAME_ERR = 0x03090702,    // dispose_data  dataName不存在
        DISPOSE_DATA_ERR = 0x03090703,      // dispose_data 清空数据失败

        INIT_CFG_ERR = 0x04090101,          // InitConfig 初始化配置失败
        START_ERR = 0x04090201,             // Start 开始线程失败
        STOP_ERR = 0x04090301,              // Stop 停止线程失败
        SETDATA_ERR = 0x04090401,           // SetData 设置数据失败
        DISPOSE_ERR = 0x04090501            // Dispose 清空数据失败
    }
    #endregion
}
