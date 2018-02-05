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
using System.Net.Http;

[assembly:Xamarin.Forms.Dependency(typeof(AIHubMobile.RestClient))]
namespace AIHubMobile
{
    public class RestClient : IRestClient<WeatherSet>
    {
        List<WeatherSet> Items;
        HttpClient client;

        public RestClient()
        {
            client = new HttpClient();
            client.MaxResponseContentBufferSize = 256000;
            Items = new List<WeatherSet>();

            //This is hardoded now it will eventually get the data from a WEB APi
            Items.Add(new WeatherSet(1, Convert.ToDateTime("2016-01-01"), 22, 60, 8, 20));
            Items.Add(new WeatherSet(2, Convert.ToDateTime("2016-03-01"), 22, 60, 8, 20));
            Items.Add(new WeatherSet(3, Convert.ToDateTime("2016-02-01"), 22, 60, 8, 20));
        }

        public async Task<bool> RefreshWeatherSets()
        {

            //Hardcoded for now but we will have web api calls updating in this fucntion

            return await Task.FromResult(true);
        }

        public async Task<IEnumerable<WeatherSet>> GetAllWeatherSets(bool forceRefresh = false)
        {
            return await Task.FromResult(Items);
        }
    }
}
