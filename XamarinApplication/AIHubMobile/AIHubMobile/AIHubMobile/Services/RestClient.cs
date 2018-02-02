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

            Items.Add(new WeatherSet(1, Convert.ToDateTime("2016-01-01"), 22, 60, 8, 20));
            Items.Add(new WeatherSet(2, Convert.ToDateTime("2016-03-01"), 22, 60, 8, 20));
            Items.Add(new WeatherSet(3, Convert.ToDateTime("2016-02-01"), 22, 60, 8, 20));
        }

        public async Task<bool> RefreshWeatherSets()
        {
            //Comment this is when we use the web API to update

            //string url = @"http://localhost:50405/api/WeatherSetController/GetAllForStation";
            //var uri = new Uri(string.Format(url, string.Empty));

            //var response = await client.GetAsync(uri);

            //if (response.IsSuccessStatusCode)
            //{
            //    var content = await response.Content.ReadAsStringAsync();
            //    Items = JsonConvert.DeserializeObject<List<WeatherSet>>(content);
            //    return await Task.FromResult(true);
            //}
            //else
            //{
            //    return await Task.FromResult(false);
            //}

            //Hardcoded for now

            return await Task.FromResult(true);
        }

        public async Task<IEnumerable<WeatherSet>> GetAllWeatherSets(bool forceRefresh = false)
        {
            return await Task.FromResult(Items);
        }
    }
}
