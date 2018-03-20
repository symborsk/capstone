using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text;

namespace AIHubMobile
{
    public interface IIotHubMessenger
    {
        Task<bool> UpdateDeviceOptions(string DeviceName, StationOptions opt);
        Task<bool> RequestUpdateNow(string DeviceName);
    }
}
