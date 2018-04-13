/* IIoTHubMessenger.cs
 * Created by: John Symborski
 * 
 * Interface definition for the IoTHubMessenger
 */
using System.Threading.Tasks;

namespace AIHubMobile
{
    public interface IIotHubMessenger
    {
        Task<bool> UpdateDeviceOptions(string DeviceName, StationOptions opt);
        Task<bool> RequestUpdateNow(string DeviceName);
    }
}
