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
using Microsoft.WindowsAzure.Storage.Blob;

namespace AIHubMobile
{
    public interface IRestAzureStorage<T>
    {
        Task<bool> RefreshWeatherSets(WeatherSet.WeatherSetDateRanges range);
        Task<IEnumerable<WeatherStation>> GetAllWeatherSets(bool forceRefresh = false, WeatherSet.WeatherSetDateRanges range = WeatherSet.WeatherSetDateRanges.Today);
        Task<bool> UpdateStationOptions(StationOptions options);
        Task<StationOptions> GetConfigSetting(String deviceName);
    }
}
