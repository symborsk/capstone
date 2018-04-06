using System;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using Newtonsoft.Json.Linq;
using System.Threading.Tasks;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;
namespace AIServerConsoleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 0)
            {
                Console.WriteLine("Invalid number of arguments: expected 0" + args.Length);
                return;
            }

            CloudStorageAccount storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            CloudBlobClient client = storageAccount.CreateCloudBlobClient();

            Task<List<CloudBlockBlob>> task = Task.Run(() => GetAllList(client));
            List<CloudBlockBlob> rgBlobs  = task.Result;

            foreach(CloudBlockBlob blob in rgBlobs)
            {
                Task<string> taskDownload = Task.Run(() => blob.DownloadTextAsync());
                String sDownloadedBlob = taskDownload.Result;
                String [] sDownloadedBlobs = sDownloadedBlob.Split(new[] { Environment.NewLine }, StringSplitOptions.None);

                foreach (string item in sDownloadedBlobs)
                {
                    JObject obj = JObject.Parse(item);
                    string timestamp = obj["timestamp"].ToString();
                    run_cmd(@"C:\git\ai_model\scripts\model.py", String.Format("-eval -json \'{0}\'", item));
                    obj["Forecast"] = run_cmd(@"C:\git\ai_model\scripts\model.py", String.Format("-eval -json \'{0}\'", item));
                }
            }
        }

        static async void PushDataUpToAzure(CloudBlobClient cli, string jsonObj, string timestamp)
        {
            bool succ = await SendJsonToStorage(cli, jsonObj, timestamp);

            if (succ)
                Console.WriteLine("Success writing JSON file to azure storage");
            else
                Console.WriteLine("Failure Loading JSON file to azure storage... Goodbye");
        }

        static async Task<bool> SendJsonToStorage(CloudBlobClient blobClient, string fullFilePath, string timeStamp)
        {
            BlobContinuationToken continuationToken = null;
            BlobResultSegment resultSegment = null;

            try
            {
                //Convert the unix timestamp to a date
                DateTime dtDateTime = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc);
                dtDateTime = dtDateTime.AddSeconds(Double.Parse(timeStamp));

                string pathToBlob = dtDateTime.Year + "//" + dtDateTime.Month + "//" + dtDateTime.Date;

                // Retrieve reference to a previously created container
                CloudBlobContainer container = blobClient.GetContainerReference("sensor-hub");
                resultSegment = await container.ListBlobsSegmentedAsync(@"/logs/post" + pathToBlob, true, BlobListingDetails.All, 1000, continuationToken, null, null);

               if(resultSegment.Results.Count() ==  1)
                {
                    CloudAppendBlob blob =  (CloudAppendBlob) resultSegment.Results.First();
                    await blob.AppendTextAsync(fullFilePath);
                }
                else
                {
                    CloudAppendBlob blob = container.GetAppendBlobReference(pathToBlob + "//" + Guid.NewGuid() + ".json");
                    await blob.UploadTextAsync(fullFilePath);
                }
            }
            catch(Exception e)
            {
                Console.WriteLine("Failue uploading the blob: " + e.Message);
                return false;
            }

            return true;
        }

        static async Task<List<CloudBlockBlob>> GetAllList(CloudBlobClient blobCli)
        {

            BlobContinuationToken continuationToken = null;
            BlobResultSegment resultSegment = null;
            CloudBlobContainer container = blobCli.GetContainerReference("sensor-hub");
            try
            {
                resultSegment = await container.ListBlobsSegmentedAsync(@"/logs/pre", true, BlobListingDetails.All, 1000, continuationToken, null, null);
                List<CloudBlockBlob> rgList = resultSegment.Results.OfType<CloudBlockBlob>().OrderByDescending(m => m.Properties.LastModified).ToList();
                return rgList;
            }
            catch(Exception e)
            {
                Console.WriteLine("Error getting latest blob: " + e.Message);
                return null;
            }
        }

        private static string run_cmd(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "my/full/path/to/python.exe";
            start.Arguments = string.Format("{0} {1}", cmd, args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    return reader.ReadToEnd();        
                }
            }
        }
    }
}
