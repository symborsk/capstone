/**
 * RestClient.cs
 * By: John Symborski
 * Capstone Group 2
 * This service will do any interactio with RESTful Web Api.
 * */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Net.Http;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;

[assembly:Xamarin.Forms.Dependency(typeof(AIHubMobile.RestClient))]
namespace AIHubMobile
{
    public class RestClient : IRestClient<WeatherStation>
    {
        List<WeatherStation> Items;
        HttpClient client;
        CloudStorageAccount storageAccount;

        public RestClient()
        {
            client = new HttpClient();
            client.MaxResponseContentBufferSize = 256000;

            //storageAccount = CloudStorageAccount.Parse("SharedAccessSignature=?st=2017-02-28T14%3A17%3A00Z&se=2018-03-03T14%3A17%3A00Z&sp=rl&sv=2017-04-17&sr=c&sig=nxoO5iSP8rZjiQilNQsOBa89W6LqtRyTEOpqnwnqXXE%3D;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/sensor-hub?st=2017-02-28T14%3A17%3A00Z&se=2018-03-03T14%3A17%3A00Z&sp=rl&sv=2017-04-17&sr=c&sig=nxoO5iSP8rZjiQilNQsOBa89W6LqtRyTEOpqnwnqXXE%3D");
            storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");

            Items = new List<WeatherStation>();

            //This is hardoded now it will eventually get the data from a WEB APi
            List<WeatherSet> weatherSets = new List<WeatherSet>();
            ReadOnlyStationOptions roOptions = new ReadOnlyStationOptions(88, 21, true);
            EditableStationOptions editOptions = new EditableStationOptions(true, new TimeSpan(1, 0, 0));
            weatherSets.Add(new WeatherSet(1, Convert.ToDateTime("2016-01-01"), 22, 60, 8, 20));
            weatherSets.Add(new WeatherSet(2, Convert.ToDateTime("2016-03-01"), 22, 60, 8, 20));
            weatherSets.Add(new WeatherSet(3, Convert.ToDateTime("2016-02-01"), 22, 60, 8, 20));

            Items.Add(new WeatherStation(new StationOptions(editOptions, roOptions), 1, weatherSets));
        }

        public async Task<bool> RefreshWeatherSets()
        {
            
            // Create the blob client.
            CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();
            Console.WriteLine("Test Statment ---------------------------------------------");

            // Retrieve reference to a previously created container.
            CloudBlobContainer container = blobClient.GetContainerReference("sensor-hub");

            BlobResultSegment seg = await ListBlobsAsync(container);

            // Retrieve reference to a blob named "myblob".
            CloudBlockBlob blockBlob = container.GetBlockBlobReference("sensor-hub");

            //Hardcoded for now but we will have web api calls updating in this fucntion

            return await Task.FromResult(true);
        }

        public async Task<IEnumerable<WeatherStation>> GetAllWeatherSets(bool forceRefresh = false)
        {
            return await Task.FromResult(Items);
        }

        public async Task<BlobResultSegment> ListBlobsAsync(CloudBlobContainer con)
        {

            BlobContinuationToken continuationToken = null;
            BlobResultSegment resultSegment = null;

            try
            {
                //Call ListBlobsSegmentedAsync and enumerate the result segment returned, while the continuation token is non-null.
                //When the continuation token is null, the last page has been returned and execution can exit the loop.
                do
                {
                    //This overload allows control of the page size. You can return all remaining results by passing null for the maxResults parameter,
                    //or by calling a different overload.
                    // from: https://hahoangv.wordpress.com/2016/05/16/azure-storage-step-4-blobs-storage-in-action/
                    resultSegment = await con.ListBlobsSegmentedAsync("", true, BlobListingDetails.All, 10, continuationToken, null, null);
                    foreach (CloudAppendBlob blobItem in resultSegment.Results)
                    {
                        string text;                   
                        text = await blobItem.DownloadTextAsync();
                        var objects = JArray.Parse(text);

                        foreach (JObject root in objects)
                        {
                            foreach (KeyValuePair<String, JToken> tag in root)
                            {
                                String tagName = tag.Key.ToString();
                                String tagValue = tag.Value.ToString();
                                Console.WriteLine("{0} : {1}", tagName, tagValue);
                            }
                        }
                    }
                    Console.WriteLine();

                    //Get the continuation token.
                    continuationToken = resultSegment.ContinuationToken;
                }
                while (continuationToken != null);
            }
            catch(Exception e)
            {
                Console.WriteLine(e.Message);
            }

            return resultSegment;
        }
    }
}
