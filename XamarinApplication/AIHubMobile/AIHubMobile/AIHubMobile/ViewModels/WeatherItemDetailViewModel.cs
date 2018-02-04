using System;

namespace AIHubMobile
{
    public class WeatherItemDetailViewModel : BaseViewModel
    {
        public WeatherSet Item { get; set; }
        public WeatherItemDetailViewModel(WeatherSet item = null)
        {
            Title = "Station Name: " + item?.StationId;
            Item = item;
        }
    }
}
