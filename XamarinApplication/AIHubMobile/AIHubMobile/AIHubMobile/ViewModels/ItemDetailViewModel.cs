using System;

namespace AIHubMobile
{
    public class ItemDetailViewModel : BaseViewModel
    {
        public WeatherSet Item { get; set; }
        public ItemDetailViewModel(WeatherSet item = null)
        {
            Title = "Station Name: " + item?.StationId;
            Item = item;
        }
    }
}
