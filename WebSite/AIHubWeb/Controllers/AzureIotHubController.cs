using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Microsoft.Azure.Devices;
using System.Text;
using System.Threading.Tasks;

namespace AIHubWeb.Controllers
{
    public class AzureIotHubController : Controller
    {
        private const string conn = "HostName=pcl-dev-bgwilkinson-ioth.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=C91QtDRu89e9v33wBNJKNyQSqqsRRchl92BRsCObQck=";
        private ServiceClient client;

        public AzureIotHubController()
        {
            client = ServiceClient.CreateFromConnectionString(conn);
        }

        public async Task<bool> UpdateDeviceOptions(string DeviceName, StationOptions opt)
        {
            try
            {
                var commandMessage = new Message(Encoding.ASCII.GetBytes(Json(opt.editOptions).ToString()));
                await client.SendAsync(DeviceName, commandMessage);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return await Task.FromResult(false);
            }

            return await Task.FromResult(true);
        }

        //I dont know if we will do this because of power contraints
        public async Task<bool> RequestUpdateNow(string DeviceName)
        {
            return await Task.FromResult(false);
        }

    }
}