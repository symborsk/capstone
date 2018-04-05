using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;
namespace AIServerConsoleApp
{
    class Program
    {
        static async void Main(string[] args)
        {
            if (args.Length != 0)
            {
                Console.WriteLine("Invalid number of arguments: expected 0" + args.Length);
                return;
            }

            CloudStorageAccount storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            CloudBlobClient client = storageAccount.CreateCloudBlobClient();

            List<CloudBlockBlob> rgBlobs = await GetAllList(client);

            foreach(CloudBlockBlob blob in rgBlobs)
            {
                String sDownloadedBlob = await blob.DownloadTextAsync();

            }

        }

        static async void PushDataUpToAzure(CloudBlobClient cli, String pathToJson, string timestamp)
        {
            bool succ = await SendJsonToStorage(cli, pathToJson, timestamp);

            if (succ)
                Console.WriteLine("Success writing JSON file to azure storage");
            else
                Console.WriteLine("Failure Loading JSON file to azure storage... Goodbye");
        }

        static async Task<bool> SendJsonToStorage(CloudBlobClient blobClient, string fullFilePath, string timeStamp)
        {
           

            try
            {
                //Convert the unix timestamp to a date
                DateTime dtDateTime = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc);
                dtDateTime = dtDateTime.AddSeconds(Double.Parse(timeStamp));

                string pathToBlob = dtDateTime.Year + "//" + dtDateTime.Month + "//" + dtDateTime.Date;

                // Retrieve reference to a previously created container
                //TODO: query all the device names
                CloudBlobContainer container = blobClient.GetContainerReference("sensor-hub");
                CloudBlockBlob blob = container.GetBlockBlobReference(pathToBlob);

                await blob.UploadFromFileAsync(fullFilePath);
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
    }
}
