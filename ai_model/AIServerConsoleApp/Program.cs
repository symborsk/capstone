using System;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Threading.Tasks;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;

namespace AIServerConsoleApp
{
    class Program
    {
        static string pythonPath = "";

        static void Main(string[] args)
        {
            if (args.Length != 0)
            {
                Console.WriteLine("Invalid number of arguments: expected 0" + args.Length);
                return;
            }

            pythonPath = find_python_path();

            CloudStorageAccount storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            CloudBlobClient client = storageAccount.CreateCloudBlobClient();
      
            Task<List<CloudBlockBlob>> task = Task.Run(() => GetAllList(client));
            List<CloudBlockBlob> rgBlobs = task.Result;
           
            foreach (CloudBlockBlob blob in rgBlobs)
            {
                Task<string> taskDownload = Task.Run(() => blob.DownloadTextAsync());
                String sDownloadedBlob = taskDownload.Result;
                String [] sDownloadedBlobs = sDownloadedBlob.Split(new[] { Environment.NewLine }, StringSplitOptions.None);

                foreach (string item in sDownloadedBlobs)
                {
                    // Write the JSON to a file
                    JObject obj = JObject.Parse(item);
                    string dir = Directory.GetCurrentDirectory();
                    string guid = Guid.NewGuid().ToString();
                    using (StreamWriter file = File.CreateText(@"..\test_files\" + guid + ".json"))
                    using (JsonTextWriter writer = new JsonTextWriter(file))
                    {
                        obj.WriteTo(writer);
                    }

                    // Get a timestamp for the processed data
                    string timestamp = obj["timestamp"].ToString();

                    // Run AI model to get JSON forecast & then send it back to Azure
                    obj["Forecast"] = JObject.Parse(run_cmd(@"..\scripts\model.py", String.Format("-eval -file {0}", guid + ".json")));
                    PushDataUpToAzure(client, obj.ToString(Formatting.None), timestamp);
                }
            }
        }

        static void PushDataUpToAzure(CloudBlobClient cli, string jsonObj, string timestamp)
        {
            bool succ = SendJsonToStorage(cli, jsonObj, timestamp);

            if (succ)
                Console.WriteLine("Success writing JSON file to azure storage");
            else
                Console.WriteLine("Failure Loading JSON file to azure storage... Goodbye");
        }

        static bool SendJsonToStorage(CloudBlobClient blobClient, string fullText, string timeStamp)
        {
            BlobContinuationToken continuationToken = null;
            BlobResultSegment resultSegment = null;

            try
            {
                //Convert the unix timestamp to a date
                DateTime dtDateTime = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc);
                dtDateTime = dtDateTime.AddSeconds(Double.Parse(timeStamp));
				String outputPath = String.Format(@"logs/post/{0}/{1}/{2}", dtDateTime.Year, dtDateTime.Month, dtDateTime.Day);

                // Retrieve reference to a previously created container
                https://pcldevbgwilkinson01.blob.core.windows.net/sensor-hub/logs/pre/2018/04/06/0_8b385536905846c68aa7a3e4e476200b_1.json
                CloudBlobContainer container = blobClient.GetContainerReference("sensor-hub");
                resultSegment = container.ListBlobsSegmented(outputPath, true, BlobListingDetails.All, 1000, continuationToken, null, null);

               if(resultSegment.Results.Count() ==  1)
                {
                    CloudAppendBlob blob =  (CloudAppendBlob) resultSegment.Results.First();
                    blob.AppendText(fullText);
                }
                else
                {
                    CloudAppendBlob blob = container.GetAppendBlobReference(outputPath + "/" + Guid.NewGuid() + ".json");
                    blob.UploadText(fullText);
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
                resultSegment = await container.ListBlobsSegmentedAsync(@"logs/pre/", true, BlobListingDetails.All, 1000, continuationToken, null, null);
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
            start.FileName = pythonPath;
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

        private static string find_python_path()
        {
            ProcessStartInfo procStartInfo = new ProcessStartInfo("cmd.exe", @"/C " + "python -c \"import sys; print(sys.executable)\"" );

            procStartInfo.RedirectStandardOutput = true;
            procStartInfo.UseShellExecute = false;
            procStartInfo.CreateNoWindow = true;

            // wrap IDisposable into using (in order to release hProcess) 
            using (Process process = new Process())
            {
                process.StartInfo = procStartInfo;
                process.Start();

                // Add this: wait until process does its work
                process.WaitForExit();

                // and only then read the result
                string result = process.StandardOutput.ReadToEnd();
                return result;
            }
        }
    }
}
