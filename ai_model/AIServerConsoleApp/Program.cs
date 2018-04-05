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

    //    BlobContinuationToken continuationToken = null;
    //    BlobResultSegment resultSegment = null;

    //        try
    //        {
    //            //Call ListBlobsSegmentedAsync and enumerate the result segment returned, while the continuation token is non-null.
    //            //When the continuation token is null, the last page has been returned and execution can exit the loop.
    //            do
    //            {
    //                //This overload allows control of the page size. You can return all remaining results by passing null for the maxResults parameter,
    //                //or by calling a different overload.
    //                // from: https://hahoangv.wordpress.com/2016/05/16/azure-storage-step-4-blobs-storage-in-action/
    //                List<string> prefixForBlob = GeneratePrefixStrings(WeatherSet.WeatherSetDateRanges.AllTime);
    //                foreach (string prefix in prefixForBlob)
    //                {
    //                    if (resultSegment == null)
    //                    {
    //                        resultSegment = await con.ListBlobsSegmentedAsync(prefix, true, BlobListingDetails.All, 1000, continuationToken, null, null);
    //}
    //                    else
    //                    {
    //                        BlobResultSegment temp = await con.ListBlobsSegmentedAsync(prefix, true, BlobListingDetails.All, 1000, continuationToken, null, null);
    //resultSegment.Results.Union(temp.Results);
    //                    }
    //                }

        static async CloudBlockBlob GetLatestPath(CloudBlobClient blobCli)
        {

            BlobContinuationToken continuationToken = null;
            BlobResultSegment resultSegment = null;
            CloudBlobContainer container = blobCli.GetContainerReference("sensor-hub");
            try
            {
                resultSegment = await container.ListBlobsSegmentedAsync("", true, BlobListingDetails.All, 1000, continuationToken, null, null);
                List<CloudBlockBlob> rgList = resultSegment.Results.OfType<CloudBlockBlob>().OrderByDescending(m => m.Properties.LastModified).ToList();
                return rgList.First();
            }
            catch(Exception e)
            {
                Console.WriteLine("Error getting latest blob: " + e.Message);
            }
 

        }
    }
}
