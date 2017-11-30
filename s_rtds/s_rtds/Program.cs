using Com.Richisland.HandleService;
using log4net;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace s_rtds
{
    class Program
    {
        /// <summary>
        /// 记录日志
        /// </summary>
        private static ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        static void Main(string[] args)
        {
            if (null != args && args.Count() > 0)
            {
                try
                {
                    HandleService handleServ = new HandleService();
                    // 调用HandleService中Init方法
                    int result = handleServ.Init(args[0], args[1], args[2]);

                    if (result == 1)
                    {
                        // 调用HandleService中run方法
                        handleServ.Run();
                    }
                }
                catch (Exception ex)
                {
                    log.Debug(string.Format("parameter error：{0}", ex.Message.ToString()));
                    System.Environment.Exit(0);
                }
            }
            else
            {
                log.Debug("parameter does not meet the requirements");
                System.Environment.Exit(0);
            }
        }
    }
}
