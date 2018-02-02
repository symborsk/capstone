using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace AIHubMobile
{
    public interface IRestClient<T>
    {
        Task<bool> RefreshWeatherSets();
        Task<IEnumerable<WeatherSet>> GetAllWeatherSets(bool forceRefresh = false);
    }
}
