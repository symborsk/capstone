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

        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("Please specify -GetLatestData or -SendToAzureBlob" + args.Length);
                return;
            }

            string function = args[0];

            switch (function)
            {
                case "-GetLatestData":
                    GetLatestPreProcessedData();
                    return;
                case "-SendToAzureBlob":
                    SendAllDataInPostProccessing();
                    return;
                default:
                    Console.WriteLine("Unrecognized command... Goodbye");
                    return;
            }     
        }

        static private void GetLatestPreProcessedData()
        {
            CloudStorageAccount storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            CloudBlobClient client = storageAccount.CreateCloudBlobClient();

            List<CloudBlockBlob> rgBlobs = GetAllList(client);

            if(rgBlobs.Count == 0 )
            {
                Console.WriteLine(false);
                return;
            }

            CloudBlockBlob blockBlob = rgBlobs[0];
            string blobText = blockBlob.DownloadText();

            if (File.Exists(@"..\test_files\preprocessed_data.json"))
            {
                File.Delete(@"..\test_files\preprocessed_data.json");
            }

            File.WriteAllText(@"..\test_files\preprocessed_data.json", blobText);

            blockBlob.Delete();
            Console.WriteLine(true);          
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
                    fullText = Environment.NewLine + fullText;
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

        static List<CloudBlockBlob> GetAllList(CloudBlobClient blobCli)
        {
            BlobContinuationToken continuationToken = null;
            BlobResultSegment resultSegment = null;
            CloudBlobContainer container = blobCli.GetContainerReference("sensor-hub");
            try
            {
                resultSegment = container.ListBlobsSegmented(@"logs/pre/", true, BlobListingDetails.All, 1000, continuationToken, null, null);
                List<CloudBlockBlob> rgList = resultSegment.Results.OfType<CloudBlockBlob>().OrderByDescending(m => m.Properties.LastModified).ToList();
                return rgList;
            }
            catch(Exception e)
            {
                Console.WriteLine("Error getting latest blob: " + e.Message);
                return null;
            }
        }

        private static void SendAllDataInPostProccessing()
        {
            CloudStorageAccount storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            CloudBlobClient client = storageAccount.CreateCloudBlobClient();

            try
            {
                string file = File.ReadAllText(@"..\test_files\processed_data.json");
                string[] objs = file.Split(new[] { "\n", "\r\n" }, StringSplitOptions.RemoveEmptyEntries);

                foreach (string jsonString in objs)
                {
                    JObject obj = JObject.Parse(jsonString);
                    string timestamp = obj["timestamp"].ToString();
                    SendJsonToStorage(client, obj.ToString(Formatting.None), timestamp);
                }

                if (File.Exists(@"..\test_files\processed_data.json"))
                {
                    File.Delete(@"..\test_files\processed_data.json");
                }

                Console.WriteLine(true);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}
