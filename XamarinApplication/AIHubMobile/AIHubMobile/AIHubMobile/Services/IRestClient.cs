using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace AIHubMobile
{
    public interface IRestClient
    {
         Task<List<WeatherSet>> GetAllWeatherSets(bool forceRefresh = false);
    }
}
