using System;
using System.Collections.Generic;
using System.Linq;
using System.Configuration;
using System.Threading.Tasks;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Net.Http;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;
using Microsoft.WindowsAzure.Storage.Table;
using System.Reflection;
using System.Web;
using System.Web.Mvc;

namespace AIHubWeb
{
    public class AzureStorageController : Controller
    {
        CloudStorageAccount storageAccount;
        List<WeatherStation> weatherStations;

        public AzureStorageController()
        {
            //TODO: look at using shared accounts
            //storageAccount = CloudStorageAccount.Parse("SharedAccessSignature=?st=2017-02-28T14%3A17%3A00Z&se=2018-03-03T14%3A17%3A00Z&sp=rl&sv=2017-04-17&sr=c&sig=nxoO5iSP8rZjiQilNQsOBa89W6LqtRyTEOpqnwnqXXE%3D;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/sensor-hub?st=2017-02-28T14%3A17%3A00Z&se=2018-03-03T14%3A17%3A00Z&sp=rl&sv=2017-04-17&sr=c&sig=nxoO5iSP8rZjiQilNQsOBa89W6LqtRyTEOpqnwnqXXE%3D");
            storageAccount = CloudStorageAccount.Parse("DefaultEndpointsProtocol=https;AccountName=pcldevbgwilkinson01;AccountKey=NPkk2BjPvlG1Am78JrSi4ylEQNB3F6tacE/G8P3x8zLOe/BqZwvYMCXP+ni9KMwmx+px/f+J+n9QJq+v9eVSGg==;BlobEndpoint=https://pcldevbgwilkinson01.blob.core.windows.net/;QueueEndpoint=https://pcldevbgwilkinson01.queue.core.windows.net/;TableEndpoint=https://pcldevbgwilkinson01.table.core.windows.net/;FileEndpoint=https://pcldevbgwilkinson01.file.core.windows.net/");
            weatherStations = new List<WeatherStation>();
        }

        public async Task<List<WeatherStation>> GetCurrentWeatherSets()
        {
            return await Task.FromResult(weatherStations);
        }

        public async Task<List<WeatherSet>> GetStationListForName(string stationName, DateTime start, DateTime end)
        {
            await RefreshWeatherSets(WeatherSet.WeatherSetDateRanges.AllTime);
            List<WeatherSet> rgSet = new List<WeatherSet>();
            foreach (WeatherStation stat in weatherStations)
            {
                if (stat.StationName == stationName)
                {
                    rgSet = stat.rgWeatherSets;
                    break;
                }
            }

            //Remove all that are not withing the start and end date
            rgSet.RemoveAll(set => set.RecordedTime < start || set.RecordedTime > end);

            return rgSet;
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
                    foreach (string prefix in prefixForBlob)
                    {
                        if (resultSegment == null)
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
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }

            return resultSegment;
        }

        private async Task<bool> CreateWeatherStationsFromBlob(BlobResultSegment seg)
        {

            weatherStations.Clear();

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
                        text += "]";
                    }

                    JArray allDataSets = JArray.Parse(text);
                    Type weatherSetClass = typeof(WeatherSet);

                    foreach (JObject root in allDataSets)
                    {
                        string devName = root["device_name"].ToString();
                        double lat = Convert.ToDouble(root["location"]["lat"].ToString());
                        double lon = Convert.ToDouble(root["location"]["lon"].ToString());

                        int currStationIndex = weatherStations.FindIndex(x => x.StationName == devName);

                        //If a station of that type does not exist add it now and set current index as that
                        if (currStationIndex == -1)
                        {
                            weatherStations.Add(new WeatherStation(devName, lat, lon));
                            currStationIndex = weatherStations.Count - 1;
                        }

                        //Set the recorded time of this in local time, as it is stored in UTC time on server
                        WeatherSet newSet = new WeatherSet();

                        // Unix timestamp is what we store so convert it to local tie
                        double unixTimeStamp = double.Parse(root["timestamp"].ToString());
                        DateTime dtDateTime = new DateTime(1970, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc);
                        newSet.RecordedTime = dtDateTime.AddSeconds(unixTimeStamp).ToLocalTime();

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
                        weatherStations[currStationIndex].AddWeatherSet(newSet);
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
            string sLogPrefix;
            string testmode = ConfigurationManager.AppSettings["TestMode"];
            if (testmode == "true")
            {
                sLogPrefix = @"test/";
            }
            else
            {
                sLogPrefix = @"logs/";
            }
       
            switch (range)
            {
                case WeatherSet.WeatherSetDateRanges.Today:
                    prefixes.Add(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month + "//" + currentUtcDay.Date);
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.PastThreeDays:
                    for (int i = 0; i < 3; i++)
                    {
                        prefixes.Add(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month + "//" + currentUtcDay.Date);
                        currentUtcDay.AddDays(-1);
                    }
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.PastWeek:
                    for (int i = 0; i < 7; i++)
                    {
                        prefixes.Add(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month + "//" + currentUtcDay.Date);
                        currentUtcDay.AddDays(-1);
                    }
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.ThisMonth:
                    prefixes.Add(sLogPrefix + currentUtcDay.Year + "//" + currentUtcDay.Month);
                    return prefixes;

                case WeatherSet.WeatherSetDateRanges.ThisYear:
                    prefixes.Add(sLogPrefix + currentUtcDay.Year);
                    return prefixes;

                default:
                    prefixes.Add("");
                    return prefixes;
            }
        }

        private EditableStationOptions CreateDefaultEditableStationOption(CloudTable tab, String name)
        {
            EditableStationOptions option = new EditableStationOptions(name);

            TableOperation insertOp = TableOperation.InsertOrReplace(option);

            //We do not need to await this 
            tab.ExecuteAsync(insertOp);

            return option;
        }

        public async Task<bool> UpdateDeviceConfigSettings(EditableStationOptions option)
        {
            CloudTableClient tableClient = storageAccount.CreateCloudTableClient();
            CloudTable table = tableClient.GetTableReference("DeviceConfigSettings");

            TableOperation insertOrRepOp = TableOperation.InsertOrReplace(option);

            TableResult res = await table.ExecuteAsync(insertOrRepOp);
            if (res.HttpStatusCode != 204)
            {
                Console.WriteLine("Failure updating station options");
            }

            return true;
        }

        public async Task<EditableStationOptions> GetConfigSetting(String deviceName)
        {
            CloudTableClient tableClient = storageAccount.CreateCloudTableClient();
            CloudTable table = tableClient.GetTableReference("DeviceConfigSettings");


            //Get the station options or create them this may change later if we want to do this at the device
            TableOperation op = TableOperation.Retrieve<EditableStationOptions>("EditableStationOptions", deviceName);
            TableResult retrievedResult = await table.ExecuteAsync(op);

            EditableStationOptions option;
            if (retrievedResult.Result == null)
            {
                option = CreateDefaultEditableStationOption(table, deviceName);
            }
            else
            {
                option = (EditableStationOptions)retrievedResult.Result;
            }

            return option;
        }
    }
}

