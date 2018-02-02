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
    public class RestClient : IRestClient
    {
        List<WeatherSet> Items;
        HttpClient client;

        public RestClient()
        {
            client = new HttpClient();
            client.MaxResponseContentBufferSize = 256000;
            Items = new List<WeatherSet>();
        }

        public async Task<List<WeatherSet>> GetAllWeatherSets(bool forceRefresh = false)
        {
            string url = @"http://localhost:50405/api/WeatherSetController/GetAllForStation";
            var uri = new Uri(string.Format(url, string.Empty));
        
            var response = await client.GetAsync(uri);

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                Items = JsonConvert.DeserializeObject<List<WeatherSet>>(content);
            }
       
            return await Task.FromResult(Items);
        }
    }
}
