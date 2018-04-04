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
            if (args.Length != 2)
            {
                Console.WriteLine("Invalid number of arguments: Exepected[0 : filePathToJsonFile | 1 : timeStamp] Got: " + args.Length);
                return;
            }

            bool succ = await SendJsonToStorage(args[0], args[1]);

            if (succ)
                Console.WriteLine("Success writing JSON file to azure storage");
            else
                Console.WriteLine("Failure Loading JSON file to azure storage... Goodbye");

        }

        static async Task<bool> SendJsonToStorage(string fullFilePath, string timeStamp)
        {
            CloudStorageAccount storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            // Create the blob client.
            CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();

            try
            {
                //Convert the unix timestamp to a date
                DateTime dtDateTime = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc);
                dtDateTime = dtDateTime.AddSeconds(Double.Parse(timeStamp));

                string pathToBlob = dtDateTime.Year + "//" + dtDateTime.Month + "//" + dtDateTime.Date;

                // Retrieve reference to a previously created container.
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
    }
}
