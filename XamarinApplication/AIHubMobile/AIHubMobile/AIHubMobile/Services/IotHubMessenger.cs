/* IoTHubMessenger.cs
 * Created by: John Symborski
 * 
 * Implementation of the IoTHubMessenger to interact w/ IoT Hub
 */

using System;
using System.Text;
using Microsoft.Azure.Devices;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace AIHubMobile
{
    public class IotHubMessenger : IIotHubMessenger
    {
        private const string conn = "HostName=pcl-dev-bgwilkinson-ioth.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=C91QtDRu89e9v33wBNJKNyQSqqsRRchl92BRsCObQck=";
        private ServiceClient client;
 
        public IotHubMessenger()
        {
            client = ServiceClient.CreateFromConnectionString(conn);
        }

        public async Task<bool> UpdateDeviceOptions(string DeviceName, StationOptions opt)
        {
            try
            {
                var json = JsonConvert.SerializeObject(opt);
                var commandMessage = new Message(Encoding.ASCII.GetBytes(json));
                await client.SendAsync(DeviceName, commandMessage);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return await Task.FromResult(false);
            }

            return await Task.FromResult(true);
        }

        public async Task<bool> RequestUpdateNow(string DeviceName)
        {
            return await Task.FromResult(false);
        }
    }
}
