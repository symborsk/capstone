/**
 * IRestClient.cs
 * By: John Symborski
 * Capstone Group 2
 * Interface to define the interaction with RESTFUL web API.
 * */

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
