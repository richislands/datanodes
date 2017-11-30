using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Com.Richisland.RDBHandle
{
    public class Rtds
    {
        private const string Dll_Name = "sg_dl_rtds_pb.dll";

        private const string FUN_Init = "rtds_init";
        private const string FUN_SetData = "rtds_set_data";
        private const string FUN_GetCurData = "rtds_get_cur_data";
        private const string FUN_Rtds_Release = "rtds_release_mem";

        /// <summary>
        /// RTDS初始化
        /// </summary>
        /// <returns></returns>
        [DllImport(Dll_Name, EntryPoint = FUN_Init, CharSet = CharSet.Ansi)]
        public static extern int rtds_init();

        /// <summary>
        /// 设置数据
        /// </summary>
        /// <param name="data">点数据内容</param>
        /// <returns></returns>
        [DllImport(Dll_Name, EntryPoint = FUN_SetData, CharSet = CharSet.Ansi)]
        public static extern int rtds_set_data(byte[] data, int data_len);

        /// <summary>
        /// 获取当前数据
        /// </summary>
        /// <param name="data">点数据内容</param>
        /// <returns></returns>
        [DllImport(Dll_Name, EntryPoint = FUN_GetCurData, CharSet = CharSet.Ansi)]
        public static extern int rtds_get_cur_data(byte[] data, int data_len, out IntPtr unmanaged_ptr);

        /// <summary>
        /// 清理C++内存空间
        /// </summary>
        /// <param name="unmanaged_ptr">指针</param>
        [DllImport(Dll_Name, EntryPoint = FUN_Rtds_Release, CharSet = CharSet.Ansi)]
        public static extern void rtds_release_mem(out IntPtr unmanaged_ptr);
    }
}
