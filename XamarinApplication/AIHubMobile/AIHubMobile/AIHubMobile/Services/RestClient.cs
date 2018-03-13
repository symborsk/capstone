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
using System.Reflection;

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
        }

        public async Task<bool> RefreshWeatherSets(WeatherSet.WeatherSetDateRanges range)
        {

            // Create the blob client.
            CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();

            // Retrieve reference to a previously created container.
            CloudBlobContainer container = blobClient.GetContainerReference("sensor-hub");

            BlobResultSegment seg = await ListBlobsAsync(container, range);
            
            bool succ = await CreateWeatherStationsFromBlob(seg);

            // Retrieve reference to a blob named "myblob".

            return await Task.FromResult(true);
        }

        public async Task<IEnumerable<WeatherStation>> GetAllWeatherSets(bool forceRefresh = false, WeatherSet.WeatherSetDateRanges range = WeatherSet.WeatherSetDateRanges.Today)
        {
            return await Task.FromResult(Items);
        }

        public async Task<BlobResultSegment> ListBlobsAsync(CloudBlobContainer con, WeatherSet.WeatherSetDateRanges range)
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
                    List<string> prefixForBlob = GeneratePrefixStrings(WeatherSet.WeatherSetDateRanges.AllTime);
                    foreach(string prefix in prefixForBlob)
                    {
                        if(resultSegment == null)
                        {
                            resultSegment = await con.ListBlobsSegmentedAsync(prefix, true, BlobListingDetails.All, 1000, continuationToken, null, null);
                        }
                        else
                        {
                            BlobResultSegment temp = await con.ListBlobsSegmentedAsync(prefix, true, BlobListingDetails.All, 1000, continuationToken, null, null);
                            resultSegment.Results.Union(temp.Results);
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

        private async Task<bool> CreateWeatherStationsFromBlob(BlobResultSegment seg)
        {
            Items.Clear();
            foreach (CloudBlockBlob blobItem in seg.Results)
            {
                string text;
                try
                {
                    text = await blobItem.DownloadTextAsync();

                    //The azure stream analytics job that creates the JSON array does not add a ']' at the end until the day is completed
                    //This is an undesirable feature as it caused any data we downlod from today to break the JArray parser, add a ']'
                    if (!text.EndsWith("]"))
                    {
                        text.Append(']');
                    }

                    JArray allDataSets = JArray.Parse(text);
                    Type weatherSetClass = typeof(WeatherSet);

                    foreach (JObject root in allDataSets)
                    {
                        string devName = root["device_name"].ToString();
                        double lat = Convert.ToDouble(root["location"]["lat"].ToString());
                        double lon = Convert.ToDouble(root["location"]["lon"].ToString());

                        int currStationIndex = Items.FindIndex(x => x.StationName == devName);
                        
                        //If a station of that type does not exist add it now and set current index as that
                        if (currStationIndex == -1)
                        {
                            Items.Add(new WeatherStation(devName, lat, lon));
                            currStationIndex = Items.Count - 1;
                        }

                        //Set the recorded time of this in local time, as it is stored in UTC time on server
                        WeatherSet newSet = new WeatherSet();
                        DateTime utcTime = DateTime.Parse(root["EventProcessedUtcTime"].ToString());
                        newSet.RecordedTime = utcTime.ToLocalTime();

                        //Sensors are another array that we need to dive into
                        JArray sensorArray = JArray.Parse(root["sensors"].ToString());

                        foreach (JObject sensorRoot in sensorArray)
                        {              
                            JObject dataObj = JObject.Parse(sensorRoot["data"].ToString());
                            foreach (KeyValuePair<String, JToken> tag in dataObj)
                            {
                                String tagName = tag.Key.ToString();
                                String tagValue = tag.Value.ToString();

                                //This may seem strange but this will allows us to download the data and simply check and see what sensors have data
                                //This allows the sensors at the station side to be easily turned on or off without crashing the app
                                //If we have a property that matched the data we will
                                PropertyInfo info = weatherSetClass.GetProperty(tagName);
                                if (info != null)
                                {
                                    info.SetValue(newSet, tagValue, null);
                                }
                            }
                        }

                        //Add the set once this is done
                        Items[currStationIndex].AddWeatherSet(newSet);
                    }
                }
                //This can happen when there is an empty blob object 
                catch (Exception ex)
                {   
                    
                    Console.WriteLine("Failure getting a blob: " + ex.Message);
                }
            }

            return await Task.FromResult(true);
        }

        //Generates all the prefixes needed for the specific range
        private List<string> GeneratePrefixStrings(WeatherSet.WeatherSetDateRanges range)
        {
            List<string> prefixes = new List<string>();
            //Blobs are stroed under utc time
            DateTime currentUtcDay = DateTime.UtcNow;
            string sLogPrefix = @"logs/";
            switch (range)
            {
                case WeatherSet.WeatherSetDateRanges.Today:    
                    prefixes.Append(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month + "//" + currentUtcDay.Date);
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.PastThreeDays:
                    for( int i = 0; i < 3; i++)
                    {
                        prefixes.Append(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month + "//" + currentUtcDay.Date);
                        currentUtcDay.AddDays(-1);
                    }
                    return prefixes;
              
                case WeatherSet.WeatherSetDateRanges.PastWeek:
                    for (int i = 0; i < 7; i++)
                    {
                        prefixes.Append(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month + "//" + currentUtcDay.Date);
                        currentUtcDay.AddDays(-1);
                    }
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.ThisMonth:
                    prefixes.Append(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month);
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.ThisYear:
                    prefixes.Append(sLogPrefix + currentUtcDay.Year);
                    return prefixes;

                default:
                    prefixes.Add("");
                    return prefixes;
            }
        }
    }
}
